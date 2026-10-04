#!/bin/bash
# SessionStart hook for Claude Code on the web: prepares the motion design environment at every cloud session.
#   1. Guardrails of AGENTS.md: empty .env at the root, telemetry off, pinned versions and audited commit checked,
#      HYPERFRAMES_SKILL_BOOTSTRAP_DEPS never set.
#   2. npm ci (HyperFrames pinned by package-lock.json), skipped when node_modules already matches the lockfile.
#   3. Render browser: the chrome-headless-shell pinned by HyperFrames (npx hyperframes browser ensure), with the
#      headless shell pre-installed in the cloud image as fallback.
#   4. Python Playwright for the styleframes (render-styleframes.py), pinned to the version of the Chromium
#      pre-installed in the cloud image (/opt/pw-browsers), so no browser download.
#   5. Network check: cdn.jsdelivr.net (GSAP and fonts) must be reachable for the renders.
# Idempotent and non-interactive. Logs go to stderr; the short summary on stdout is what Claude reads at startup.
# Local sessions are left alone: the install there follows the prompt of README.md.
set -euo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
cd "$ROOT"

# Same values as .claude/settings.json, so every command below already runs with telemetry off.
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1
unset HYPERFRAMES_SKILL_BOOTSTRAP_DEPS
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'unset HYPERFRAMES_SKILL_BOOTSTRAP_DEPS' >> "$CLAUDE_ENV_FILE"
fi

AUDITED_COMMIT=93ab289
PW_PY_VERSION=1.56.0 # Chromium build 1194 (Chrome 141), the one pre-installed in /opt/pw-browsers

log() { echo "[session-start] $*" >&2; }
WARNINGS=()
warn() { WARNINGS+=("$*"); log "WARNING: $*"; }

# 1. Guardrails ---------------------------------------------------------------------------------------------------
if [ ! -f .env ]; then
  cp .env.example .env
  log ".env created from .env.example (empty on purpose, never write a key in it)"
fi
if grep -qvE '^[[:space:]]*(#|$)' .env; then
  warn ".env holds something other than comments: AGENTS.md wants it empty (no key, ever)"
fi

HF_VERSION="$(node -p "require('./package.json').devDependencies.hyperframes")"
CORE_VERSION="$(node -p "require('./package.json').devDependencies['@hyperframes/core']")"
[[ "$HF_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || warn "hyperframes is not pinned to an exact version in package.json ($HF_VERSION)"
[ "$CORE_VERSION" = "$HF_VERSION" ] || warn "@hyperframes/core ($CORE_VERSION) differs from hyperframes ($HF_VERSION)"
grep -q "$AUDITED_COMMIT" .claude/skills/AUDITED_COMMIT.txt || warn "the HeyGen skills are not the audited commit $AUDITED_COMMIT"

# 2. npm ci -------------------------------------------------------------------------------------------------------
LOCK_SUM="$(sha256sum package-lock.json | cut -d' ' -f1)"
STAMP=node_modules/.motion-design-lock.sha256
if [ -f "$STAMP" ] && [ "$(cat "$STAMP")" = "$LOCK_SUM" ] && [ -f node_modules/hyperframes/package.json ]; then
  log "npm: node_modules already matches package-lock.json"
else
  log "npm ci (HyperFrames $HF_VERSION pinned by package-lock.json)"
  npm ci --no-audit --no-fund --loglevel=error >&2
  echo "$LOCK_SUM" > "$STAMP"
fi
INSTALLED="$(node -p "require('./node_modules/hyperframes/package.json').version")"
if [ "$INSTALLED" != "$HF_VERSION" ]; then
  log "ERROR: node_modules has hyperframes $INSTALLED, package.json pins $HF_VERSION"
  exit 1
fi

npx hyperframes telemetry disable >/dev/null 2>&1 || warn "npx hyperframes telemetry disable failed (the env vars still keep telemetry off)"

# 3. Render browser -----------------------------------------------------------------------------------------------
if npx hyperframes browser ensure >/dev/null 2>&1; then
  BROWSER="$(npx hyperframes browser path 2>/dev/null | tail -n 1)"
else
  FALLBACK="$(ls -d /opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell 2>/dev/null | sort -V | tail -n 1 || true)"
  if [ -n "$FALLBACK" ] && [ -x "$FALLBACK" ]; then
    BROWSER="$FALLBACK (fallback, HYPERFRAMES_BROWSER_PATH)"
    [ -z "${CLAUDE_ENV_FILE:-}" ] || echo "export HYPERFRAMES_BROWSER_PATH=\"$FALLBACK\"" >> "$CLAUDE_ENV_FILE"
    warn "npx hyperframes browser ensure failed, renders use the pre-installed headless shell $FALLBACK"
  else
    BROWSER="missing"
    warn "no render browser: npx hyperframes browser ensure failed and no fallback in /opt/pw-browsers"
  fi
fi

# 4. Python Playwright (styleframes) ------------------------------------------------------------------------------
if ! python3 -c "import playwright" >/dev/null 2>&1; then
  log "pip install playwright==$PW_PY_VERSION (styleframes)"
  python3 -m pip install --quiet --disable-pip-version-check --root-user-action=ignore "playwright==$PW_PY_VERSION" >&2 ||
    warn "pip install playwright failed: render-styleframes.py will not run"
fi
if timeout 60 python3 - >/dev/null 2>&1 <<'EOF'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    p.chromium.launch().close()
EOF
then
  PLAYWRIGHT="ok ($(python3 -c 'from importlib.metadata import version; print(version("playwright"))'))"
else
  PLAYWRIGHT="not working"
  warn "Python Playwright cannot launch Chromium: render-styleframes.py will not run"
fi

# Network: every sequence loads GSAP from cdn.jsdelivr.net (as HyperFrames does), and so do the fonts of
# new-project.sh --fonts. A cloud environment whose network policy blocks that host cannot render the films.
CDN_STATUS="$(curl -s -o /dev/null --max-time 10 -w '%{http_code}' https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js || true)"
if [ "$CDN_STATUS" = "200" ]; then
  CDN="reachable"
else
  CDN="BLOCKED"
  warn "cdn.jsdelivr.net is blocked by the network policy of this environment (GSAP of every sequence and the fonts load from it, so renders fail with sub_timeline_script_failure). Tell the user to add cdn.jsdelivr.net to the allowed domains of the environment (Network access: Custom), do not route around it"
fi

# Summary for Claude ----------------------------------------------------------------------------------------------
if python3 -c "import whisper" >/dev/null 2>&1; then
  WHISPER="installed"
else
  WHISPER="not installed (needed by mots.py and onsets.py at the voice step: a big download with torch, ask the user before installing it)"
fi

echo "Motion design environment ready (SessionStart hook):"
echo "- HyperFrames $INSTALLED (npm ci, pinned), telemetry off, .env at the root, HeyGen skills at audited commit $AUDITED_COMMIT"
echo "- Render browser: $BROWSER; cdn.jsdelivr.net (GSAP, fonts): $CDN"
echo "- ffmpeg: $(command -v ffmpeg >/dev/null && echo present || echo MISSING); Python Playwright (styleframes): $PLAYWRIGHT"
echo "- openai-whisper: $WHISPER"
echo "- Guardrails: AGENTS.md (no feedback, publish, cloud, upgrade, skills update; media-use --local-only; nothing leaves the machine)"
for w in "${WARNINGS[@]+"${WARNINGS[@]}"}"; do
  echo "- WARNING: $w"
done
