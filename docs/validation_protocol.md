# Validation protocol

1. Verify original archive integrity, formats, axis units and specimen metadata.
2. Preserve original reference/test boundaries. Check exact duplicates, near duplicates and shared specimens across libraries.
3. Use specimen-grouped validation. Hold out environmental conditions where specimen provenance permits; report when grouping cannot be established.
4. Compare conventional spectral matching (Open Specy or a documented correlation baseline) against SVM and random forest with preprocessing fitted inside training folds.
5. Evaluate macro-F1, balanced accuracy, per-class confusion, natural-material false-positive rate and coverage versus error under abstention. Tune thresholds only on validation data; reserve the final test set.
6. Report uncertainty and limitations. Biofouled reference polymers do not establish performance in actual seaweed matrices. Source attribution and contamination mitigation require independent farm sampling evidence.

## Data provenance
https://doi.org/10.5061/dryad.f1vhhmh59
https://github.com/wincowgerDEV/OpenSpecy-package
