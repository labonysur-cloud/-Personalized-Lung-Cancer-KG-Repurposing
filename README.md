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

| Author & Reference | Dataset Used | Dataset Format | Model / Algorithm Used | Accuracy / Performance | Key Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Ryu et al. (2026) | OncoKB, PubMed, TxGNN KG | Tabular, Graph Triples | Rule-based Heuristic Pipeline (IDAP) | Recovered matched therapy in 28/41 samples | Relies on co-mention (non-causal); lacks deep XAI path extraction. |
| Perdomo-Quinteiro et al. (2026) | NeDRex KG, DrugMechDB | Heterogeneous Graph | Heterogeneous GraphSAGE + XAIPath | AUROC > 0.95, Hits@1 = 0.71 | Simple path evaluation exponentially increases computation time; relies on existing KG without patient multi-omics. |
| Khodadadi AghGhaleh et al. (2026) | RepoDB, SIDER, STRING | Directed Multigraph | Word2Vec + Dual-Channel 1D-CNN | AUC-ROC = 0.9836, F1 = 0.9074 | Lacks an XAI module for human-readable biological pathway extraction. |
| Li & Xie (2026) | TCGA, NCG, COSMIC | Pan-cancer Multi-omics | MNDGNN (Multiplex Directed GNN) | AUROC = 0.8780, F1 = 0.8238 | Identifies driver genes rather than drug repurposing candidates. |
| Gonzalez-Cavazos et al. (2026)| MIND KG, DrugMechDB | Heterogeneous KG | DBR-X (Case-Based Reasoning + R-GCN) | MRR = 0.3770, Hits@1 = 0.2796 | Similarity retrieval relies on simple inner products; lacks localized genomic profiling. |
| Islam et al. (2023) | NICRH Hospital Registry | Clinical Records | Statistical Survival Analysis | Characterized demographic differentials | Observational clinical dataset; lacks AI/GNN integration. |

## Copyright and Uniqueness
This repository and the architectural concepts within are designed strictly to prevent plagiarism. The integration of localized VAF data with graph edge re-weighting in an R-GCN space is a novel approach completely unique to this research. All code is originally authored and copyright free.

## References
[1] Y. Ryu, H.-E. Jeong, and J.-Y. An, "IDAP: An integrated literature- and knowledge-graph-driven evidence prioritization pipeline for precision oncology," Bioinformatics, vol. 42, no. 5, art. no. btag300, 2026.
[2] P. Perdomo-Quinteiro, E. Guney, and A. Belmonte-Hernández, "Generating explainable hypotheses for drug repurposing with graph neural networks," Sci. Rep., vol. 16, p. 18840, 2026.
[3] M. Khodadadi AghGhaleh et al., "ConvAHKG: Action-based hybrid knowledge graph with a dual-channel convolutional approach for drug repurposing," Sci. Rep., vol. 16, p. 7592, 2026.
[4] P. Li and M. Xie, "Multiplex networks-based directed graph neural networks for cancer driver gene identification," PLOS Comput. Biol., vol. 22, no. 5, p. e1014275, 2026.
[5] A. C. Gonzalez-Cavazos, R. Tu, M. Sinha, and A. I. Su, "A case-based explainable graph neural network framework for mechanistic drug repositioning," Bioinformatics, vol. 42, no. 2, art. no. btag008, 2026.
[6] M. R. Islam et al., "Lung cancer in Bangladesh," J. Thorac. Oncol., vol. 18, no. 8, pp. 972–980, 2023.
