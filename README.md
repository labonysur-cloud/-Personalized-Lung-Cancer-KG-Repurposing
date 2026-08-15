# An Explainable Knowledge Graph-Based Framework for Personalized Drug Repurposing for Bangladeshi Lung Cancer Patients

```text
       .---.       .---.           \     /
      /     \     /     \           \   /
     |       |   |       |           | |
     |       |   |       |          /   \
      \     /     \     /          /     \
       `---'       `---'          |       |
         L U N G S                 \     /
                                    \   /
                                     | |
                                     DNA
```

## Abstract
Lung cancer remains one of the most prominent health challenges in Bangladesh, marked by high mortality rates and limited clinical access to targeted precision therapies. Traditional de novo drug discovery is an extraordinarily slow and expensive process. While computational drug repurposing offers a cost-effective alternative, current AI-driven models suffer from two major barriers: Geographical/Genomic Bias (relying almost exclusively on Western cohorts) and the Black Box Problem (lacking transparent biological reasoning for clinicians). 

This repository implements a localized, heterogeneous biomedical knowledge graph coupled with Graph Neural Networks (R-GCN) and path-based Explainable AI (XAI) to perform personalized drug repurposing specifically tailored for Bangladeshi non-small cell lung cancer (NSCLC) patients. The entire framework ensures strict reproducibility and uniqueness, operating on robust in-silico validation.

## Research Objectives & Novelty
The primary objective of this research is to design, implement, and evaluate an explainable AI (XAI) framework based on a heterogeneous biomedical knowledge graph to identify personalized, repurposed drug candidates.

1. Construct a Localized Biomedical Knowledge Graph: Aggregate primary clinical and somatic mutation profiles from Bangladeshi patients, integrating them with global repositories.
2. Implement GNNs for Link Prediction: Develop Relational Graph Convolutional Networks (R-GCNs) to learn low-dimensional graph embeddings and predict high-affinity drug-disease associations.
3. Extract Explainable Biological Pathways via XAI: Integrate path-based XAI algorithms to extract human-readable molecular traversal paths ensuring full mechanistic transparency.
4. Deliver a Clinical Decision-Support System: Benchmark predicted candidates against drug-response data and published literature.

Novelty: The inclusion of localized somatic mutation data from the Bangladeshi demographic re-weights the graph edges, effectively breaking the Western-centric geographical bias in current precision oncology models.

## Proposed Methodology & Pipeline

Step 1: Data Localization & KG Construction
Filtering global biomedical data alongside primary Bangladeshi clinical/somatic mutation profiles (MAF/VAF data) to construct standardized graph entities.

Step 2: R-GCN Model Pre-training
Training R-GCN models on the global knowledge graph to capture complex non-linear topological interactions via link prediction.

Step 3: Patient Personalization & Fine-Tuning
Dynamically reweighting graph edge weights using patient-specific Variant Allele Frequency (VAF) scores to adapt predictions for individual genomic profiles.

Step 4: Mechanistic XAI Extraction
Traversing the graph topology to extract human-readable molecular paths that medically justify every prioritized drug candidate.

Step 5: Rigorous Validation
Benchmarking performance using AUROC/AUPRC metrics, performing ablation studies, and cross-validating predictions with ClinicalTrials.gov and PubMed literature.

## Underexplored & Public Datasets

To ensure high model fidelity without compromising reproducibility, we utilize several underexplored and highly robust public datasets. All processing is strictly performed via Kaggle environments to eliminate local computational bottlenecks.

### 1. Open Targets Platform (Gene-Disease Associations)
Why we use it: Open Targets provides the most comprehensively curated genetic associations for Non-Small Cell Lung Carcinoma (MONDO:0005233). It is superior to older databases because it actively integrates multi-omics evidence.
Link: https://platform.opentargets.org

Python Snippet for Extraction:
```python
import requests
query = """
query {
  disease(efoId: "MONDO_0005233") {
    associatedTargets(page: {index: 0, size: 500}) {
      rows { target { id approvedSymbol } score }
    }
  }
}
"""
url = "https://api.platform.opentargets.org/api/v4/graphql"
response = requests.post(url, json={"query": query})
```

### 2. STRING API (Protein-Protein Interactions)
Why we use it: STRING provides physical and functional protein interaction networks. Instead of downloading static massive files, we use their v12 API to fetch dynamically updated network edges specifically for our identified NSCLC targets.
Link: https://string-db.org

Python Snippet for Extraction:
```python
import requests
url = "https://version-12-0.string-db.org/api/json/network"
params = {"identifiers": "TP53%0dEGFR", "species": 9606}
response = requests.post(url, data=params)
```

### 3. ChEMBL API (Drug-Target Interactions)
Why we use it: ChEMBL is highly underexplored in standard baseline GNNs which usually rely heavily on DrugBank. ChEMBL provides open-access, dynamic bioactivity data crucial for finding novel binding affinities.
Link: https://www.ebi.ac.uk/chembl/

Python Snippet for Extraction:
```python
import requests
url = "https://www.ebi.ac.uk/chembl/api/data/mechanism?target_component__accession=P00533&format=json"
res = requests.get(url)
```

### 4. Primary Dataset (Bangladeshi Patient Cohort)
Why we use it: This proprietary dataset injects localization into the global graph. It contains Variant Allele Frequencies (VAF) which will dynamically scale edge weights in the GNN. Note: Due to ethical constraints, raw patient data is not publicly shared in this repository.

## Comprehensive Literature Review

| Author & Reference | Dataset Used | Model / Algorithm Used | Key Limitations Identified |
| :--- | :--- | :--- | :--- |
| Ryu et al. (2026) [1] | OncoKB, PubMed, TxGNN KG, CPTAC | Rule-based Heuristic Prioritization (IDAP) | Relies on non-causal co-mentions; heuristic scores sensitive to weights; lacks deep XAI path extraction. |
| Perdomo-Quinteiro et al. (2026) [2] | NeDRex KG, DrugMechDB | Heterogeneous GraphSAGE + XAIPath | Path evaluation increases computation time exponentially; lacks patient-level multi-omics. |
| Khodadadi AghGhaleh et al. (2026) [3] | RepoDB, SIDER, STRING, DisGeNET | Word2Vec + Dual-Channel 1D-CNN | Relies on trial-and-error grid search; lacks an XAI module for human-readable pathway extraction. |
| Li & Xie (2026) [4] | TCGA, NCG, COSMIC, PPI | MNDGNN (Multiplex Directed GNN) | Identifies driver genes rather than drug repurposing candidates; noisy multiplex edges affect performance. |
| Gonzalez-Cavazos et al. (2026) [5] | MIND KG, DrugMechDB | DBR-X (Case-Based Reasoning + R-GCN) | Similarity retrieval relies on simple inner products; completely lacks localized genomic profiling. |
| Islam et al. (2023) [6] | NICRH Hospital Registry (Bangladesh) | Statistical Survival Analysis | Purely observational clinical dataset; lacks AI/GNN computational modeling or drug repurposing integration. |
| Aamer et al. (2026) [7] | PrimeKG, FDA Approvals | COMIC (Contrastive Masking) | Performance degrades on sparse graphs; DDI congestion obscures actual mechanistic paths. |
| Abo-Dahab et al. (2026) [8] | ChEMBL 36 | TransR, ComplEx, Heterogeneous GNN | Transductive setup limits performance on unobserved cold-start entities without topological context. |
| Xiong et al. (2025) [9] | BioSNAP, DrugBank, BindingDB | Geometric GNN (GPS-DTI) with CAM | Focuses solely on paired binding affinity rather than complex multi-layered patient Knowledge Graphs. |
| Khan et al. (2025) [10] | DrugBank, RCSB PDB | Molecular Docking & MD Simulations | Purely structural in silico approach; lacks population-specific patient multi-omics or GNN link prediction. |
| Wu et al. (2025) [11] | Multicenter NSCLC Cohort | Integrated ML Survival Framework | Focuses strictly on machine learning survival modeling; lacks explicit XAI graph path extraction. |

## Copyright and Uniqueness
This repository and the architectural concepts within are designed strictly to prevent plagiarism. The integration of localized VAF data with graph edge re-weighting in an R-GCN space is a novel approach completely unique to this research. All code is originally authored and copyright free.

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
