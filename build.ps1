<#
.SYNOPSIS
    Build the whole ThermoLab site — both language copies plus the JupyterLite labs.

.DESCRIPTION
    A thin wrapper over scripts/build_site.py that resolves the two tools which are not on
    PATH in a fresh shell: uv (installed under ~/.local/bin) and mystmd (node_modules/.bin,
    installed by npm). Everything else — stylesheets, quizzes, animations, MyST, JupyterLite
    — is staged by the Python script.

    Output lands in _site/, where /en/, /he/ and /lite/ share one origin. That shared origin
    is what makes the laboratory links work; `npx myst start` serves a single MyST project
    and has no /lite route, so lab links always 404 there.

.PARAMETER Serve
    Serve _site/ over HTTP after a successful build.

.PARAMETER Port
    Port for -Serve (default 8000).

.PARAMETER Media
    Always re-render the animation GIFs. By default they are rendered only when missing or
    older than the render scripts / thermolab sources.

.PARAMETER NoMedia
    Never render animations.

.PARAMETER NoLite
    Skip the JupyterLite bundle (module pages' /lite/ links will 404).

.PARAMETER NoClean
    Reuse content/<lang>/_build instead of rebuilding it. Faster, but MyST never evicts
    superseded content-hashed images, so the site may ship dead copies of re-rendered GIFs.

.PARAMETER BasePath
    Path prefix the site will be served under, e.g. /thermolab for a GitHub Pages project site.
    Defaults to the domain root, which is what a local build wants. The published site sets this
    from the workflow, so use it only to reproduce the deployed layout locally.

.EXAMPLE
    .\build.ps1 -Serve

.EXAMPLE
    .\build.ps1 -Media -Serve -Port 8080

.EXAMPLE
    .\build.ps1 -BasePath /thermolab
#>
[CmdletBinding()]
param(
    [switch]$Serve,
    [int]$Port = 8000,
    [switch]$Media,
    [switch]$NoMedia,
    [switch]$NoLite,
    [switch]$NoClean,
    [string]$BasePath
)

$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

$uv = Join-Path $env:USERPROFILE '.local\bin\uv.exe'
if (-not (Test-Path -LiteralPath $uv)) {
    $uv = (Get-Command uv -ErrorAction SilentlyContinue).Source
}
if (-not $uv) {
    throw "uv not found. Install it, or adjust this script's path to uv.exe."
}

# mystmd is a project-local npm dependency; build_site.py exits with a clear message if it is
# absent, but installing here means a fresh clone needs exactly one command.
if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot 'node_modules\.bin'))) {
    Write-Host '=== npm install (mystmd not yet installed) ===' -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -ne 0) { throw "npm install failed with exit code $LASTEXITCODE" }
}

# build_site.py shells out to uv to build the wheel JupyterLite serves to Pyodide, and cannot
# find uv itself: it runs inside the environment uv created, which does not contain uv.
$env:UV = $uv

$buildArgs = @()
if ($BasePath) { $buildArgs += '--base-path'; $buildArgs += $BasePath }
if ($Media)   { $buildArgs += '--media' }
if ($NoMedia) { $buildArgs += '--no-media' }
if ($NoLite)  { $buildArgs += '--no-lite' }
if ($NoClean) { $buildArgs += '--no-clean' }
if ($Serve)   { $buildArgs += '--serve'; $buildArgs += "$Port" }

& $uv run python scripts/build_site.py @buildArgs
exit $LASTEXITCODE
