# An Explainable Knowledge Graph-Based Framework for Personalized Drug Repurposing for Bangladeshi Lung Cancer Patients

```text
         [ Genomic Data ]            |         [ Clinical Target ]
                                     |
            \      /                 |              ____    ____
           - \    / -                |             /    \  /    \
              \  /                   |            |      ||      |
               \/                    |            |  ||  ||  ||  |
               /\                    |            |  ||  ||  ||  |
              /  \                   |            |      ||      |
           - /    \ -                |             \____/  \____/
            /      \                 |
```

## Abstract
Lung cancer remains one of the most prominent health challenges in Bangladesh, marked by high mortality rates and limited clinical access to targeted precision therapies. Traditional de novo drug discovery is an extraordinarily slow and expensive process. While computational drug repurposing offers a cost-effective alternative, current AI-driven models suffer from two major barriers: Geographical/Genomic Bias (relying almost exclusively on Western cohorts) and the Black Box Problem (lacking transparent biological reasoning for clinicians). 

This repository implements a localized, heterogeneous biomedical knowledge graph coupled with Graph Neural Networks (Heterogeneous GraphSAGE) and path-based Explainable AI (XAI) to perform personalized drug repurposing specifically tailored for Bangladeshi non-small cell lung cancer (NSCLC) patients. The entire framework ensures strict reproducibility and uniqueness, operating on robust in-silico validation.

## Research Objectives & Novelty
The primary objective of this research is to design, implement, and evaluate an explainable AI (XAI) framework based on a heterogeneous biomedical knowledge graph to identify personalized, repurposed drug candidates.

1. Construct a Localized Biomedical Knowledge Graph: Aggregate primary clinical and somatic mutation profiles from Bangladeshi patients, integrating them with global repositories.
2. Implement GNNs for Link Prediction: Develop Heterogeneous GraphSAGE to learn low-dimensional graph embeddings and predict high-affinity drug-disease associations.
3. Extract Explainable Biological Pathways via XAI: Integrate path-based XAI algorithms to extract human-readable molecular traversal paths ensuring full mechanistic transparency.
4. Deliver a Clinical Decision-Support System: Benchmark predicted candidates against drug-response data and published literature.

**Novelty:** The inclusion of localized somatic mutation data from the Bangladeshi demographic re-weights the graph edges, effectively breaking the Western-centric geographical bias in current precision oncology models.

## Proposed Methodology & Pipeline

```text
  [ Global Biomedical Data ]                [ Primary Bangladeshi Patient Data ]
              \                                          /
               \                                        /
                v                                      v
    +-------------------------------------------------------------+
    |           STEP 1: Data Localization & KG Construction       |
    |  (Nodes: Patient, Gene, Protein, Disease, Drug, Pathway)    |
    +-----------------------------+-------------------------------+
                                  |
                                  v
    +-----------------------------+-------------------------------+
    |           STEP 2: Heterogeneous GraphSAGE Model Pre-training                  |
    |  (Learning Heterogeneous Graph Embeddings & Link Prediction)|
    +-----------------------------+-------------------------------+
                                  |
                                  v
    +-----------------------------+-------------------------------+
    |           STEP 3: Patient Personalization & Fine-Tuning     |
    |  (Dynamic Edge Re-weighting via VAF & Genomic Profiles)     |
    +-----------------------------+-------------------------------+
                                  |
                                  v
    +-----------------------------+-------------------------------+
    |           STEP 4: Mechanistic XAI Extraction                |
    |  (Extracting Human-Readable Molecular Traversal Paths)      |
    +-----------------------------+-------------------------------+
                                  |
                                  v
    +-----------------------------+-------------------------------+
    |           STEP 5: Rigorous Validation & Scoring             |
    |  (Benchmarking vs GDSC, PRISM, FAERS, and Clinical Data)    |
    +-------------------------------------------------------------+
```

**Detailed Pipeline Descriptions:**
* **Step 1:** Filtering global biomedical data alongside primary Bangladeshi clinical/somatic mutation profiles (MAF/VAF data) to construct standardized graph entities.
* **Step 2:** Training Heterogeneous GraphSAGE models on the global knowledge graph to capture complex non-linear topological interactions via link prediction.
* **Step 3:** Dynamically reweighting graph edge weights using patient-specific Variant Allele Frequency (VAF) scores to adapt predictions for individual genomic profiles.
* **Step 4:** Traversing the graph topology to extract human-readable molecular paths that medically justify every prioritized drug candidate.
* **Step 5:** Benchmarking performance using AUROC/AUPRC metrics, performing ablation studies, and cross-validating predictions with independent drug-response data and literature.

