# DTI application refactor architecture V1

## Objective

Preserve every existing function of `app.py` while moving the code into
smaller modules, removing genuine duplication, and retaining exact rollback.

This commit does not activate the modular application and does not remove
legacy code.

## Frozen runtime sources

- Frontend commit before scaffold: `e25fa18bcf64940afe93fadfa841965f226f809d`
- `app.py` SHA256: `6f4e208b35e494d7a26d61ff020d5651f9e767f28f26834357b53255aae6775f`
- `simple_app.py` SHA256: `230fb0cf1fb2e8b06538348e83d56f5362815a9dee37aa532dfac4bf5fd11f14`
- Backend commit: `81fdd064e472b0de9b850065f93976ed217edf13`
- Backend physical BAO SHA256: `fec91dd7f48d2e9aeab0b904ac2943d413d8320b6de1e963f81a25dd89c036f8`

## Required migration invariants

1. No legacy function may disappear without a preservation record.
2. Inputs must be counted before and after migration.
3. Outputs and display surfaces must be counted before and after migration.
4. Numeric precision must not regress.
5. Claim boundaries and provenance text must remain available.
6. Backend requests and scientific calculations must not change implicitly.
7. `app.py` remains the rollback source until migration is fully verified.
8. The current public simple entrypoint remains operational.
9. 30.06 remains forbidden.
10. Paid infrastructure remains forbidden.

## Target structure

```text
dti_ui_v1/
├── components/
│   ├── formatting.py
│   ├── status.py
│   ├── identity.py
│   ├── boundary.py
│   ├── inputs.py
│   └── layout.py
├── contracts/
│   └── preservation.py
├── pages/
│   ├── physical_bao.py
│   ├── source_identity.py
│   ├── fixed_h0_audit.py
│   ├── route_ab.py
│   ├── desi_dr2.py
│   ├── planck.py
│   └── legacy_workspace.py
└── services/
    ├── api_client.py
    ├── data_access.py
    ├── response_parser.py
    └── provenance.py
```

## Migration sequence

The sequence is functional rather than gate-based:

1. Extract shared pure functions and formatting utilities.
2. Extract API and file-access services.
3. Extract repeated display components.
4. Move low-dependency pages first.
5. Move high-density audit sections after shared components stabilize.
6. Compare feature manifests and input/output counts.
7. Activate the modular workspace only after zero-loss verification.
8. Retain the pre-refactor Git bundle and frozen source copies.

## Current activation state

- New modular package imported by public runtime: **NO**
- Legacy code removed: **NO**
- Backend changed: **NO**
- Public entrypoint changed: **NO**
- Rollback snapshot available: **YES**
