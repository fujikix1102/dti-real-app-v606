# DTI catalog-level upstream pilot — executed result

## Outcome

The restore-safe experimental clone completed the catalog-level stage contract for permanent
5%, 10%, and 20% steps in H(z), centered at z = 0.934 with tanh width 0.03.

- Catalog realizations processed: 336
- Data objects processed: 1,044,211
- Random objects processed: 2,184,000
- Landy–Szalay correlation functions: 672
- Anisotropic BAO template fits: 84
- Compressed observables per condition: 13
- Pipeline exceptions: 0
- Application tests after installation: 85/85 passed
- Backend tests after installation: 1/1 passed

Every condition executed this ordered path:

1. Survey-shaped synthetic object catalog generation.
2. Known H(z) transition injection before fiducial coordinate conversion.
3. Transverse and radial coordinate dilation.
4. FFT-smoothed displacement-field reconstruction.
5. Landy–Szalay xi(s, mu) correlation estimation.
6. Anisotropic shifted-BAO template fitting with per-mu broadband nuisance terms.
7. Compression in the official DESI DR2 13-observable ordering.

## Recovery

| H(z) step | alpha RMSE | compressed-vector relative RMSE | QSO radial target | QSO radial recovered |
|---:|---:|---:|---:|---:|
| 5% | 2.363% | 2.537% | 0.95238 | 0.98975 |
| 10% | 4.334% | 4.928% | 0.90909 | 1.00888 |
| 20% | 4.006% | 4.920% | 0.83333 | 0.95539 |

The pipeline is operational, but recovery is not complete or monotonic. The broad QSO-like
radial response remains the largest blind spot. This reproduces the qualitative conclusion of
the earlier transfer surrogate: upstream mixing and compression can hide or alias a sharp
transition, especially in high-redshift broad-window observables.

## Claim boundary

This is an executed catalog-level control, not a DESI production rerun. The generated object
catalog and survey mask are deterministic synthetic controls. The environment did not contain
the official EZmock/Abacus catalogs, pyrecon, pycorr, desilike, or fitsio, and external package
and mock retrieval was unavailable during execution. Therefore `production_equivalent` is fixed
to `false` in every artifact.

The result demonstrates that the complete software stage boundary can run and that transition
recovery is tracer-dependent. It does not provide an observational DTI detection, exclusion,
Bayes factor, posterior probability, or DESI collaboration validation.

## Reproducibility

- Full result: `dti_catalog_pipeline_pilot.json`
- 5% condition: `dti_catalog_pipeline_pilot_amp005.json`
- 20% condition: `dti_catalog_pipeline_pilot_amp020.json`
- Aggregate JSON: `dti_catalog_pipeline_pilot_summary.json`
- Aggregate CSV: `dti_catalog_pipeline_pilot_summary.csv`
- Executable: `run_dti_catalog_pipeline_pilot.py`
- Aggregate builder: `summarize_dti_catalog_pipeline_pilot.py`
- Test contract: `test_dti_catalog_pipeline_pilot.py`

