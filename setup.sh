#!/usr/bin/env bash
# chillar-reels setup — one command, idempotent, macOS + Linux.
#   ./setup.sh              install / verify everything
#   ./setup.sh --models     also pre-download the whisper model used for alignment
set -uo pipefail
cd "$(dirname "$0")"
ROOT="$(pwd)"
OS="$(uname -s)"
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN" tools
export PATH="$LOCAL_BIN:$PATH"

declare -a RESULTS=()
pass() { RESULTS+=("✅ $1"); echo "  ✅ $1"; }
fail() { RESULTS+=("❌ $1 — $2"); echo "  ❌ $1 — $2"; }
have() { command -v "$1" >/dev/null 2>&1; }
step() { echo; echo "▶ $1"; }
can_sudo() { have sudo && { sudo -n true 2>/dev/null || [ -t 0 ]; }; }

ver_ge() { [ "$(printf '%s\n%s\n' "$2" "$1" | sort -V | head -1)" = "$2" ]; }

# ---------------------------------------------------------------- ffmpeg
step "ffmpeg"
if ! have ffmpeg || ! have ffprobe; then
  if [ "$OS" = "Darwin" ] && have brew; then
    brew install ffmpeg
  elif have apt-get && can_sudo; then
    sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg
  elif have dnf && can_sudo; then
    sudo dnf install -y ffmpeg || sudo dnf install -y ffmpeg-free
  elif [ "$OS" = "Linux" ]; then
    echo "  no sudo — installing static ffmpeg build into $LOCAL_BIN"
    arch="$(uname -m)"; case "$arch" in x86_64) a=amd64;; aarch64) a=arm64;; *) a="";; esac
    if [ -n "$a" ]; then
      tmp="$(mktemp -d)"
      curl -fsSL --retry 3 --retry-delay 2 "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-${a}-static.tar.xz" -o "$tmp/ff.tar.xz" \
        && tar -xJf "$tmp/ff.tar.xz" -C "$tmp" \
        && cp "$tmp"/ffmpeg-*-static/ffmpeg "$tmp"/ffmpeg-*-static/ffprobe "$LOCAL_BIN/"
      rm -rf "$tmp"
    fi
  fi
fi
if have ffmpeg && have ffprobe; then
  pass "ffmpeg $(ffmpeg -version | head -1 | awk '{print $3}')"
  filters="$(ffmpeg -hide_banner -filters 2>/dev/null)"
  [[ "$filters" == *arnndn* ]] && pass "ffmpeg arnndn filter" || fail "ffmpeg arnndn filter" "denoise falls back to afftdn"
else
  fail "ffmpeg" "install manually (brew install ffmpeg / sudo apt install ffmpeg)"
fi

# ---------------------------------------------------------------- node
step "Node.js 22+"
if have node && ver_ge "$(node -v | tr -d v)" "22.0.0"; then
  pass "node $(node -v)"
else
  if [ "$OS" = "Darwin" ] && have brew; then brew install node@22; fi
  have node && ver_ge "$(node -v | tr -d v)" "22.0.0" && pass "node $(node -v)" \
    || fail "node 22+" "install via https://nodejs.org or nvm install 22"
fi

# ---------------------------------------------------------------- python / uv
step "Python 3.11+ (via uv)"
if ! have uv; then
  curl -LsSf https://astral.sh/uv/0.11.7/install.sh | sh     # pinned installer version
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
if have uv; then
  pass "uv $(uv --version | awk '{print $2}')"
  uv python find '>=3.11' >/dev/null 2>&1 || uv python install 3.12
  if uv sync --locked --quiet; then                          # uv.lock is law: fail, never re-resolve
    pass "python venv $(.venv/bin/python -V | awk '{print $2}') + deps"
  else
    fail "python deps" "uv sync failed (see output above)"
  fi
else
  fail "uv" "install from https://docs.astral.sh/uv/"
fi
PY="$ROOT/.venv/bin/python"

# ---------------------------------------------------------------- faster-whisper / stable-ts
step "faster-whisper + stable-ts (word timestamps / forced alignment)"
if [ -x "$PY" ] && "$PY" -c "import faster_whisper, stable_whisper" 2>/dev/null; then
  pass "faster-whisper $("$PY" -c 'import faster_whisper;print(faster_whisper.__version__)') / stable-ts $("$PY" -c 'import stable_whisper;print(stable_whisper.__version__)')"
  if [[ " $* " == *" --models "* ]]; then
    "$PY" -c "from faster_whisper import WhisperModel; WhisperModel('medium', device='cpu', compute_type='int8')" \
      && pass "whisper 'medium' model cached" || fail "whisper model" "download failed"
  fi
else
  fail "faster-whisper/stable-ts" "uv sync did not install them"
fi

