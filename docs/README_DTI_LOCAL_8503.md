# DTI local 8503 app README

## Purpose

This is a local-only DTI / AxiCLASS / vanilla CLASS helper app.

It is an experimental local UI for checking parameter payloads, local fixed examples, local vanilla CLASS probe output, and continuity / discontinuity examiner behavior.

It is not a likelihood engine, not a posterior comparison, not a Planck validation tool, and not a manuscript-value update tool.

## Current accepted freeze

- app.py SHA256: `e9a8048d39cd423aaafbcd8df6f3fc3cdbb7168748be752d106c6d1db302d8e4`
- GitHub commit: `ef0c602a34e0fa6869bfb576a302281f58f04940`
- Branch: `main`

## Start the local 8503 app

    cd "/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_SECTION7C_CONTINUITY_EXAMINER_CLONE_20260525_124307/dti-real-app-v606-section7c-continuity-examiner"
    python3 -m streamlit run app.py --server.port 8503 --server.address 127.0.0.1

Open:

    http://localhost:8503

## 7a / 7b / 7c Enable gates

Some local operations are intentionally disabled until their Enable checkbox is turned on.

The Enable controls for 7a, 7b, and 7c are visually highlighted to reduce accidental failed runs.

## 7b local vanilla CLASS live probe

The 7b live probe sends a local request to:

    http://127.0.0.1:8011/axiclass/live-vanilla-probe

If the local 8011 API is not running, the app may show a connection-unavailable notice.

That is not a physics failure. It only means the local vanilla CLASS helper endpoint is offline.

## Boundary

This app does not perform:

- likelihood evaluation
- posterior comparison
- Planck validation
- manuscript-value update
- physics-value update
- proof of physical discontinuity
- proof of operator-phase transition

## Graph policy

Graph rendering remains closed in this freeze unless an explicit new experimental graph branch is created.

Do not use fake, synthetic, illustrative, fallback, or UI-reference graphs as scientific output.

If graph Strategy A or Strategy B is tested later, create a separate experimental clone or branch from this freeze.

## Safe update rule

Do not edit this freeze directly for speculative graph work.

For any new feature:

1. Create a backup.
2. Apply local-only patch.
3. Run py_compile.
4. Run static safety scan.
5. Restart only local 8503.
6. Confirm no deploy, no public Streamlit update, no manuscript update.
