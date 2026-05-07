#!/usr/bin/env bash
# Simple FTP deploy via curl. Credentials resolution order:
#   1. Existing env vars (CI / one-off override)
#   2. .env file in this dir (legacy / portability)
#   3. macOS Keychain entry: service=aresLab/kominy-krby.sk/ftp, account=kominy-krby.sk
# Note: uses plain FTP because Websupport's TLS data channel drops mid-upload
# on per-domain agentftp.<domain> accounts (control channel works, data channel 450).
set -euo pipefail

cd "$(dirname "$0")"

# .env is optional now — falls back to Keychain.
if [[ -f .env ]]; then
  set -a; source .env; set +a
fi

: "${FTP_HOST:=agentftp.kominy-krby.sk}"
: "${FTP_USER:=agentftp.kominy-krby.sk}"
: "${FTP_REMOTE_DIR:=/kominy-krby.sk/web/}"
: "${LOCAL_DIR:=.}"

# Pull password from Keychain if not already in env.
if [[ -z "${FTP_PASS:-}" ]]; then
  if ! FTP_PASS=$(security find-generic-password \
        -s "aresLab/kominy-krby.sk/ftp" -a "${FTP_USER}" -w 2>/dev/null); then
    cat >&2 <<HINT
FTP_PASS not in env, .env, or macOS Keychain.
To save it once into Keychain (password will be prompted if -w omitted):
  security add-generic-password -s 'aresLab/kominy-krby.sk/ftp' \\
                                -a '${FTP_USER}' -U -w
HINT
    exit 1
  fi
fi

# Ensure trailing slash on remote dir.
[[ "${FTP_REMOTE_DIR}" != */ ]] && FTP_REMOTE_DIR="${FTP_REMOTE_DIR}/"

# Files to skip from the local dir (repo metadata, env, scripts).
EXCLUDES=(.git .gitignore .env .env.example deploy.sh README.md CLAUDE.md .DS_Store node_modules .backups)

upload() {
  local local_path="$1"
  local rel="${local_path#${LOCAL_DIR}/}"
  echo "  → ${rel}"
  curl --fail --ftp-create-dirs \
       --user "${FTP_USER}:${FTP_PASS}" \
       --upload-file "${local_path}" \
       "ftp://${FTP_HOST}${FTP_REMOTE_DIR}${rel}"
}

should_skip() {
  local p="$1"
  for ex in "${EXCLUDES[@]}"; do
    [[ "${p}" == *"/${ex}" || "${p}" == *"/${ex}/"* ]] && return 0
  done
  return 1
}

echo "Deploying ${LOCAL_DIR} → ftp://${FTP_HOST}${FTP_REMOTE_DIR}"
while IFS= read -r -d '' f; do
  should_skip "${f}" && continue
  upload "${f}"
done < <(find "${LOCAL_DIR}" -type f -print0)

echo "Done."
