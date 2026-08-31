import json
import codecs

with codecs.open('src/models/BGLC_KG_Model_Training.ipynb', 'r', 'utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'code':
        if any('Extraction of Novel Repurposing Candidates' in line for line in cell['source']):
            new_source = []
            for line in cell['source']:
                new_source.append(line)
                if "print(\"\\nPipeline execution is 100% complete" in line:
                    new_source.pop() # Remove the last print, we'll append more
                    
                    vis_code = [
                        "\n    # --- ADVANCED REAL-TIME VISUALIZATIONS (PURE REAL DATA) ---\n",
                        "    import networkx as nx\n",
                        "    import seaborn as sns\n",
                        "    import matplotlib.pyplot as plt\n",
                        "    \n",
                        "    print(\"\\n--- Generating Real-Time Data Visualizations ---\")\n",
                        "    fig, axes = plt.subplots(1, 2, figsize=(18, 7))\n",
                        "    \n",
                        "    # 1. Drug Mapping: Top 15 Candidates Probability Bar Plot\n",
                        "    top_15 = df_novel.head(15)\n",
                        "    sns.barplot(data=top_15, x='Predicted_Probability', y='Drug_Node_ID', ax=axes[0], palette='viridis', orient='h')\n",
                        "    axes[0].set_title('Top 15 Novel Drug Mapping (Probability Heatmap)', fontweight='bold')\n",
                        "    axes[0].set_xlabel('GNN Predicted Probability')\n",
                        "    axes[0].set_ylabel('Drug Node ID')\n",
                        "    \n",
                        "    # 2. Benchmarking: Density Plot of Probabilities\n",
                        "    known_probs = []\n",
                        "    for batch in test_loader:\n",
                        "        batch = batch.to(device)\n",
                        "        out = model(batch.x_dict, batch.edge_index_dict, batch[target_edge].edge_label_index)\n",
                        "        known_probs.extend(torch.sigmoid(out).cpu().numpy())\n",
                        "        \n",
                        "    sns.kdeplot(known_probs, fill=True, color='blue', label='Test Set (Known Benchmarks)', ax=axes[1])\n",
                        "    sns.kdeplot(novel_preds, fill=True, color='red', label='Novel Unseen Candidates', ax=axes[1])\n",
                        "    axes[1].set_title('Benchmarking: Probability Distribution Heatmap', fontweight='bold')\n",
                        "    axes[1].set_xlabel('Probability Score')\n",
                        "    axes[1].set_ylabel('Density')\n",
                        "    axes[1].legend()\n",
                        "    \n",
                        "    plt.tight_layout()\n",
                        "    plt.savefig(os.path.join(VIS_DIR, 'drug_mapping_and_benchmarking.png'), dpi=300)\n",
                        "    plt.show()\n",
                        "    \n",
                        "    # 3. Volcano Map (Probability vs Graph Connectivity)\n",
                        "    print(\"\\n--- Generating Prediction Volcano Map ---\")\n",
                        "    drug_degrees = torch.bincount(data[target_edge].edge_index[0], minlength=num_drugs).cpu().numpy()\n",
                        "    if ('drug', 'targets', 'gene') in data.edge_types:\n",
                        "        drug_degrees += torch.bincount(data[('drug', 'targets', 'gene')].edge_index[0], minlength=num_drugs).cpu().numpy()\n",
                        "        \n",
                        "    results_df = df_novel.copy()\n",
                        "    results_df['Graph_Connectivity'] = np.log2(drug_degrees[results_df['Drug_Node_ID'].values] + 1)\n",
                        "    results_df['is_top'] = ['Top Candidate' if i < 15 else 'Other' for i in range(len(results_df))]\n",
                        "    \n",
                        "    plt.figure(figsize=(10, 6))\n",
                        "    sns.scatterplot(data=results_df, x='Predicted_Probability', y='Graph_Connectivity', hue='is_top', palette={'Top Candidate': 'red', 'Other': 'grey'}, alpha=0.7)\n",
                        "    plt.axvline(x=0.5, color='blue', linestyle='--', label='Decision Threshold (0.5)')\n",
                        "    plt.title('Prediction Volcano Map (Probability vs Topological Connectivity)', fontweight='bold')\n",
                        "    plt.xlabel('GNN Predicted Probability')\n",
                        "    plt.ylabel('Log2(Drug Graph Connectivity)')\n",
                        "    plt.legend()\n",
                        "    plt.savefig(os.path.join(VIS_DIR, 'volcano_map.png'), dpi=300)\n",
                        "    plt.show()\n",
                        "    \n",
                        "    # 4. Real-Time Knowledge Graph Connection (Top Candidate Subgraph)\n",
                        "    print(\"\\n--- Plotting Real-Time Knowledge Graph Connection ---\")\n",
                        "    top_drug_idx = int(top_15.iloc[0]['Drug_Node_ID'])\n",
                        "    G_sub = nx.Graph()\n",
                        "    G_sub.add_node(f\"Drug_{top_drug_idx}\", color='red', size=800)\n",
                        "    G_sub.add_node(f\"Disease_{target_disease_idx}\", color='green', size=800)\n",
                        "    G_sub.add_edge(f\"Drug_{top_drug_idx}\", f\"Disease_{target_disease_idx}\", label=f\"Predicted ({top_15.iloc[0]['Predicted_Probability']:.2f})\")\n",
                        "    \n",
                        "    if ('drug', 'targets', 'gene') in data.edge_types:\n",
                        "        drug_targets_gene = data[('drug', 'targets', 'gene')].edge_index\n",
                        "        drug_mask = drug_targets_gene[0] == top_drug_idx\n",
                        "        for gene_idx in drug_targets_gene[1][drug_mask]:\n",
                        "            G_sub.add_node(f\"Gene_{gene_idx.item()}\", color='lightblue', size=500)\n",
                        "            G_sub.add_edge(f\"Drug_{top_drug_idx}\", f\"Gene_{gene_idx.item()}\", label=\"targets\")\n",
                        "            \n",
                        "    plt.figure(figsize=(10, 8))\n",
                        "    pos = nx.spring_layout(G_sub, seed=42)\n",
                        "    colors = [nx.get_node_attributes(G_sub, 'color').get(n, 'grey') for n in G_sub.nodes()]\n",
                        "    sizes = [nx.get_node_attributes(G_sub, 'size').get(n, 500) for n in G_sub.nodes()]\n",
                        "    nx.draw(G_sub, pos, with_labels=True, node_color=colors, node_size=sizes, font_size=10, font_weight='bold', edge_color='gray')\n",
                        "    edge_labels = nx.get_edge_attributes(G_sub, 'label')\n",
                        "    nx.draw_networkx_edge_labels(G_sub, pos, edge_labels=edge_labels, font_size=8)\n",
                        "    plt.title(\"Real-Time Knowledge Graph Connection (Top Candidate Subgraph)\", fontweight='bold')\n",
                        "    plt.savefig(os.path.join(VIS_DIR, 'realtime_kg_connection.png'), dpi=300)\n",
                        "    plt.show()\n",
                        "    \n",
                        "    print(\"\\nPipeline execution and Visualizations 100% complete.\")\n"
                    ]
                    new_source.extend(vis_code)
            cell['source'] = new_source

with codecs.open('src/models/BGLC_KG_Model_Training.ipynb', 'w', 'utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
