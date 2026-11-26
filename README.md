# SeaweedGuard — v1.0.0

**Hackathon MVP | Africa's Blue Futures Hackathon 2027**

[Open the web application](https://seaweedguard.streamlit.app/)

SeaweedGuard is an experimental ATR-FTIR spectral screening workstation for identifying candidate polymers in isolated, measured samples, with a prospective application in seaweed contamination monitoring.

## MVP freeze — 26 November 2026

The project owner confirmed the interface was working satisfactorily. This version freezes the approved v0.2.11 workstation without modifying the E18 scientific engine. Independent browser automation and CI results have not been confirmed.

- Built-in experimental examples and downloadable CSVs.
- Single-spectrum and batch workflows.
- Dynamic intensity display, spectral zoom and reference overlay when the model is connected.
- Figentra publication exports (PNG, PDF and SVG).
- Session-based farm observations and analysis history.

The public demo supports recorded example replay. Live inference on other spectra requires the authorised frozen model bundle, which is distributed separately pending reference-data licence review.

## Scientific evidence

Reported E18 external evaluation using [MicroPlastiX](https://doi.org/10.22000/1820), 3,832 ATR-FTIR spectra:

| Endpoint | Result |
|---|---:|
| PP/PS target classification | 1,027 / 1,203 (85.37%) |
| Correct accepted target predictions | 767 / 767 (100%) |
| Target acceptance coverage | 767 / 1,203 (63.76%) |
| Non-target rejection | 2,615 / 2,629 (99.47%) |

Accepted target accuracy is conditional on accepted PP/PS target spectra and excludes 14 non-target false acceptances. Nylon and PVC were not represented in this external evaluation. No direct validation of seaweed tissue, particle concentrations, contamination sources or food safety is claimed.

## Research question

How reliably can spectral identification distinguish synthetic polymers from natural materials under environmental fouling, and when should uncertain predictions be referred for expert review?

## Data provenance

- [Kozloski, Cowger & Arienzo (2024) — Dryad dataset](https://doi.org/10.5061/dryad.f1vhhmh59).
- [MicroPlastiX external dataset](https://doi.org/10.22000/1820).
- [Open Specy](https://github.com/wincowgerDEV/OpenSpecy-package) is the reference baseline, not an invention of this project.

Consult original source licences before redistribution.

## Research and code

[Open E01 in Colab](https://colab.research.google.com/github/peterDataScientia/SeaweedGuard-/blob/main/notebooks/E01_Raw_Spectral_Data_Audit.ipynb)

Mount your own Drive and set the archive path. E01 inventories nested archives and audits readable numeric spectra without assigning unverified labels.

- `notebooks/`: reproducible experiments.
- `docs/`: scientific protocol and data provenance.
- `outputs/`: generated audit tables (kept local by default).
- `app.py`: web workstation.
- `frozen_engine.py`: frozen E18 inference.
- `tests/`: automated regression and interface checks.
