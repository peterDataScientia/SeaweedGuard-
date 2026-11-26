# SeaweedGuard

An experimental research prototype for microplastic identification, monitoring and mitigation in seaweed farming, developed for the Africa's Blue Futures Hackathon 2027.

## Research question
How reliably can spectral identification distinguish synthetic polymers from natural materials under environmental fouling, and when should uncertain predictions be referred for expert review?

## Data provenance
Kozloski, Cowger & Arienzo (2024), [Dryad dataset](https://doi.org/10.5061/dryad.f1vhhmh59). Raw data are retained separately in Google Drive; consult the source licence before redistribution. [Open Specy](https://github.com/wincowgerDEV/OpenSpecy-package) is the reference baseline, not an invention of this project.

## Start here
[Open E01 in Colab](https://colab.research.google.com/github/peterDataScientia/SeaweedGuard-/blob/main/notebooks/E01_Raw_Spectral_Data_Audit.ipynb)

Mount your own Drive and set the archive path. E01 inventories nested archives and audits readable numeric spectra without assigning unverified labels.

## Structure
- `notebooks/`: reproducible experiments
- `docs/`: scientific protocol and data provenance
- `outputs/`: generated audit tables (kept local by default)

## Status and limitations
Initial development only. No measured performance or local seaweed validation is claimed. Spectral identification alone cannot determine contamination sources, particle concentration, or food safety. All sample and group labels must be checked against original metadata before model evaluation.
