#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "== DTI app Section 7c continuity examiner local run =="
echo "app=$APP_DIR"
echo "url=http://localhost:8503"
echo "boundary=local_only_experimental_noncanonical"
echo "github_push=NO"
echo "render_deploy=NO"
echo "streamlit_public_update=NO"
echo

cd "$APP_DIR"
streamlit run app.py --server.port 8503
