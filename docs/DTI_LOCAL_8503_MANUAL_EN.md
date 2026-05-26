# DTI local 8503 app Manual

## 0. What this Manual is for

This Manual explains how to operate the local DTI 8503 app safely.

The app is a local helper interface for:

- inspecting parameter profiles
- comparing Candidate and Reference inputs
- running local AxiCLASS / vanilla CLASS helper checks
- checking local response behavior in the continuity examiner
- preserving clear interpretation boundaries

The app is not a likelihood engine.
The app is not a posterior comparison tool.
The app is not a Planck validation tool.
The app does not update manuscript values.
The app does not prove physical discontinuity, physical continuity, or an operator-phase transition.

Example:

If the app shows a local probe output, read it as:

"These are local derived quantities from the current input payload."

Do not read it as:

"This model is statistically preferred by Planck."

---

## 1. Current accepted app state

The current local app state includes:

- README download button
- English Manual PDF download button
- README and Manual controls before "2. Current profile status" in the left sidebar
- red RUN / probe buttons
- highlighted 7a / 7b / 7c Enable controls
- local 8011 endpoint for the 7b vanilla CLASS live probe
- softened 8011 unavailable guidance
- visible 7c continuity / discontinuity examiner
- visible Section 8 boundary confirmation
- graph rendering disabled

Current fixed GitHub commit used as the base line:

af1a7fcc4d823bb73692138e12323c8a83c20369

Example:

If you see a red RUN button, treat it as an execution button.
If you see a yellow Enable notice, turn it on only when you intentionally want to run that section.

---

## 2. Starting the local 8503 app

Use Bash.

Command:

cd "/Users/fujikijunichi/Desktop/MAXOMEGA/_paper_journal/paper_20260305_102018_audit_sensitivity/_DTI_SECTION7C_CONTINUITY_EXAMINER_CLONE_20260525_124307/dti-real-app-v606-section7c-continuity-examiner"

python3 -m streamlit run app.py --server.port 8503 --server.address 127.0.0.1

Open:

http://localhost:8503

Example:

If the browser does not open automatically, copy this URL into Safari or Chrome:

http://localhost:8503

---

## 3. Main safety boundaries

This app does not provide:

- likelihood evaluation
- posterior comparison
- Planck validation
- MCMC sampling
- evidence calculation
- manuscript-value update
- physical-discontinuity proof
- operator-phase transition proof

Use this interpretation rule:

Local app output = local diagnostic output.
Audited likelihood claim = only from a proper audited likelihood pipeline.

Example of safe wording:

"The local probe returned a derived parameter payload for the current input."

Example of unsafe wording:

"The local probe proves this branch is preferred by Planck."

---

## 4. Screen overview

The left sidebar is the operation entrance.

It contains:

- profile selection
- README / Manual downloads
- current profile status
- Candidate / Reference controls
- profile text
- Apply text to form controls

The main area contains:

- DTI-Core Grand Auditor title
- Candidate / Reference input form
- 7a local fixed-example check
- 7b local vanilla CLASS live probe
- 7c continuity / discontinuity examiner
- Section 8 boundary confirmation

Example workflow:

1. Select a registered profile in the sidebar.
2. Check "2. Current profile status".
3. Confirm Candidate / Reference values.
4. Enable only the section you want to run.
5. Press the relevant red RUN / probe button.
6. Read the output inside the stated boundary.

---

## 5. Before pressing a red RUN / probe button

Check these five items:

1. intended profile
2. current input values
3. relevant Enable checkbox
4. local 8011 status, if using 7b
5. interpretation boundary

Example:

Before running 7b, check:

- Did I select the intended profile?
- Did I load or type the intended values?
- Is the 7b Enable checkbox active?
- Is local 8011 running?
- Am I interpreting the output as local diagnostic output only?

---

## 6. Left sidebar usage

Use the sidebar to choose and inspect the current profile.

The sidebar is for:

- choosing the profile
- loading presets
- checking current profile status
- downloading README / Manual
- confirming profile text
- applying profile text to form inputs

The sidebar is not a likelihood interface.

Example:

If the sidebar says Active profile = FUJIKI DTI working reference, it means the app is currently inspecting that profile.

It does not mean the profile is validated or preferred.

---

## 7. Parameter profile cartridge

A profile is a parameter cartridge.

It can contain values such as:

- H0
- omega_cdm
- omega_b
- fEDE
- S8
- rs_drag

A profile does not automatically mean:

- true model
- preferred model
- validated model
- accepted manuscript value

Example:

A profile can be useful for testing input behavior even if it is not a final physics claim.

---

## 8. README / Manual download area

README is the short guide.
Manual is the full guide.

