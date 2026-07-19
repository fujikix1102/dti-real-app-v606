# MAXOMEGA / DTI — Hubble Tension Atlas

An auditable scientific workbench that lets a viewer change an early-dark-energy hypothesis, run AxiCLASS, and follow the same physical model through CMB spectra, the drag sound horizon, DESI DR2 BAO, Planck 2018, Pantheon+, and overlap-safe local-distance-ladder comparisons.

## Why it matters

The Hubble tension is often presented as a single pair of incompatible numbers. This application makes the model-to-observation chain inspectable: every submitted parameter, achieved EDE quantity, solver output, likelihood component, residual, and source-file identity remains visible.

## Evidence-bearing capabilities

- AxiCLASS axion-like EDE propagation with achieved `f_EDE` and `z_c` reported by the solver.
- Planck 2018 Plik-lite TTTEEE, Commander low-T, and SimAll low-E likelihoods through `clipy`.
- Pantheon+ supernova likelihood with the absolute-magnitude intercept analytically marginalized.
- Official DESI DR2 13-element BAO mean and covariance, explicitly labeled as a template-derived compressed product rather than raw clustering data.
- Seeded transition injection/recovery transfer audit: 10,000 null simulations and 72,000 injected realizations quantify when broad tracer windows and 13-value BAO compression can hide a sharp H(z) transition.
- Executed catalog-level upstream pilot: 336 catalog realizations, 672 Landy–Szalay correlation functions, and 84 anisotropic BAO fits propagate 5%, 10%, and 20% injected H(z) steps through coordinate conversion, FFT reconstruction, template fitting, and the 13-value layout. This pilot uses deterministic synthetic survey-shaped catalogs and is explicitly not labeled DESI-production-equivalent.
- Current-versus-previous Δχ², CMB spectra, BAO residuals, and a bilingual Hubble Tension Atlas.
- A Hubble Consistency Engine that distinguishes Pareto improvement from cross-dataset trade-offs and prevents SH0ES/CCHP summaries from being double-counted with Pantheon+.
- A finite-grid joint H₀ trade-off audit that follows all three installed backend likelihood components and records a hash-addressed result.
- Atomic run artifacts containing canonical SHA-256 identities, replay payloads, runtime versions, and scientific boundaries.

## Claim boundary

The General route evaluates deterministic likelihood coordinates at submitted parameter points. It does not claim a posterior, Bayes factor, discovery significance, or converged MCMC result. Published SH0ES/CCHP values are Gaussian summary comparisons only; because they overlap supernova information with Pantheon+, they are not included in the backend joint sum. A full reconciliation claim requires raw calibrator likelihoods and covariance, declared priors, a converged joint sampler, and model comparison. Audit-DTI smoothness is conditional on the seven-effective-redshift, 13-value DESI DR2 Gaussian compression and the scanned AxiCLASS family; it is not evidence that raw observations or the Universe are fundamentally continuous. The injection/recovery study is an independent DESI-like transfer surrogate, not a rerun of the production catalog, reconstruction, RascalC, desilike, or Ly-alpha pipelines. Planck calibration is fixed at `A_planck = 1.0` in this interactive view. The isolated transition sandbox is a mathematical diagnostic and is not treated as EDE evidence.

## Judge path (under three minutes)

1. Open **Compute → Execution** and run the default AxiCLASS point.
2. Change `H0` and run again.
3. Open **Atlas** to inspect the propagation chain, component χ² values, DESI residuals, and within-component Δχ².
4. Open **Consistency** to inspect published SH0ES/CCHP summaries, overlap protection, and the previous-run trade-off classification.
5. Open **Compare** for input, derived-output, all installed likelihood coordinates, and TT-spectrum differences.
6. Open **Evidence** to inspect durable SHA-256 run identities and source contracts.
