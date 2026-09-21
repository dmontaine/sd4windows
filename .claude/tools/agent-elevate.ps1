# agent-elevate.ps1 - the unelevated half of Claude Code's own elevation channel
#
# NOT sd-elevate.ps1.  That pair (sdb_ai/sd64/gplbld/sd-elevate.ps1 and
# sd-elevate-helper.ps1) is SD's OWN product plumbing - called from
# gpl.bp/elevate when an SD administrator session needs os.execute done
# elevated, keyed to "sd-elev-<logname>", and it only ever runs scripts SD
# writes into the data tree.  This pair exists so the coding-agent session
# itself can run a gplbld script elevated, without asking the owner to type it
# into his own terminal each time.  Same shape, copied on purpose (CLAUDE.md:
# "gplbld/sd-elevate.ps1 is the shape to copy"), separate code, separate pipe
# name, so the two can never be confused for one another.
#
# Modes:
#
#   -Start   launch the elevated helper.  THIS IS WHERE THE ONE UAC PROMPT
#            APPEARS, on the interactive desktop - a person has to click it.
#   -Run     hand a script to the helper, wait for it to finish, PRINT what it
#            wrote, and exit with its exit code.  -Script names a .ps1 file
#            directly inside <repo>\sdb_ai\sd64\gplbld; -ScriptArgs are its
#            arguments (plain words only - see agent-elevate-lib.ps1).
#   -Stop    tell the helper to exit.
#
# Exit codes - READ THE PRINTED OUTPUT AS WELL AS THE CODE:
#
#   0..N  -Run: the SCRIPT's own exit code (124 = killed at the time limit)
#   1     the operation failed, OR the reply had no evidence behind it
#   3     refused - by the allow-list (checked here AND by the helper)
#   5     not elevated / elevation refused, declined, or unavailable
#   9     no helper is running for this session - call -Start first
#
# A REPLY IS NOT A RESULT UNTIL THERE IS EVIDENCE.  Any process of this user can create a
# pipe with this name before the helper does and answer PING with ELEVATED; a caller that
# trusted the reply would then report "exit 0" for a script that never ran.  So -Run
# accepts a reply only if the two output files it names EXIST and were written after the
# request was sent, and it prints them.  Nothing is reported with nothing to show for it.
#
# Single-owner, deliberately simpler than sd-elevate's: it serves exactly one Claude Code
# session and lives until -Stop or its own idle timeout.
#
# Nothing here has been run as of the day it was written; see the checklist in
# PROJECT_STATUS.md before relying on it.

param(
    [switch]$Start,
    [switch]$Run,
    [switch]$Stop,
    [string]$Script = '',
    [string[]]$ScriptArgs = @(),
    [string]$PipeName = "claude-agent-elev-$($env:USERNAME)",
    [int]$IdleTimeoutMinutes = 60,
    [int]$MaxRunMinutes = 30,
    [string]$OutDir = (Join-Path $env:LOCALAPPDATA 'SD-verify\agent-elevate'),
    [string]$LogFile = (Join-Path $env:TEMP 'claude-agent-elevate.log')
)

$ErrorActionPreference = 'Stop'

. (Join-Path $PSScriptRoot 'agent-elevate-lib.ps1')

# <repo>\.claude\tools -> <repo>
$repoRoot  = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$allowRoot = Get-AgentAllowRoot $repoRoot

function Send-Request([string]$message, [int]$timeoutMs = 10000) {
    try {
        $c = New-Object System.IO.Pipes.NamedPipeClientStream('.', $PipeName, 'InOut')
        $c.Connect($timeoutMs)
        $w = New-Object IO.StreamWriter($c)
        $w.AutoFlush = $true
        $r = New-Object IO.StreamReader($c)
        $w.WriteLine($message)
        $reply = $r.ReadLine()
        $c.Dispose()
        return $reply
    } catch {
        return $null
    }
}

function Test-Helper {
    return ((Send-Request 'PING' 1500) -eq 'ELEVATED')
}

function Show-Tail([string]$label, [string]$path, [int]$lines) {
    Write-Host ("--- {0}: {1}" -f $label, $path)
    $text = @(Get-Content -LiteralPath $path -Tail $lines -ErrorAction SilentlyContinue)
    if ($text.Count -eq 0) { Write-Host '    (empty)' } else { $text | ForEach-Object { Write-Host ('    ' + $_) } }
}

