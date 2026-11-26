# E02 — Conservative cleaning (executed)

Source: https://doi.org/10.5061/dryad.f1vhhmh59. Run: python scripts/e02_clean.py ARCHIVE.zip --out outputs/E02 (requires numpy and pandas).

926 records: 686 eligible unique arrays, 185 quarantined for conflicting labels, 2 quarantined for invalid axes (also label-conflicting), 53 redundant copies. 70 distinct conflicting arrays: Nylon_fragments versus PC (25), PS versus PTFE (23), Cashmere versus Leather (22). No condition conflicts. Folder labels are provisional, with biofouling nylon mapped to Nylon_fragments based on the documented irregular particles. No conflicting labels were reassigned. Same-label pristine duplicates retain one representative, prioritizing test-library provenance. All original records remain in the generated manifest.

454 pristine records across 18 classes; 232 exposed records: Nylon 31 dry/26 wet, PP 31/31, PS 26/26, PVC 31/30. Pristine counts of these four classes: 1, 28, 3, 27 respectively. Exact numerical hashes are disjoint across partitions. Specimen-level independence and near-duplicate leakage remain unverified. Exposed holdout is a candidate external-condition benchmark, not an independent farm validation set. Do not fit or select models on this holdout. The pristine scarcity of nylon and PS prevents a defensible four-class benchmark without additional verified reference data or source-label reconciliation.

Generated outputs: manifest.csv, clean_index.csv, clean_spectra.npz. Original data and derived spectra are not redistributed here. No model performance claimed.
