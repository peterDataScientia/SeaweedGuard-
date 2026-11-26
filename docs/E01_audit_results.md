# E01 — Executed raw spectral audit

Source: Dryad DOI 10.5061/dryad.f1vhhmh59; archive `doi_10_5061_dryad_f1vhhmh59__v20241126.zip`, 60,830,858 bytes. SHA256: `2e50dadad8bff263fd6300ec4cbb8846e4a1debc78103a3e1205d1ada91caf67`.

## Observed results
- Test library: 588 CSV spectra in 22 folders; 518 unique numerical arrays.
- Biofouling library: 338 CSV spectra in 12 material/condition folders; 338 unique numerical arrays.
- Combined: 926 records, 756 unique numerical arrays, 170 redundant records, 123 duplicate groups involving 293 records. Exact byte duplicates involve 249 records. Cross-library overlap: 100 unique arrays involving 247 records. Within-library cross-folder duplicates: 70 groups.
- 924 spectra have 863 points on a common ascending grid (674.9918–3999.809 cm^-1; median spacing 3.857 cm^-1). Instrument resolution reported by source is 8 cm^-1, not grid spacing.
- Two CSVs have 862 rows, only 386 distinct wavenumbers each, and a nonmonotonic axis: `Test_spectra_library/PS/Polystyrene_1.CSV` and `Test_spectra_library/PTFE/Polystyrene_1.CSV`. The numerical arrays are identical. No nonfinite values in any CSV.
- Example cross-folder duplication: `Nylon_fragments/Nylon_fragments_1.CSV` and `PC/Nylon_fragments_1.CSV`, also repeated in the pristine nylon biofouling folder. Folder names are not validated ground truth.
- Reference OMNIC archive contains LBD, LBT and README files; 21,547 entries indicated in LBD header. Individual reference spectra not yet parsed.

## Method
Read both nested experimental ZIPs, parse each CSV with NumPy loadtxt (comma delimiter, one header row), compute SHA256 of raw bytes and float64 array bytes, compare groups and check finite values and wavenumber monotonicity. The two anomalous files were retained for reporting, not corrected.

## Interpretation and next steps
Quarantine conflicting labels and irregular axes until original source metadata are reconciled; do not randomly split repeated spectra. The pristine overlap may reflect intended reuse by original authors and is not proof of leakage in their published analysis. Independent specimen IDs remain unverified. Biofouling samples were exposed in the Mekong River and processed by peroxide oxidation; these do not constitute local seaweed-matrix validation. No model performance or novelty claim is made.
