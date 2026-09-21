# agent-elevate-helper.ps1 - the elevated half of Claude Code's own elevation channel
#
# Launched by agent-elevate.ps1 through Start-Process -Verb RunAs, which is where the UAC
# prompt appears.  Serves this one Claude Code session until it is -Stopped or
# IdleTimeoutMinutes passes with no request.
#
# NOT sd-elevate-helper.ps1 - see agent-elevate.ps1's header for why these are two separate
# pairs rather than one shared one.
#
# WHAT IT WILL RUN, AND WHAT IT WILL NOT.  A request is one line of JSON naming a script and
# its arguments; agent-elevate-lib.ps1 decides whether it is allowed, and the answer is
# taken HERE, not trusted from the caller.  Only a .ps1 file directly inside -AllowRoot
# (the repo's gplbld directory), with plain arguments, is run.  Anything else is answered
# REFUSED|<why> and logged.  There is no raw-path form any more.
#
# ALWAYS CAPTURED, NEVER LEFT IN THE REPO.  CLAUDE.md's instrument rule: a verdict with no
# evidence of what ran is not a result.  Standard output and standard error go to two files
# under -OutDir (not beside the script), named in the reply so the caller can check they
# exist and are fresh.
#
# A RUN HAS A HARD LIMIT (-MaxRunMinutes).  A script that hangs is killed, with its child
# processes, and answered 124 - the caller must never wait for ever on a pipe.
#
# THE PIPE DACL IS LOAD-BEARING, same reasoning as SD's own: without it the pipe takes this
# elevated process's default DACL and the unelevated caller is refused "Access to the path is
# denied".  Granting only this user's SID is the whole access boundary - no other ACCOUNT on
# this machine can reach the pipe; every process of THIS user can, which is why the server
# re-checks every request and why the client will not accept a reply that has no evidence.
#
# WHAT THIS PROCESS IS: once -Start succeeds, anything the allow-list admits runs with this
# user's ADMINISTRATOR rights until -Stop or the idle timeout, with no per-command
# confirmation.  Stop it (`agent-elevate.ps1 -Stop`) when the elevated work is done.

param(
    [Parameter(Mandatory = $true)][string]$PipeName,
    [Parameter(Mandatory = $true)][string]$AllowRoot,
    [Parameter(Mandatory = $true)][string]$OutDir,
    [int]$IdleTimeoutMinutes = 60,
    [int]$MaxRunMinutes = 30,
    [string]$LogFile = ''
)

. (Join-Path $PSScriptRoot 'agent-elevate-lib.ps1')

function Say($m) {
    if ($LogFile -ne '') {
        try {
            Add-Content -LiteralPath $LogFile -Value (
                "{0} {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $m)
        } catch { }
    }
}

$elevated = ([Security.Principal.WindowsPrincipal](
    [Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $elevated) {
    Say "not elevated - refusing to serve"
    exit 2
}

Say ("helper up, pid {0}, pipe {1}, idle {2} min, max run {3} min, allow root {4}, out dir {5}" -f
    $PID, $PipeName, $IdleTimeoutMinutes, $MaxRunMinutes, $AllowRoot, $OutDir)

$me = [Security.Principal.WindowsIdentity]::GetCurrent().User
$lastActivity = Get-Date

try {
    while ($true) {
        $idleMin = ((Get-Date) - $lastActivity).TotalMinutes
        if ($idleMin -ge $IdleTimeoutMinutes) {
            Say "idle $([int]$idleMin) min >= limit - exiting"
            break
        }

        $psec = New-Object System.IO.Pipes.PipeSecurity
        $psec.AddAccessRule((New-Object System.IO.Pipes.PipeAccessRule(
            $me, 'FullControl', 'Allow')))

        $server = New-Object System.IO.Pipes.NamedPipeServerStream(
            $PipeName, 'InOut', 1, 'Byte', 'Asynchronous', 4096, 4096, $psec)

        $iar = $server.BeginWaitForConnection($null, $null)
        $connected = $false
        while (-not $connected) {
            if ($iar.AsyncWaitHandle.WaitOne(2000)) { $connected = $true; break }
            $idleMin = ((Get-Date) - $lastActivity).TotalMinutes
            if ($idleMin -ge $IdleTimeoutMinutes) {
                Say "idle $([int]$idleMin) min >= limit while waiting - exiting"
                $server.Dispose()
                exit 0
            }
        }
        $server.EndWaitForConnection($iar)
        $lastActivity = Get-Date

        $reader = New-Object IO.StreamReader($server)
        $writer = New-Object IO.StreamWriter($server)
        $writer.AutoFlush = $true

        $req = $reader.ReadLine()

        if ($null -eq $req) { $server.Dispose(); continue }

        if ($req -eq 'PING') {
            $writer.WriteLine('ELEVATED')
            $server.Dispose()
            continue
        }

        if ($req -eq 'STOP') {
            $writer.WriteLine('0')
            Say "stop requested"
            $server.Dispose()
            break
        }

        $parsed = ConvertFrom-AgentRunRequest $req
        if ($null -eq $parsed) {
            Say "refused: unrecognised request"
            $writer.WriteLine('REFUSED|unrecognised request')
            $server.Dispose()
            continue
        }

        $v = Test-AgentScriptAllowed $parsed.Script $AllowRoot
        if (-not $v.Ok) {
            Say ("refused: {0}: {1}" -f $v.Why, $parsed.Script)
            $writer.WriteLine('REFUSED|' + $v.Why)
            $server.Dispose()
            continue
        }
        $a = Test-AgentArgsOk $parsed.ArgList
        if (-not $a.Ok) {
            Say ("refused: {0}" -f $a.Why)
            $writer.WriteLine('REFUSED|' + $a.Why)
            $server.Dispose()
            continue
        }

        if (-not (Test-Path -LiteralPath $OutDir)) { $null = New-Item -ItemType Directory -Path $OutDir -Force }
        $base    = Join-Path $OutDir ((Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [IO.Path]::GetFileNameWithoutExtension($v.Full))
        $outFile = $base + '.out'
        $errFile = $base + '.err'

        Say ("running {0} {1}" -f $v.Full, ($parsed.ArgList -join ' '))
        $code = 1
        try {
            $p = Start-Process powershell -PassThru -WindowStyle Hidden `
                -RedirectStandardOutput $outFile -RedirectStandardError $errFile `
                -ArgumentList (Format-AgentLaunchArgs $v.Full $parsed.ArgList)
            # TOUCH THE HANDLE: without this, ExitCode is NULL after WaitForExit(ms) on a
            # Start-Process -PassThru object (Windows PowerShell 5.1) - found on the first run.
            $null = $p.Handle
            if ($p.WaitForExit($MaxRunMinutes * 60000)) {
                $code = $p.ExitCode
            } else {
                & "$env:SystemRoot\System32\taskkill.exe" /PID $p.Id /T /F | Out-Null
                $code = 124
                Say ("killed after {0} min: {1}" -f $MaxRunMinutes, $v.Full)
            }
        } catch {
            Say "run failed: $($_.Exception.Message)"
            $code = 1
        }

        Say ("ran {0} -> {1}" -f $v.Full, $code)
        $writer.WriteLine((Format-AgentRunReply $code $outFile $errFile))
        $server.Dispose()
        $lastActivity = Get-Date
    }
}
catch {
    Say "helper error: $($_.Exception.Message)"
}

Say "helper exiting"
exit 0
