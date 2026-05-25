#!/usr/bin/env bash
set -euo pipefail

echo "== DTI app Section 8d clone local run =="
echo "app=/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_REAL_APP_SECTION8D_LIVE_VANILLA_CLONE_20260525_110229/dti-real-app-v606-section8d-live-vanilla"
echo "url=http://localhost:8502"
echo "boundary=local_only_experimental_noncanonical"
echo "github_push=NO"
echo "render_deploy=NO"
echo "streamlit_public_update=NO"
echo

cd "/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_REAL_APP_SECTION8D_LIVE_VANILLA_CLONE_20260525_110229/dti-real-app-v606-section8d-live-vanilla"
streamlit run app.py --server.port 8502