try {
    if ($Start) {
        $elevated = ([Security.Principal.WindowsPrincipal](
            [Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole(
            [Security.Principal.WindowsBuiltInRole]::Administrator)
        if ($elevated) { Write-Host 'agent-elevate: this shell is already elevated - nothing to launch'; exit 0 }

        if (Test-Helper) { Write-Host 'agent-elevate: a helper is already serving'; exit 0 }

        $helper = Join-Path $PSScriptRoot 'agent-elevate-helper.ps1'
        if (-not (Test-Path -LiteralPath $helper)) { Write-Host "agent-elevate: no helper at $helper"; exit 1 }
        if (-not (Test-Path -LiteralPath $allowRoot -PathType Container)) {
            Write-Host "agent-elevate: the allowed directory does not exist: $allowRoot"; exit 1
        }

        # NOT $args - that is PowerShell's automatic variable, and assigning to it here left
        # the helper with no switches at all (found 21 Sep 2026, before it was ever run).
        $launchArgs = @('-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
                        '-File', "`"$helper`"", '-PipeName', $PipeName,
                        '-AllowRoot', "`"$allowRoot`"", '-OutDir', "`"$OutDir`"",
                        '-IdleTimeoutMinutes', $IdleTimeoutMinutes,
                        '-MaxRunMinutes', $MaxRunMinutes,
                        '-LogFile', "`"$LogFile`"")

        Write-Host 'agent-elevate: launching the elevated helper with:'
        Write-Host ('  powershell ' + ($launchArgs -join ' '))
        Write-Host '  A UAC prompt will appear on the desktop - it must be clicked.'

        try {
            Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList $launchArgs | Out-Null
        } catch {
            # Declined at the UAC prompt, or no interactive desktop to show it on.
            Write-Host 'agent-elevate: elevation was declined or could not be shown.'
            exit 5
        }

        # Generous: a human has to see and click the UAC prompt first.
        for ($i = 0; $i -lt 60; $i++) {
            if (Test-Helper) { Write-Host 'agent-elevate: helper is up and answered ELEVATED'; exit 0 }
            Start-Sleep -Milliseconds 1000
        }
        Write-Host 'agent-elevate: no helper answered within 60 s.'
        exit 5
    }

    if ($Run) {
        if ($Script -eq '') { Write-Host 'agent-elevate: -Run needs -Script'; exit 1 }

        # The same decisions the helper will take, taken here first for a fast, plain answer.
        $v = Test-AgentScriptAllowed $Script $allowRoot
        if (-not $v.Ok) { Write-Host ("agent-elevate: refused locally - {0}: {1}" -f $v.Why, $Script); exit 3 }
        $a = Test-AgentArgsOk $ScriptArgs
        if (-not $a.Ok) { Write-Host ("agent-elevate: refused locally - {0}" -f $a.Why); exit 3 }

        if (-not (Test-Helper)) { Write-Host 'agent-elevate: no helper is running - call -Start first'; exit 9 }

        Write-Host ("agent-elevate: running {0} {1}" -f $v.Full, ($ScriptArgs -join ' '))
        $sent  = Get-Date
        $reply = Send-Request (ConvertTo-AgentRunRequest $v.Full $ScriptArgs) 10000
        if ($null -eq $reply) { Write-Host 'agent-elevate: the helper gave no reply'; exit 1 }

        if ($reply.StartsWith('REFUSED|')) {
            Write-Host ("agent-elevate: refused by the helper - {0}" -f $reply.Substring(8))
            exit 3
        }

        $parts = $reply -split '\|', 3
        $code = 0
        if ($parts.Count -ne 3 -or -not [int]::TryParse($parts[0], [ref]$code)) {
            Write-Host ("agent-elevate: NO EVIDENCE - the reply was not <code>|<out>|<err>: '{0}'" -f $reply)
            exit 1
        }
        $outFile = $parts[1]; $errFile = $parts[2]
        foreach ($f in $outFile, $errFile) {
            $fresh = (Test-Path -LiteralPath $f) -and ((Get-Item -LiteralPath $f).LastWriteTime -ge $sent.AddSeconds(-5))
            if (-not $fresh) {
                Write-Host ("agent-elevate: NO EVIDENCE - {0} does not exist or predates the request. This is not a result." -f $f)
                exit 1
            }
        }

        Show-Tail 'stdout (last 60 lines)' $outFile 60
        Show-Tail 'stderr (last 30 lines)' $errFile 30
        Write-Host ("agent-elevate: script exit code {0}{1}" -f $code, $(if ($code -eq 124) { ' (killed at the time limit)' } else { '' }))
        exit $code
    }

    if ($Stop) {
        if (-not (Test-Helper)) { Write-Host 'agent-elevate: nothing to stop'; exit 0 }
        Send-Request 'STOP' 5000 | Out-Null
        Write-Host 'agent-elevate: stop sent'
        exit 0
    }

    Write-Host 'agent-elevate: give one of -Start, -Run, -Stop'
    exit 1
}
catch {
    Write-Host ("agent-elevate: error - {0}" -f $_.Exception.Message)
    exit 1
}
