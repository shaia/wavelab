#!/usr/bin/env bash
#
# Build the whole ThermoLab site — both language copies plus the JupyterLite labs.
#
# A thin wrapper over scripts/build_site.py that resolves the two tools which are not on PATH
# in a fresh shell: uv (installed under ~/.local/bin) and mystmd (node_modules/.bin, installed
# by npm). Everything else — stylesheets, quizzes, animations, MyST, JupyterLite — is staged
# by the Python script.
#
# Output lands in _site/, where /en/, /he/ and /lite/ share one origin. That shared origin is
# what makes the laboratory links work; `npx myst start` serves a single MyST project and has
# no /lite route, so lab links always 404 there.
#
# The POSIX counterpart of build.ps1; the two must stay in step.

set -euo pipefail

usage() {
    cat <<'EOF'
Usage: ./build.sh [options]

Options:
  -s, --serve        Serve _site/ over HTTP after a successful build.
  -p, --port PORT    Port for --serve (default 8000).
      --media        Always re-render the animations. By default they are rendered only when
                     missing, or older than the render scripts / thermolab sources.
      --no-media     Never render animations.
      --no-lite      Skip the JupyterLite bundle (module pages' /lite/ links will 404).
      --no-clean     Reuse content/<lang>/_build instead of rebuilding it. Faster, but MyST
                     reuses cached page ASTs and never evicts superseded content-hashed
                     images, so the site may ship stale or duplicated media.
      --base-path P  Path prefix the site will be served under, e.g. /thermolab for a GitHub
                     Pages project site. Defaults to the domain root, which is what a local
                     build wants; the published site sets it from the workflow.
  -h, --help         Show this help.

Examples:
  ./build.sh --serve
  ./build.sh --media --serve --port 8080
  ./build.sh --base-path /thermolab
EOF
}

cd "$(dirname "$0")"

serve=0
port=8000
build_args=()

while [ $# -gt 0 ]; do
    case "$1" in
        -s|--serve)   serve=1 ;;
        -p|--port)
            if [ $# -lt 2 ]; then
                echo "build.sh: $1 requires a port number" >&2
                exit 2
            fi
            port="$2"
            shift
            ;;
        --base-path)
            if [ $# -lt 2 ]; then
                echo "build.sh: $1 requires a path prefix" >&2
                exit 2
            fi
            build_args+=(--base-path "$2")
            shift
            ;;
        --media)      build_args+=(--media) ;;
        --no-media)   build_args+=(--no-media) ;;
        --no-lite)    build_args+=(--no-lite) ;;
        --no-clean)   build_args+=(--no-clean) ;;
        -h|--help)    usage; exit 0 ;;
        *)
            echo "build.sh: unknown option '$1'" >&2
            usage >&2
            exit 2
            ;;
    esac
    shift
done

if [ "$serve" -eq 1 ]; then
    build_args+=(--serve "$port")
fi

# Prefer an installed-but-unlinked uv over one on PATH only if PATH has none: a fresh shell on
# this project's usual Windows setup has uv under ~/.local/bin without PATH picking it up.
# The .exe candidate covers Git Bash, where $HOME maps to the Windows profile directory.
find_uv() {
    if command -v uv >/dev/null 2>&1; then
        command -v uv
        return 0
    fi
    local candidate
    for candidate in "$HOME/.local/bin/uv" "$HOME/.local/bin/uv.exe"; do
        if [ -x "$candidate" ]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done
    return 1
}

if ! uv_bin="$(find_uv)"; then
    echo "build.sh: uv not found on PATH or in ~/.local/bin — install it from https://docs.astral.sh/uv/" >&2
    exit 1
fi

# mystmd is a project-local npm dependency; build_site.py exits with a clear message if it is
# absent, but installing here means a fresh clone needs exactly one command.
if [ ! -d node_modules/.bin ]; then
    echo "=== npm install (mystmd not yet installed) ==="
    npm install
fi

# build_site.py shells out to uv to build the wheel JupyterLite serves to Pyodide, and cannot
# find uv itself: it runs inside the environment uv created, which does not contain uv.
export UV="$uv_bin"

# Empty-array expansion is written the long way so it survives `set -u` on bash < 4.4 (macOS
# still ships 3.2), where "${build_args[@]}" on an empty array counts as an unbound variable.
exec "$uv_bin" run python scripts/build_site.py ${build_args[@]+"${build_args[@]}"}
