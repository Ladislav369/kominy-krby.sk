#!/usr/bin/env bash
# Simple FTP deploy via curl. Reads credentials from .env.
# Note: uses plain FTP because Websupport's TLS data channel drops mid-upload
# on per-domain agentftp.<domain> accounts (control channel works, data channel 450).
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -f .env ]]; then
  echo "Missing .env (copy .env.example → .env and fill it in)." >&2
  exit 1
fi

set -a; source .env; set +a

: "${FTP_HOST:?FTP_HOST not set}"
: "${FTP_USER:?FTP_USER not set}"
: "${FTP_PASS:?FTP_PASS not set}"
: "${FTP_REMOTE_DIR:=/web/}"
: "${LOCAL_DIR:=.}"

# Ensure trailing slash on remote dir.
[[ "${FTP_REMOTE_DIR}" != */ ]] && FTP_REMOTE_DIR="${FTP_REMOTE_DIR}/"

# Files to skip from the local dir (repo metadata, env, scripts).
EXCLUDES=(.git .gitignore .env .env.example deploy.sh README.md .DS_Store node_modules .backups)

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