Markdown Manual is the documentation source-of-record.
PDF Manual is a generated distribution copy.

Example:

Use README when you only need startup reminders.
Use Manual when you need operational boundaries and examples.

---

## 9. Current profile status

Current profile status is only a display of the current selection.

It should not be read as validation.

Active profile means the selected or loaded profile.
Reference means the comparison baseline.
Displayed difference is descriptive, not likelihood preference.

Example:

Safe reading:

"The current profile has a higher H0 than the reference."

Unsafe reading:

"The current profile is statistically better than the reference."

---

## 10. Candidate / Reference input

Candidate is the profile being inspected.
Reference is the comparison baseline.

Neither label implies correctness.

Example:

Candidate:
A DTI working-reference region.

Reference:
A Planck-like baseline or registered comparison profile.

Safe interpretation:

"The app compares the input values as a local profile comparison."

Unsafe interpretation:

"The app has performed posterior model comparison."

---

## 11. +/- buttons and direct numeric input

Use direct numeric typing when exact values matter.
Use +/- buttons for small exploratory adjustments.

Example:

For a recorded check, type:

H0 = 72.0

For a quick sensitivity check, use +/-.

Rule:

If the value will be cited, recorded, or compared later, type it directly.

---

## 12. 7a Enable and Run

7a is the local-only AxiCLASS fixed-example check.

It is disabled by default.
Enable 7a intentionally.
Then press the red Run button.

Example:

Use 7a when you want to confirm that a fixed local example still runs.

Do not use 7a output as a Planck validation result.

Safe wording:

"7a fixed-example check completed."

Unsafe wording:

"7a proves this model is preferred."

---

## 13. 7b Enable and local vanilla CLASS live probe

7b sends current input parameters to the local vanilla CLASS live derived-parameter endpoint.

Endpoint:

http://127.0.0.1:8011/axiclass/live-vanilla-probe

7b does not compute:

- likelihood
- posterior
- Planck validation
- manuscript values

Example:

If 7b returns derived quantities, read them as local derived quantities from the current input payload.

Do not read them as statistical preference.

---

## 14. 8011 unavailable notice

If local 8011 is not running, the app shows a softened unavailable notice.

This is not a physics failure.
It only means the local endpoint is unavailable.

Check 8011 with:

lsof -tiTCP:8011 -sTCP:LISTEN

Example:

No output from lsof means local 8011 is not listening.

Correct response:

Start or restart the local 8011 API, then try 7b again.

Incorrect response:

Changing physics values because the endpoint was unavailable.

---

## 15. 7c continuity / discontinuity examiner

7c inspects local numerical response behavior across a sweep.

It does not prove:

- physical continuity
- physical discontinuity
- operator-phase transition

Example:

Safe wording:

"7c shows a local numerical response pattern under this sweep."

Unsafe wording:

"7c proves a physical phase transition."

---

## 16. Section 8 usage

Section 8 is a candidate payload and boundary-confirmation area.

It is not a result-claim section.

Example:

Use Section 8 to confirm what the app did and did not do.

Do not use Section 8 as a substitute for an audited likelihood table.

---

## 17. Boundary table reading

Boundary tables explain what the app did not do.

Important boundaries:

- likelihood evaluation = NO
- posterior comparison = NO
- Planck validation = NO
- physics-value update = NO
- manuscript update = NO
- graph rendering reopened = NO

Example:

If likelihood evaluation = NO, the app did not compute likelihood.
If Planck validation = NO, the app did not validate against Planck.

---

## 18. Boundary confirmation reading

Boundary confirmation prevents over-interpretation.

If the app says local-only, exploratory, not likelihood, not posterior, not Planck validation, and not manuscript value, keep the interpretation inside that boundary.

Example:

Safe:

"This is a local diagnostic result."

Unsafe:

"This is a final cosmological inference."

---

## 19. Graph rendering disabled

Graph rendering is intentionally disabled in the current freeze.

No fake graph is allowed.
No fallback graph is allowed.
No illustrative graph is allowed.
No synthetic graph is allowed.
No fixed-reference substitute graph is allowed.

Any graph must come from:

- real measured output, or
- an explicit audited source TSV

Example:

If no compatible real output exists, show no graph.

Do not draw a placeholder curve.

---

## 20. README / Manual / source-of-record management

README is the short practical guide.
Manual is the full operating guide.

Markdown Manual is the source-of-record.
PDF Manual is generated from Markdown.

Example:

Edit the Markdown first.
Generate the PDF second.
Commit both only after checking SHA and display.

---

## 21. Common failures and responses

Problem:

PDF shows square boxes.

Response:

Use English-only Manual PDF.

