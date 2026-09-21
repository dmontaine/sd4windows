# agent-elevate-lib.ps1 - the DECISIONS of Claude Code's own elevation channel, as pure
# functions with no side effects, so gplbld/test-agentelevate-units.ps1 can drive them
# without elevating anything.  Dot-sourced by agent-elevate.ps1 (the unelevated client)
# and agent-elevate-helper.ps1 (the elevated server): the client checks first for a fast
# answer and the SERVER CHECKS AGAIN, because the pipe can be reached by any process of
# this user and the server is the only place a refusal cannot be skipped.
#
# WHAT THE ALLOW-LIST IS FOR, STATED HONESTLY.  Once the helper is up, whatever it is
# handed runs with this user's ADMINISTRATOR rights.  The allow-list restricts that to
# .ps1 files that sit DIRECTLY in <repo>\sdb_ai\sd64\gplbld - the tracked, reviewable
# scripts - so a script dropped in %TEMP% or a downloads folder cannot be run through
# the pipe.  IT DOES NOT PROTECT AGAINST A COMPROMISED AGENT: a file written into
# gplbld runs like any other, exactly as the owner's own elevated shell would run it.
# It stops accidents and casual abuse of the pipe, not an adversary who can already
# write to the repo.
#
# NOTE ON -eq / -ne BELOW: PowerShell string comparison is case-INSENSITIVE by default,
# which is what Windows paths need.  Do not "fix" them to -ceq.

function New-AgentVerdict([bool]$Ok, [string]$Why, [string]$Full) {
    return @{ Ok = $Ok; Why = $Why; Full = $Full }
}

function Get-AgentAllowRoot([string]$RepoRoot) {
    return [IO.Path]::GetFullPath((Join-Path $RepoRoot 'sdb_ai\sd64\gplbld')).TrimEnd('\')
}

function Test-AgentScriptAllowed([string]$Path, [string]$AllowRoot) {
    if ([string]::IsNullOrWhiteSpace($Path)) {
        return (New-AgentVerdict $false 'no script path was given' '')
    }
    if ($Path -match '[\x00-\x1f]') {
        return (New-AgentVerdict $false 'the path contains control characters' '')
    }
    # THE NULL CASE, REFUSED OUT LOUD: with no allowed directory the only safe answer is
    # no, never "then everything is allowed".
    if ([string]::IsNullOrWhiteSpace($AllowRoot) -or -not (Test-Path -LiteralPath $AllowRoot -PathType Container)) {
        return (New-AgentVerdict $false 'the allowed directory does not exist - refusing everything' '')
    }
    try { $full = [IO.Path]::GetFullPath($Path) }
    catch { return (New-AgentVerdict $false 'not a valid path' '') }

    $root   = [IO.Path]::GetFullPath($AllowRoot).TrimEnd('\')
    $parent = [IO.Path]::GetDirectoryName($full)
    if ($null -eq $parent -or $parent.TrimEnd('\') -ne $root) {
        return (New-AgentVerdict $false 'the script is not directly inside the allowed directory' $full)
    }
    if ([IO.Path]::GetExtension($full) -ne '.ps1') {
        return (New-AgentVerdict $false 'only .ps1 files are run' $full)
    }
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        return (New-AgentVerdict $false 'no such file' $full)
    }
    # A link would let an allowed NAME point at a file anywhere.  (A file link inside the
    # directory needs elevation or developer mode to create, so this is a guard against
    # something an unprivileged process should not be able to plant.)
    $item     = Get-Item -LiteralPath $full -Force
    $rootItem = Get-Item -LiteralPath $root -Force
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        ($rootItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        return (New-AgentVerdict $false 'the script or its directory is a link' $full)
    }
    return (New-AgentVerdict $true '' $full)
}

# Arguments travel through Start-Process -ArgumentList, which joins them with spaces and
# does no quoting of its own, so anything that could split or inject is refused rather
# than escaped: a switch or value made of letters, digits and . , : = @ \ / _ -
function Test-AgentArgsOk([string[]]$ArgList) {
    foreach ($a in @($ArgList)) {
        if ([string]::IsNullOrEmpty($a)) { return @{ Ok = $false; Why = 'an empty argument was given' } }
        # \z, NOT $: in .NET a $ also matches just before a TRAILING NEWLINE, so "abc`n"
        # would pass a $-anchored check and split the command line.
        if ($a -notmatch '^[A-Za-z0-9_.,:=@\\/-]+\z') {
            return @{ Ok = $false; Why = ("argument '{0}' has characters outside the allowed set" -f $a) }
        }
    }
    return @{ Ok = $true; Why = '' }
}

# One request per line: a compact JSON object.  PING and STOP stay plain words.  There is
# deliberately NO "raw path" form any more, so nothing can be sent that skips the checks.
function ConvertTo-AgentRunRequest([string]$Script, [string[]]$ArgList) {
    return (@{ script = $Script; argv = @($ArgList) } | ConvertTo-Json -Compress)
}

function ConvertFrom-AgentRunRequest([string]$Line) {
    if ([string]::IsNullOrWhiteSpace($Line) -or -not $Line.TrimStart().StartsWith('{')) { return $null }
    try { $o = $Line | ConvertFrom-Json -ErrorAction Stop } catch { return $null }
    if ($null -eq $o -or -not ($o.PSObject.Properties.Name -contains 'script')) { return $null }
    return @{ Script = [string]$o.script; ArgList = @($o.argv | ForEach-Object { [string]$_ }) }
}

# A reply must NEVER carry an empty or non-numeric exit code.  Found on the very first run
# (21 Sep 2026): Start-Process -PassThru leaves ExitCode NULL after WaitForExit(ms) unless
# the process Handle was touched first, so the reply read "|<out>|<err>" - and a caller
# that read an empty code as "no error" would have reported a false green.  A missing or
# malformed code becomes 1 (failed), never 0.
function Format-AgentRunReply($ExitCode, [string]$OutFile, [string]$ErrFile) {
    $code = 1
    if ($null -ne $ExitCode -and ([string]$ExitCode) -match '^-?\d+\z') { $code = [int]$ExitCode }
    return ('{0}|{1}|{2}' -f $code, $OutFile, $ErrFile)
}

function Format-AgentLaunchArgs([string]$Full, [string[]]$ArgList) {
    return (@('-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-File', ('"' + $Full + '"')) + @($ArgList))
}