# ---------------------------------------------------------------- Kokoro (synthetic test voice)
step "Kokoro TTS (synthetic test voice only)"
[ -x "$PY" ] && "$PY" -c "import kokoro_onnx, soundfile" 2>/dev/null \
  && pass "kokoro-onnx" || fail "kokoro-onnx" "optional; only needed for synthetic test voices"

# ---------------------------------------------------------------- HyperFrames + Chrome
step "HyperFrames + Chromium"
if have npm; then
  npm ci --silent --no-audit --no-fund >/dev/null 2>&1 && pass "hyperframes $(npx --no-install hyperframes --version 2>/dev/null | tail -1)" \
    || fail "hyperframes" "npm install failed"
  npx --no-install hyperframes browser ensure >/dev/null 2>&1 && pass "chrome for rendering ($(npx --no-install hyperframes browser path 2>/dev/null | tail -1 | xargs basename))" \
    || fail "chrome for rendering" "run: npx hyperframes browser ensure"
  npx --no-install hyperframes skills update >/dev/null 2>&1 && pass "HyperFrames Claude Code skills" \
    || fail "HyperFrames skills" "run: npx hyperframes skills update"
fi
if [ -x "$PY" ]; then
  "$PY" -m playwright install chromium >/dev/null 2>&1 && pass "playwright chromium (asset scraper)" \
    || fail "playwright chromium" "run: .venv/bin/python -m playwright install chromium"
fi

# ---------------------------------------------------------------- RNNoise model
step "RNNoise voice model"
RNN="tools/rnnoise/std.rnnn"
if [ ! -s "$RNN" ]; then
  mkdir -p tools/rnnoise
  curl -fsSL --retry 3 --retry-delay 2 "https://raw.githubusercontent.com/richardpl/arnndn-models/0fda24c46d78f0207d820bb970fbe85c1971b39c/std.rnnn" -o "$RNN" || rm -f "$RNN"
  echo "6b8943dc4a9b6b24425873992a44f29c0577503276456af46a8854774faeb294  $RNN" | sha256sum -c --quiet - || rm -f "$RNN"
fi
[ -s "$RNN" ] && pass "rnnoise model ($RNN)" || fail "rnnoise model" "denoise falls back to afftdn"

# ---------------------------------------------------------------- fonts
step "Brand fonts (OFL, Google Fonts)"
GF="https://raw.githubusercontent.com/google/fonts/e7db6ca603fd4862010383ff17ffd6cc4ffac1c0/ofl"   # pinned commit
fetch_font() { # dest url
  [ -s "brand/fonts/$1" ] || curl -fsSL --retry 3 --retry-delay 2 "$2" -o "brand/fonts/$1" || rm -f "brand/fonts/$1"
}
fetch_font "BricolageGrotesque[opsz,wdth,wght].ttf" "$GF/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf"
fetch_font "BricolageGrotesque-OFL.txt"   "$GF/bricolagegrotesque/OFL.txt"
fetch_font "Mukta-ExtraBold.ttf"          "$GF/mukta/Mukta-ExtraBold.ttf"
fetch_font "Mukta-Bold.ttf"               "$GF/mukta/Mukta-Bold.ttf"
fetch_font "Mukta-OFL.txt"                "$GF/mukta/OFL.txt"
fetch_font "JetBrainsMono[wght].ttf"      "$GF/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"
fetch_font "JetBrainsMono-OFL.txt"        "$GF/jetbrainsmono/OFL.txt"
for f in "BricolageGrotesque[opsz,wdth,wght].ttf" Mukta-ExtraBold.ttf "JetBrainsMono[wght].ttf"; do
  [ -s "brand/fonts/$f" ] && pass "font $f" || fail "font $f" "download failed"
done
if [ -x "$PY" ]; then
  "$PY" pipeline/lib/glyph_check.py && pass "glyph coverage (₹, Devanagari)" || fail "glyph coverage" "see output above"
fi

# ---------------------------------------------------------------- env
step ".env"
[ -f .env ] || cp .env.example .env
for k in FREESOUND_API_KEY PIXABAY_API_KEY PEXELS_API_KEY; do
  v="$(grep -E "^$k=" .env | cut -d= -f2-)"
  [ -n "$v" ] && pass "$k set" || fail "$k" "empty in .env (needed by fetch_assets.py)"
done

# ---------------------------------------------------------------- summary
echo; echo "════════ chillar-reels setup checklist ════════"
nfail=0
for r in "${RESULTS[@]}"; do echo "$r"; [[ "$r" == ❌* ]] && nfail=$((nfail+1)); done
echo "═══════════════════════════════════════════════"
[ "$nfail" -eq 0 ] && echo "All good. Next: /new-reel <topic>" || echo "$nfail item(s) need attention."
exit 0