Problem:

8011 connection refused.

Response:

Local 8011 API is not running.

Problem:

RUN appears to do nothing useful.

Response:

Check the relevant Enable checkbox.

Problem:

A graph is expected but does not appear.

Response:

Graph rendering is intentionally disabled in this freeze.

---

## 22. Checking whether 8011 is running

Use:

lsof -tiTCP:8011 -sTCP:LISTEN

Example:

If the command returns a process ID, 8011 is listening.
If the command returns nothing, 8011 is not listening.

---

## 23. GitHub reflection checklist

Before committing or pushing, run:

python3 -m py_compile app.py
git status --short
git diff --stat
git diff --name-only

Stage exact files only.

Example:

If only these are intended:

app.py
docs/README_DTI_LOCAL_8503.md
docs/DTI_LOCAL_8503_MANUAL_EN.md
docs/DTI_LOCAL_8503_MANUAL_EN.pdf

then do not stage unrelated audit folders or output ZIPs.

---

## 24. Freeze / pointer / handoff concept

A freeze is an accepted state.
A pointer records the identity of that state.
A handoff package preserves the route back to that state.

A pointer should include:

- SHA256 values
- Git commit
- branch
- remote
- boundary status
- handoff ZIP, if present

Example:

If app.py SHA changes, it is a new app state.
If Manual PDF SHA changes, it is a new documentation distribution state.

---

## 25. Future graph Strategy A / B safety rules

Strategy A reduces multidimensional variation to a single theoretical path parameter.

Example:

Define t from 0 to 1.
Move H0 and omega_cdm together along a predefined path.
Plot output against t.

Strategy B uses scatter plots and color maps for multidimensional points.

Example:

Plot rs_drag vs S8 as points.
Use color to represent stress or distance.

Both strategies require real measured output or explicit audited source TSV.

No fake, fallback, illustrative, synthetic, or invented graph is allowed.

---

## 26. Markdown Manual and PDF Manual

Use Markdown for editing.
Use PDF for distribution.

Current decision:

Use English-only PDF Manual for reliable rendering.

Example:

Do not edit the PDF directly.
Edit DTI_LOCAL_8503_MANUAL_EN.md.
Then regenerate DTI_LOCAL_8503_MANUAL_EN.pdf.

---

## 27. Final operating rule

This app is useful only if its boundaries remain visible.

Every local probe, profile comparison, and continuity check must preserve:

- source-of-record awareness
- local-only boundary
- no likelihood claim
- no posterior claim
- no Planck-validation claim
- no manuscript-value update
- no fake graph

If a future change weakens these boundaries, do not promote it.

---

## Safe / Unsafe examples quick reference

This section makes the operating boundary explicit before GitHub reflection.

### Safe example: local documentation download

Safe example:

    Open the local 8503 app.
    Click Download English Manual PDF.
    Use the PDF as an operating guide.
    Do not treat the PDF as a physics result.

Why this is safe:

    It is documentation only.
    It does not run a likelihood evaluation.
    It does not compare posteriors.
    It does not validate against Planck.
    It does not update manuscript values.

### Safe example: local 8011 probe availability check

Safe example:

    Enable local-only vanilla CLASS live probe.
    Run the local 8011 probe only when the local API server is running.
    Read the returned payload as a local diagnostic.
    Keep the result outside manuscript claims.

Allowed interpretation:

    The endpoint responded.
    The payload was produced by the local 8011 route.
    The output may be inspected as a local implementation check.

Not allowed interpretation:

    The model is validated by Planck.
    The posterior is preferred.
    The likelihood has been evaluated.
    The manuscript value is updated.

### Unsafe example: treating the app as a likelihood engine

Unsafe example:

    Run the local probe.
    Then claim that the result proves posterior preference.

Why this is unsafe:

    The app is not a likelihood engine.
    The app is not a posterior-comparison tool.
    The app is not a Planck-validation tool.

### Unsafe example: drawing or implying fallback graphs

Unsafe example:

    No source-of-record table is available.
    Draw a fallback graph anyway.
    Use it as a scientific figure.

Why this is unsafe:

    No fake graph is allowed.
    No fallback graph is allowed.
    No illustrative scientific-looking graph is allowed.
    If compatible source-of-record data are absent, the app must show a no-graph notice.

### Unsafe example: overstating 7c continuity output

Unsafe example:

    Run the 7c continuity examiner.
    Then claim that it proves physical discontinuity or an operator-phase transition.

Why this is unsafe:

    7c is a local numerical examiner.
    It may provide a bounded diagnostic.
    It does not prove physical continuity.
    It does not prove physical discontinuity.
    It does not prove an operator-phase transition.

