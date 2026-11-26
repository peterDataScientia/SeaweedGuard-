# SeaweedGuard: Intelligent Microplastic Screening for Seaweed Quality Monitoring

**Africa's Blue Futures Hackathon 2027 | Concept note v0.0.3 | 26 November 2026**  
**Proposed challenge:** Microplastics in seaweed (based on the circulated call; exact catalogue wording and submission requirements to be checked).

### 1. Problem and opportunity

Seaweed farming supports coastal livelihoods in Tanzania, employing over 23,000 farmers in Zanzibar, approximately 80% of whom are women (United Nations in Tanzania, 2026). The documented occurrence of microplastics in Tanzanian coastal environments and cultivated seaweed elsewhere highlights the relevance of contamination monitoring to the sector (Nchimbi, Kosore, et al., 2022; Nchimbi, Shilla, et al., 2022; Suryandari et al., 2025). Although infrared spectroscopy combined with computational pattern recognition has demonstrated the potential to identify environmentally weathered polymers (Ferreiro et al., 2022), the reliability of automated spectral identification remains dependent on reference libraries, spectral processing and sample condition. Kozloski et al. (2024a) reported classification accuracies ranging from 64.1% to 98.0% across spectral matching routines for distinguishing natural from synthetic materials, with high spectral similarity not consistently corresponding to correct identification. The analytical challenge is therefore to minimise incorrect assignments while retaining sufficient identification coverage for practical monitoring. This presents an opportunity to integrate reliability-aware computational screening into laboratory-supported seaweed quality monitoring, facilitating candidate polymer identification, targeted expert review and evidence-informed contamination management.

### 2. Proposed solution

SeaweedGuard is a web-based computational platform designed to support reliable microplastic identification in laboratory-assisted seaweed quality monitoring. It analyses ATR-FTIR spectra of isolated suspected plastic particles and identifies candidate polymers through spectral matching against a curated reference library. To address identification errors associated with environmentally altered spectra, the platform combines first-derivative spectral processing, exclusion of the 1500–1700 cm⁻¹ spectral region and similarity- and class-margin-based acceptance criteria.

The functional prototype integrates single and batch spectral analysis, interactive spectral visualisation, reference comparison, downloadable analytical results and farm observation recording. By distinguishing accepted candidates from uncertain and non-target assignments, SeaweedGuard supports targeted expert review and provides a basis for translating laboratory findings into seaweed contamination monitoring and management decisions.

**Prototype:** https://seaweedguard.streamlit.app/  
**Repository:** https://github.com/peterDataScientia/SeaweedGuard-

### 3. Innovation and evidence

Existing computational platforms, including Open Specy, have established the potential of automated spectral matching for microplastic identification (Cowger et al., 2021). SeaweedGuard builds upon these advances by integrating spectral processing for environmentally altered polymers, reliability-based acceptance criteria and a proposed farm-to-laboratory monitoring workflow. Its distinctive contribution lies in prioritising reliable polymer assignments rather than maximising the number of automatically classified spectra, while providing an accessible interface for laboratory-supported seaweed quality monitoring.

The computational approach was developed using published spectral datasets (Kozloski et al., 2024b) and externally evaluated using 3,832 ATR-FTIR spectra from the MicroPlastiX database (Lenz et al., 2023). The evaluation examined polymer identification accuracy, acceptance coverage and the rejection of non-target spectra.

| Evaluation metric | Result |
|---|---:|
| PP/PS classification accuracy | 85.37% (1,027/1,203) |
| Accepted target classification accuracy | 100% (767/767) |
| Target acceptance coverage | 63.76% (767/1,203) |
| Non-target rejection rate | 99.47% (2,615/2,629) |
| Overall accepted prediction precision | 98.21% (767/781) |

These findings demonstrate the potential of selective spectral screening to support reliable polymer identification while acknowledging the trade-off between prediction reliability and acceptance coverage. Overall accepted prediction precision accounts for 14 false acceptances among non-target spectra. The external evaluation provides evidence for polypropylene and polystyrene under the tested conditions; further validation using locally collected seaweed-derived particles is required to establish applicability within Tanzanian seaweed quality-monitoring workflows. Nylon and PVC were not represented in the external evaluation.

### 4. Implementation pathway

**Farm → Sample collection → Laboratory extraction and ATR-FTIR → SeaweedGuard screening → Expert confirmation → Farm-level action → Repeat monitoring**

