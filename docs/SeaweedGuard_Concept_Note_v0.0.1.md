# SeaweedGuard: Intelligent Microplastic Screening for Seaweed Quality Monitoring

**Africa's Blue Futures Hackathon 2027 | Concept note v0.0.1 | 26 November 2026**  
**Proposed challenge:** Microplastics in seaweed (based on the circulated call; exact catalogue wording and submission requirements to be checked).

### 1. Problem and opportunity

Seaweed farming supports coastal livelihoods in Tanzania, but plastic contamination is a potential challenge throughout cultivation, harvesting, drying and processing. Microplastics have been documented in coastal surface waters and sediments of Dar es Salaam and Zanzibar [1,2]. This establishes regional exposure, not the prevalence or origin of microplastics in Tanzanian farmed seaweed. Recent research also highlights the difficulty of extracting particles from complex seaweed matrices without compromising polymer integrity [3]. For practical monitoring, a credible workflow must therefore combine representative sampling, laboratory identification, transparent handling of uncertain results and feedback to farmers.

### 2. Proposed solution

SeaweedGuard is a browser-based decision-support workstation for analysing measured attenuated total reflection Fourier-transform infrared (ATR-FTIR) spectra of isolated suspected plastic particles. The MVP (v1.0.0) provides single and batch screening, experimental examples, dynamic spectral visualisation, downloadable results and a session-based farm observation log. Its reference-matching engine uses first-derivative spectra, an empirically selected exclusion region and similarity and class-margin thresholds. Rather than force a polymer assignment, it flags uncertain or non-target results for laboratory review.

**Prototype:** https://seaweedguard.streamlit.app/  
**Repository:** https://github.com/peterDataScientia/SeaweedGuard-

### 3. Innovation and evidence

Existing spectral tools such as Open Specy [4] already support polymer identification. SeaweedGuard's proposed contribution is not a new spectroscopic technique, but an application-specific combination of fouling-aware screening, explicit rejection rules and a practical farm-to-laboratory feedback workflow. The workflow is designed to prioritise reliable identification and reveal where additional evidence is required.

The frozen E18 method was evaluated against 3,832 ATR-FTIR spectra from the independent-source MicroPlastiX library [5], comprising weathered and biofouled polymers.

| Evaluation endpoint | Reported result |
|---|---:|
| PP/PS target classification accuracy before rejection | 1,027/1,203 (85.37%) |
| Correct classifications among accepted target spectra | 767/767 (100%) |
| Target acceptance coverage | 767/1,203 (63.76%) |
| Non-target rejection | 2,615/2,629 (99.47%) |

The accepted-target result excludes 14 false acceptances among non-target spectra. Nylon and PVC were absent from this external dataset. These are spectrum-level results, not farm-level or seaweed-matrix validation. Public examples can replay recorded results; live inference requires an authorised model bundle. Individual reference-data redistribution permissions must be resolved before unrestricted deployment.

### 4. Implementation pathway

**Farm → Sample collection → Laboratory extraction and ATR-FTIR → SeaweedGuard screening → Expert confirmation → Farm-level action → Repeat monitoring**

A proposed pilot would bring together a seaweed producer group, an analytical laboratory and a marine science partner. Farmers or extension officers would record sampling locations, processing stages and relevant equipment. Trained laboratory staff would isolate suspected particles using a matrix-appropriate procedure with blanks, recovery controls and an instrument-appropriate minimum particle size. They would export spectra to SeaweedGuard, review accepted and uncertain assignments against reference spectra and record confirmed findings.

Confirmed polymer patterns could help prioritise inspection of worn cultivation materials, drying surfaces, storage and handling practices. Polymer identity alone cannot establish contamination sources; comparison with candidate materials and appropriate controls is needed. Any intervention would be evaluated through comparable before-and-after sampling rather than assumed effective.

### 5. Target users and sustainability

Primary operators are laboratory technicians, researchers and quality-control staff. Seaweed farmers and cooperatives are intended beneficiaries and contributors to sampling and mitigation decisions. Extension officers and processors could coordinate shared laboratory access, so every farm would not need its own FTIR instrument. A possible sustainability model is a shared monitoring service funded through institutional partnerships, cooperative or processor contributions, and transparent per-batch laboratory costs. Partner commitments, affordability and willingness to pay are to be assessed during the pilot, not claimed as established.

### 6. Hackathon development and success measures

| Stage | Proposed activity | Deliverable |
|---|---|---|
| Day 1 | Interview stakeholders; map sampling, laboratory access and decision requirements | Agreed pilot workflow and user needs |
| Day 2 | Demonstrate CSV acquisition, live screening with authorised bundle, and review/export; design local sample-preparation controls | Tested workflow and pilot protocol |
| Day 3 | Refine implementation, costs, evaluation criteria and pitch | MVP demonstration and partner engagement plan |
| Post-hackathon | Secure laboratory and cooperative partners; conduct blinded local pilot | Evidence of recovery, identification performance, turnaround, costs and usability |

Pilot success would be evaluated using extraction recovery, blank contamination, expert-confirmed polymer agreement, false acceptances, rejection rate, turnaround time, cost per sample and user task completion. Results would be stratified by polymer, particle size and sampling stage. Intervention effectiveness would be evaluated separately using comparable contamination measurements.

### 7. Expected impact and limitations

SeaweedGuard aims to make laboratory evidence more accessible and actionable, support targeted plastic-waste prevention and strengthen monitoring capacity in coastal communities. Reduced contamination, improved market confidence and economic benefits are intended outcomes requiring prospective evidence. The MVP cannot directly diagnose intact seaweed, quantify particle concentration from a single spectrum, establish contamination sources or certify food safety. Local matrix validation, persistent traceable records and a viable laboratory service arrangement are priorities before routine use.

### References and evidence

1. *Microplastics in marine beach and seabed sediments along the coasts of Dar es Salaam and Zanzibar in Tanzania* (2022). https://pubmed.ncbi.nlm.nih.gov/36343543/
2. *Microplastics in Marine Nearshore Surface Waters of Dar es Salaam and Zanzibar, East Africa* (2022). https://pubmed.ncbi.nlm.nih.gov/36121466/
3. *Optimization of an analytical methodology to determine microplastic contamination in different seaweed groups (Phaeophyceae, Rhodophyta and Chlorophyta)* (2026). https://pubmed.ncbi.nlm.nih.gov/41743046/
4. Open Specy. https://github.com/wincowgerDEV/OpenSpecy-package
5. Lenz, R., et al. MicroPlastiX SpecDB. https://doi.org/10.22000/1820
6. Kozloski, R., Cowger, W., & Arienzo, M. (2024). uFTIR test spectra for known synthetic and natural materials. https://doi.org/10.5061/dryad.f1vhhmh59

**Draft status:** Concept note prepared for internal review. The official challenge catalogue could not be retrieved during preparation. No partnerships, funding or pilot results have been assumed. E18 figures are project-reported results as documented in the repository README; independent CI and complete deployed-interface testing have not been verified by the assistant.
