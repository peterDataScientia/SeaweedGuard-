# E03–E10: exploratory benchmark

55 pristine PP/PVC spectra (28 PP, 27 PVC); 123 exposed (62 PP, 61 PVC). Savitzky–Golay first derivative (window 11, polynomial 2), mean centering, L2 normalization. Five-fold stratified row CV, seed 2024, diagnostic only. Correlation 1NN, RBF SVM C=10 gamma=scale, RF 200 trees seed 2024.

| Model | CV balanced accuracy | Exposed balanced accuracy | Exposed macro-F1 |
|---|---:|---:|---:|
| Correlation 1NN | 0.963624 | 0.991803 | 0.991868 |
| SVM | 0.963624 | 0.975674 | 0.975610 |
| RF | 0.963624 | 0.975542 | 0.975603 |

Correlation threshold 0.965213765 (5th percentile of pristine out-of-fold nearest-reference similarity). Exposed acceptance 87/123 (70.73%); 86/87 accepted correct (98.85%). Dry acceptance 33/62; wet 54/61. The sole correlation error was accepted. This is a heuristic abstention rule, not calibrated confidence, and no open-set rejection claim is justified.

Reference OMNIC binary library remains unparsed. No official OpenSpecy comparison executed. Provisional folder labels and unknown independent specimen IDs constrain inference. No evidence of performance on real farmed seaweed samples. Prototype source prepared locally, not deployed. Source attribution and mitigation remain observational logging, not demonstrated efficacy.
