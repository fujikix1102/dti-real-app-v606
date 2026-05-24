# DTI-Core Grand Auditor v6.0.6

Researcher-facing Streamlit app for cosmological parameter-profile auditing, comparison, search, and sandbox exploration.

## Current fixed app version

```
v6.0.6-presets-expanded-inline
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app from this GitHub repository.
4. Set the main file path to:

```
app.py
```

5. Deploy.

## Included data

```
app/data/profile_presets_v606.tsv
app/data/axiclass_fix1_results.tsv
app/data/axiclass_fix1_delta.tsv
```

The profile preset table contains 100 parameter-profile cartridges.

## Boundary

This app is for parameter-profile audit/search/sandbox use.

It is not:

- a likelihood evaluation
- a posterior comparison
- a Planck likelihood validation
- an S8-tension solution proof
- a final cosmological validation
- a source-validation claim

AxiCLASS FIX1 values are fixed locked benchmark/reference values. Live CLASS/AxiCLASS sandbox calculations, when available, are exploratory and non-canonical.

## Source freeze identity

Source app:

```
/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_REAL_APP_V606_PRESETS_EXPANDED_INLINE_20260524_125234
```

Source audit:

```
/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_REAL_APP_V606_INLINE_AUDIT_20260524_125603
```

Freeze ZIP:

```
/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_REAL_APP_V606_INLINE_FREEZE_ZIP_20260524_125839/dti_real_app_v606_inline_freeze_20260524_125839.zip
```

Freeze ZIP SHA256:

```
3b9441f440166f3a3edce0f910d9c5100be8123e534558e9ec803829b78f8d5d
```