## Data Architecture & Integration

To achieve absolute peer-review rigor, this system constructs a comprehensive heterogeneous knowledge graph by querying 14 independent, live biomedical APIs and databases. Rather than relying on static, deprecated CSV files, our pipeline programmatically authenticates, fetches, and integrates real-time data to ensure the graph reflects the latest clinical and molecular consensus.

### Comprehensive Dataset Directory

| Dataset / API | Data Role & Graph Contribution | Official Access / Download Link |
| :--- | :--- | :--- |
| **AACR Project GENIE** | Clinical genomic sequencing data; patient mutation profiles. | [cBioPortal API](https://www.cbioportal.org/api/swagger-ui/index.html) |
| **Open Targets Platform** | Therapeutic knowledge, target-disease associations, and evidence scores. | [Open Targets GraphQL API (v4)](https://api.platform.opentargets.org/api/v4/graphql) |
| **STRING** | Protein-Protein Interactions (PPI) mapped via high-confidence human networks. | [STRING REST API](https://string-db.org/help/api/) |
| **Reactome** | Mechanistic pathway layers ensuring XAI biological interpretability. | [Reactome Content Service](https://reactome.org/ContentService/) |
| **MyVariant.info** | Canonical variant mapping, rsID extraction, and ClinVar clinical significance. | [MyVariant.info API](https://myvariant.info/docs/) |
| **Ensembl REST** | Genetic population frequencies (South Asian & Bengali AF). | [Ensembl REST API](https://rest.ensembl.org/) |
| **QuickGO (EBI)** | Gene Ontology (GO) functional annotations for network expansion. | [QuickGO API](https://www.ebi.ac.uk/QuickGO/api/index.html) |
| **GTEx Portal** | Normal lung tissue expression profiles (TPM) for baseline biological context. | [GTEx v2 API](https://gtexportal.org/api/v2/redoc) |
| **DrugMechDB** | Curated mechanistic paths for XAI evaluation and validation. | [DrugMechDB GitHub](https://github.com/SuLab/DrugMechDB) |
| **GDSC (Sanger)** | Genomics of Drug Sensitivity in Cancer; functional drug efficacy validation. | [GDSC Release 8.4 Data](https://www.cancerrxgene.org/downloads/bulk_download) |
| **openFDA (FAERS & DailyMed)** | Post-marketing adverse events, label warnings, and contraindications. | [openFDA API](https://open.fda.gov/apis/) |
| **OncoKB** | Expert-curated clinical actionability (Requires independent API Token). | [OncoKB Public API](https://www.oncokb.org/swagger-ui/index.html) |
| **ChEMBL** | Drug clinical phase status, structures, and molecular target affinity. | [ChEMBL REST API](https://www.ebi.ac.uk/chembl/api/data/docs) |

## Universal Identifier Strategy

Our pipeline preserves original identifiers and generates a central mapping table to prevent data corruption during integration:

* **Drug:** Primary identifier is ChEMBL ID, supplemented by DrugCentral ID, PubChem CID, and InChIKey.
* **Gene:** Primary computational identifier is Ensembl Gene ID; human-readable identifier is HGNC Gene Symbol.
* **Protein:** Primary identifier is UniProt accession.
* **Disease:** Standardized ontology identifiers (e.g., MONDO, EFO).
* **Variant:** Genome build, chromosome, position, reference/alternate allele, and HGVS notation.

## Core Knowledge Graph Structure

Our heterogeneous graph contains the following core entity types and hierarchical relationships:

```text
Patient -> [harbors] -> Variant
Variant -> [affects] -> Gene
Gene -> [encodes] -> Protein
Protein -> [interacts_with] -> Protein
Protein -> [participates_in] -> Pathway
Pathway -> [associated_with] -> Disease
Drug -> [targets] -> Protein
Drug -> [has_response_in] -> Cancer Cell Line -> [has_molecular_profile] -> Gene
Drug -> [associated_with] -> Adverse Event
Variant -> [clinically_interpreted_by] -> ClinVar / OncoKB
```

## Drug Prediction Process

Our system performs multi-stage predictions rather than deriving simple direct correlations:

1. **Patient Molecular Profiling:** Constructing a personalized subgraph from clinical characteristics, subtype, and somatic mutations (VAF).
2. **Mutation Prioritization:** Evaluating mutation characteristics using VAF, ClinVar, OncoKB, and functional dependency.
3. **Biological Network Expansion:** Connecting high-priority genes through STRING, UniProt, Reactome, and Gene Ontology.
4. **Drug Candidate Generation:** Deriving candidate drugs via Open Targets, DrugCentral, and DrugMechDB relationships.
5. **Experimental Evidence Filtering:** Cross-checking candidate drugs against GDSC, PRISM, and DepMap sensitivity metrics.
6. **Safety Filtering:** Penalizing dangerous candidates using FAERS and DailyMed adverse-event data.
7. **Mechanistic Explanation:** Extracting biologically meaningful paths (e.g., Patient Mutation -> Gene -> Protein -> Pathway -> Drug Target -> Drug) via our XAI module.
8. **Final Ranking:** Calculating the final priority experimentally: `Final Score = Biological Relevance + Clinical Evidence + Drug Response Evidence + Mechanistic Evidence - Safety Risk`.

## Reproducibility Requirements
For every dataset used, our repository maintains an exact metadata tracking file. This includes provider, exact download URL, version/release date, SHA-256 hash, processing steps, filtering criteria, and final number of records. We firmly document exact processing steps rather than generic dataset citations.


## Reproducibility Guidelines (Code Execution)
To ensure open-science compliance and strict reproducibility, follow these step-by-step instructions to replicate the entire study:

### Step 1: Environment Setup
1. Ensure Python 3.9+ is installed.
2. Install all required dependencies using the provided requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Data Preprocessing & KG Construction
Execute **Notebook 1** (`src/data_processing/BGLC_KG_Data_Pipeline.ipynb`).
* **What it does:** Fetches raw data from 17 live biomedical APIs, canonicalizes identifiers, and constructs the `HeteroData` Knowledge Graph.
* **Outputs:** 
  - `graph/BGLC-KG-split.pt` (The graph tensor with train/val/test masks).
  - `figures/metagraph_schema_final.pdf` (KG Schema).
  - EDA Distribution Plots (Population AF, Clinical Phases, PPI Subgraphs).

### Step 3: Model Training & Novel Drug Prediction
Execute **Notebook 2** (`src/models/BGLC_KG_Model_Training.ipynb`).
* **What it does:** Loads the graph, trains the Heterogeneous GraphSAGE model, executes SOTA KGE Benchmarking (TransE, RotatE, etc.), and predicts novel drug repurposing candidates.
* **Outputs:**
  - `models/top_novel_candidates.csv` (Full prediction rankings).
  - `visualizations/model_performance_evaluation.png` (ROC, PR, Loss graphs).
  - `visualizations/drug_mapping_top200.png` (Top 200 Drug Heatmap).
  - `visualizations/realtime_kg_connection_rank_X.png` (Top 100 Drug Subgraphs for XAI).

## Comprehensive Literature Review

| Author & Reference | Dataset Used | Model / Algorithm Used | Key Limitations Identified |
| :--- | :--- | :--- | :--- |
| Ryu et al. (2026) [1] | OncoKB, PubMed, TxGNN KG, CPTAC | Rule-based Heuristic Prioritization (IDAP) | Relies on non-causal co-mentions; heuristic scores sensitive to weights; lacks deep XAI path extraction. |
| Perdomo-Quinteiro et al. (2026) [2] | NeDRex KG, DrugMechDB | Heterogeneous GraphSAGE + XAIPath | Path evaluation increases computation time exponentially; lacks patient-level multi-omics. |
| Khodadadi AghGhaleh et al. (2026) [3] | RepoDB, SIDER, STRING, DisGeNET | Word2Vec + Dual-Channel 1D-CNN | Relies on trial-and-error grid search; lacks an XAI module for human-readable pathway extraction. |
| Li & Xie (2026) [4] | TCGA, NCG, COSMIC, PPI | MNDGNN (Multiplex Directed GNN) | Identifies driver genes rather than drug repurposing candidates; noisy multiplex edges affect performance. |
| Gonzalez-Cavazos et al. (2026) [5] | MIND KG, DrugMechDB | DBR-X (Case-Based Reasoning + Heterogeneous GraphSAGE) | Similarity retrieval relies on simple inner products; completely lacks localized genomic profiling. |
| Islam et al. (2023) [6] | NICRH Hospital Registry (Bangladesh) | Statistical Survival Analysis | Purely observational clinical dataset; lacks AI/GNN computational modeling or drug repurposing integration. |
| Aamer et al. (2026) [7] | PrimeKG, FDA Approvals | COMIC (Contrastive Masking) | Performance degrades on sparse graphs; DDI congestion obscures actual mechanistic paths. |
| Abo-Dahab et al. (2026) [8] | ChEMBL 36 | TransR, ComplEx, Heterogeneous GNN | Transductive setup limits performance on unobserved cold-start entities without topological context. |
| Xiong et al. (2025) [9] | BioSNAP, DrugBank, BindingDB | Geometric GNN (GPS-DTI) with CAM | Focuses solely on paired binding affinity rather than complex multi-layered patient Knowledge Graphs. |
| Khan et al. (2025) [10] | DrugBank, RCSB PDB | Molecular Docking & MD Simulations | Purely structural in silico approach; lacks population-specific patient multi-omics or GNN link prediction. |
| Wu et al. (2025) [11] | Multicenter NSCLC Cohort | Integrated ML Survival Framework | Focuses strictly on machine learning survival modeling; lacks explicit XAI graph path extraction. |

## Copyright and Uniqueness
This repository and the architectural concepts within are designed strictly to prevent plagiarism. The integration of localized VAF data with graph edge re-weighting in a Heterogeneous GraphSAGE space is a novel approach completely unique to this research. Our framework integrates population-specific patient genomics with a heterogeneous, evidence-weighted biomedical knowledge graph and independently validates drug-repurposing candidates using mechanistic, functional, pharmacological, clinical-actionability, and safety evidence. All code is originally authored and copyright free.

## References
[1] Y. Ryu, H.-E. Jeong, and J.-Y. An, "IDAP: An integrated literature- and knowledge-graph-driven evidence prioritization pipeline for precision oncology," Bioinformatics, vol. 42, 2026.
[2] P. Perdomo-Quinteiro, E. Guney, and A. Belmonte-Hernández, "Generating explainable hypotheses for drug repurposing with graph neural networks," Sci. Rep., vol. 16, 2026.
[3] M. Khodadadi AghGhaleh et al., "ConvAHKG: Action-based hybrid knowledge graph with a dual-channel convolutional approach for drug repurposing," Sci. Rep., vol. 16, 2026.
[4] P. Li and M. Xie, "Multiplex networks-based directed graph neural networks for cancer driver gene identification," PLOS Comput. Biol., vol. 22, 2026.
[5] A. C. Gonzalez-Cavazos, R. Tu, M. Sinha, and A. I. Su, "A case-based explainable graph neural network framework for mechanistic drug repositioning," Bioinformatics, vol. 42, 2026.
[6] M. R. Islam et al., "Lung cancer in Bangladesh," J. Thorac. Oncol., vol. 18, pp. 972–980, 2023.
[7] N. Aamer, M. N. Asim, and A. Dengel, "COMIC: Explainable drug repurposing via contrastive masking for interpretable connections," BMC Bioinformatics, vol. 27, 2026.
[8] Y. Abo-Dahab, R. Hernández, and I. C. Arechiga Durán, "Pharmacology knowledge graphs enable drug repurposing without chemical structure information," Discov. Artif. Intell., vol. 6, 2026.
[9] A. Xiong et al., "An interpretable geometric graph neural network for enhancing the generalizability of drug-target interaction prediction," BMC Biol., vol. 23, 2025.
[10] M. S. Khan, A. Shamsi, A. Zuberi, and M. Shahwan, "In silico repurposing of FDA-approved drugs against MEK1: Structural and dynamic insights into lung cancer therapeutics," Front. Pharmacol., vol. 16, 2025.
[11] X. Wu et al., "Integrated machine learning survival framework for consensus modeling in a large multicenter cohort of NSCLC resistant to aumolertinib," Sci. Rep., vol. 15, 2025.