A proposed pilot would bring together a seaweed producer group, an analytical laboratory and a marine science partner. Farmers or extension officers would record sampling locations, processing stages and relevant equipment. Trained laboratory staff would isolate suspected particles using a matrix-appropriate procedure informed by published seaweed extraction methods (Pereira et al., 2026), with blanks, recovery controls and an instrument-appropriate minimum particle size. They would export spectra to SeaweedGuard, review accepted and uncertain assignments against reference spectra and record confirmed findings.

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

SeaweedGuard aims to make laboratory evidence more accessible and actionable, support targeted plastic-waste prevention and strengthen monitoring capacity in coastal communities. Reduced contamination, improved market confidence and economic benefits are intended outcomes requiring prospective evidence. The MVP cannot directly diagnose intact seaweed, quantify particle concentration from a single spectrum, establish contamination sources or certify food safety. Local matrix validation, persistent traceable records and a viable laboratory service arrangement are priorities before routine use. The public demonstration supports recorded example replay, whereas live inference requires the authorised frozen model bundle. Reference-data redistribution permissions must be resolved before unrestricted deployment.

### References

Cowger, W., Steinmetz, Z., Gray, A., Munno, K., Lynch, J., Hapich, H., Primpke, S., De Frond, H., Rochman, C., & Herodotou, O. (2021). Microplastic spectral classification needs an open source community: Open Specy to the rescue! *Analytical Chemistry, 93*(21), 7543–7548. https://doi.org/10.1021/acs.analchem.1c00123

Ferreiro, B., Andrade, J. M., Paz-Quintáns, C., Fernández-González, V., López-Mahía, P., & Muniategui, S. (2022). Weathering-independent differentiation of microplastic polymers by reflectance IR spectrometry and pattern recognition. *Marine Pollution Bulletin, 181*, Article 113897. https://doi.org/10.1016/j.marpolbul.2022.113897

Kozloski, R., Cowger, W., & Arienzo, M. M. (2024a). Moving toward automated µFTIR spectra matching for microplastic identification: Addressing false identifications and improving accuracy. *Microplastics and Nanoplastics, 4*, Article 27. https://doi.org/10.1186/s43591-024-00106-5

Kozloski, R., Cowger, W., & Arienzo, M. M. (2024b). *uFTIR test spectra for known synthetic and natural materials* [Data set]. Dryad. https://doi.org/10.5061/dryad.f1vhhmh59

Lenz, R., Fischer, F., Arnold, M., Fernández-González, V., Moscoso Pérez, C. M., Andrade-Garda, J. M., Muniategui-Lorenzo, S., & Fischer, D. (2023). *MicroPlastiX SpecDB* [Data set]. RADAR. https://doi.org/10.22000/1820

Nchimbi, A. A., Kosore, C. M., Oduor, N., Shilla, D. J., Shashoua, Y., Khan, F. R., & Shilla, D. (2022). Microplastics in marine nearshore surface waters of Dar es Salaam and Zanzibar, East Africa. *Bulletin of Environmental Contamination and Toxicology, 109*, 1037–1042. https://doi.org/10.1007/s00128-022-03620-5

Nchimbi, A. A., Shilla, D., Kosore, C. M., Shilla, D. J., Shashoua, Y., & Khan, F. R. (2022). Microplastics in marine beach and seabed sediments along the coasts of Dar es Salaam and Zanzibar in Tanzania. *Marine Pollution Bulletin, 185*, Article 114305. https://doi.org/10.1016/j.marpolbul.2022.114305

Pereira, R., Almeida, C. M. R., & Ramos, S. (2026). Optimization of an analytical methodology to determine microplastic contamination in different seaweed groups (Phaeophyceae, Rhodophyta and Chlorophyta). *MethodsX, 16*, Article 103816. https://doi.org/10.1016/j.mex.2026.103816

Suryandari, R., Sudrajat, & Nugroho, A. P. (2025). Microplastic contamination on cottonii seaweed (*Kappaphycopsis cottonii*) cultivated in Bomo Beach, Banyuwangi, East Java, Indonesia. *EnvironmentAsia, 18*(1), 13–23. https://doi.org/10.14456/ea.2025.2

United Nations in Tanzania. (2026, July 13). *Zanzibar’s seaweed sector draws global interest*. https://tanzania.un.org/en/319757-zanzibar%E2%80%99s-seaweed-sector-draws-global-interest

**Draft status:** Concept note prepared for internal review. The official challenge catalogue could not be retrieved during preparation. No partnerships, funding or pilot results have been assumed. E18 figures are project-reported results as documented in the repository README; independent CI and complete deployed-interface testing have not been verified by the assistant.
