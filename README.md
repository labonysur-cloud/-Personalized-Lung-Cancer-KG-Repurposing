# -Personalized-Lung-Cancer-KG-Repurposing

XAI-driven GNN framework utilizing heterogeneous biomedical knowledge graphs to recommend personalized repurposed drugs based on clinical and somatic mutation profiles of Bangladeshi lung cancer patients.

## Standard project architecture

```text
├── data/
│   ├── raw/             ← downloaded raw database files
│   └── processed/       ← filtered nodes.csv and edges.csv
├── notebooks/
│   └── 1_data_preprocessing.ipynb  ← Kaggle-downloaded Jupyter notebook
├── src/
│   ├── graph_builder.py ← Python module for KG construction
│   └── gnn_model.py     ← Graph Neural Network code
└── README.md
```
