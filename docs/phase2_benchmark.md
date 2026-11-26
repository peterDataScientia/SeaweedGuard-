# Phase II exploratory multiclass benchmark

Data: E02 retained arrays, 454 pristine (18 provisional classes), 232 exposed (4 classes). Five-fold row and spectral-similarity-grouped CV used only the 16 pristine classes with at least five spectra (450 rows). No verified specimen identifiers. Same derivative preprocessing and fixed SVM as previous benchmark. The exposed set was already examined during prior development and is not a fresh external validation set.

| Evaluation | 1NN balanced accuracy | SVM balanced accuracy |
|---|---:|---:|
| Row CV | 97.89% | 99.02% |
| Group CV 0.999 | 98.40% | 99.02% |
| Group CV 0.995 | 98.12% | 99.02% |
| Group CV 0.990 | 97.90% | 99.02% |
| Exposed, 18 reference classes | 67.93% | 68.01% |

Both exposed classifiers achieved 160/232 exact folder-label matches. Correlation matching confusion: Nylon_fragments: 50 Nylon_fibers, 5 Dog_fur, 1 PS, 1 PVC; PP: 62 PP; PS: 39 PS, 11 ABS, 2 PVC; PVC: 59 PVC, 1 PP, 1 PS. A post-hoc chemistry-level sensitivity analysis combining Nylon fibers and fragments yields 210/232 correct (90.52%), balanced accuracy 89.86%. This is a different endpoint, not a model improvement; nylon chemical subtype equivalence and specimen provenance remain unverified. Seven exposed spectra have nearest pristine derivative correlation >=0.999, 22 >=0.995, 34 >=0.99. Similarity alone cannot establish shared specimens.

Official OpenSpecy comparison remains unexecuted: original archive has OMNIC LBD/LBT, not a verified numeric export. R runtime absent and OSF download failed DNS in execution environment. Official library/package: https://github.com/wincowgerDEV/OpenSpecy-package and https://osf.io/x7dpz/. Do not label internal correlation baseline OpenSpecy. Core pytest suite rerun: 8 passed; Streamlit not installed locally, browser test and deployment remain pending. Independent seaweed validation remains outstanding. The 18-class benchmark is exploratory; existing UI remains the narrower PP/PVC prototype.

Run: python phase2.py PATH_TO_E02 results
