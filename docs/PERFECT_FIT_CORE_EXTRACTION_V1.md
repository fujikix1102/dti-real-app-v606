# Perfect-fit core extraction V1

## Preserved public baseline

- Commit: `2ce17f3fe0e32cfd91b4929cee916dd5a59546f3`
- app.py SHA256: `8780324e11f3f926828c7c164253184553c6691cd77563df0285fd6b070d6bc5`
- Legacy public interface: human visual confirmation PASS

## Independent implementation

The following files were added only to the isolated perfect-fit clone:

- `dti_ui_v1/components/value_formatting.py`
- `dti_ui_v1/services/response_parser.py`
- `dti_ui_v1/services/locked_bao_client.py`
- `tests/test_perfect_fit_core_v1.py`

## Boundaries

- No canonical app modification
- No public update
- No backend modification
- No network request during testing
- No CLASS or AxiCLASS execution
- No likelihood recomputation
- No sampler, posterior, or MCMC execution
- No 30.06 reuse
- No paid-infrastructure activation

## Next implementation

Create a separate perfect-fit Streamlit entrypoint using these tested
modules, then compare its rendered locked BAO values and status states
against the preserved application.
