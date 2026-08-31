import json
import codecs

with codecs.open('src/data_processing/BGLC_KG_Data_Pipeline.ipynb', 'r', 'utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'code':
        if any('Phase 10: Graph Integrity Report & Metagraph Export' in line for line in cell['source']):
            new_source = []
            for line in cell['source']:
                new_source.append(line)
                if "print(\"Pipeline complete!" in line:
                    new_source.pop() # Remove final print
                    
                    vis_code = [
                        "\n    # --- ADVANCED EXPLORATORY DATA ANALYSIS (PURE REAL DATA) ---\n",
                        "    print(\"\\n--- Generating Real-Time Data Pipeline Visualizations ---\")\n",
                        "    import seaborn as sns\n",
                        "    sns.set_theme(style=\"whitegrid\")\n",
                        "    fig, axes = plt.subplots(2, 2, figsize=(18, 14))\n",
                        "    \n",
                        "    # 1. Node Types Distribution\n",
                        "    node_counts = {n: data[n].num_nodes for n in data.node_types}\n",
                        "    sns.barplot(x=list(node_counts.keys()), y=list(node_counts.values()), ax=axes[0, 0], palette=\"cubehelix\")\n",
                        "    axes[0, 0].set_title('Knowledge Graph Node Demographics', fontweight='bold')\n",
                        "    axes[0, 0].set_ylabel('Total Count')\n",
                        "    axes[0, 0].tick_params(axis='x', rotation=45)\n",
                        "    \n",
                        "    # 2. Edge Types Distribution\n",
                        "    edge_counts = {f\"{e[0]}->{e[2]}\": data[e].edge_index.shape[1] for e in data.edge_types}\n",
                        "    sns.barplot(x=list(edge_counts.values()), y=list(edge_counts.keys()), ax=axes[0, 1], palette=\"magma\", orient='h')\n",
                        "    axes[0, 1].set_title('Topological Edge Density', fontweight='bold')\n",
                        "    axes[0, 1].set_xlabel('Number of Connections')\n",
                        "    \n",
                        "    # 3. Genomic Population Frequencies (BEB vs SAS) - Core Localization Metrics\n",
                        "    if 'variant' in data.node_types and hasattr(data['variant'], 'x') and hasattr(data['variant'], 'af_available'):\n",
                        "        beb_af = data['variant'].x[data['variant'].af_available[:, 0], 0].numpy()\n",
                        "        sas_af = data['variant'].x[data['variant'].af_available[:, 1], 1].numpy()\n",
                        "        if len(beb_af) > 0 and len(sas_af) > 0:\n",
                        "            sns.kdeplot(beb_af, fill=True, color='red', label='Bengali (BEB)', ax=axes[1, 0], alpha=0.5)\n",
                        "            sns.kdeplot(sas_af, fill=True, color='blue', label='South Asian (SAS)', ax=axes[1, 0], alpha=0.5)\n",
                        "            axes[1, 0].set_title('Variant Allele Frequency (Population Localization)', fontweight='bold')\n",
                        "            axes[1, 0].set_xlabel('Allele Frequency')\n",
                        "            axes[1, 0].set_ylabel('Density')\n",
                        "            axes[1, 0].legend()\n",
                        "    \n",
                        "    # 4. Drug Clinical Phase Distribution\n",
                        "    if 'drug' in data.node_types and hasattr(data['drug'], 'x'):\n",
                        "        phases = data['drug'].x[:, 129].numpy()\n",
                        "        sns.histplot(phases, bins=5, color='teal', ax=axes[1, 1], discrete=True)\n",
                        "        axes[1, 1].set_title('ChEMBL Drug Clinical Phases', fontweight='bold')\n",
                        "        axes[1, 1].set_xlabel('Max Clinical Phase (0=Preclinical, 4=Approved)')\n",
                        "        axes[1, 1].set_ylabel('Total Count')\n",
                        "    \n",
                        "    plt.tight_layout()\n",
                        "    plt.savefig(os.path.join(FIGURES_DIR, 'pipeline_data_distributions.png'), dpi=300)\n",
                        "    plt.show()\n",
                        "    \n",
                        "    # 5. Protein-Protein Interaction Hub (STRING Subgraph snippet)\n",
                        "    print(\"\\n--- Plotting Core Protein-Protein Interaction Hub ---\")\n",
                        "    if ('protein', 'interacts_with', 'protein') in data.edge_types:\n",
                        "        ppi_edges = data[('protein', 'interacts_with', 'protein')].edge_index\n",
                        "        G_ppi = nx.Graph()\n",
                        "        # Sub-sample highly connected nodes for clarity to avoid a hairball\n",
                        "        for i in range(min(200, ppi_edges.shape[1])):\n",
                        "            u, v = ppi_edges[0, i].item(), ppi_edges[1, i].item()\n",
                        "            G_ppi.add_edge(f\"P_{u}\", f\"P_{v}\")\n",
                        "        \n",
                        "        plt.figure(figsize=(10, 8))\n",
                        "        degrees = dict(G_ppi.degree())\n",
                        "        node_sizes = [v * 60 for v in degrees.values()]\n",
                        "        pos_ppi = nx.spring_layout(G_ppi, k=0.5, seed=42)\n",
                        "        nx.draw(G_ppi, pos_ppi, node_size=node_sizes, node_color='purple', edge_color='lightgray', alpha=0.8, with_labels=False)\n",
                        "        plt.title(\"Core Protein-Protein Interaction Hub (STRING Network Subset)\", fontweight='bold')\n",
                        "        plt.savefig(os.path.join(FIGURES_DIR, 'ppi_hub_subgraph.png'), dpi=300)\n",
                        "        plt.show()\n",
                        "    \n",
                        "    print(\"\\nPipeline complete! Validated HeteroData and advanced visual artifacts saved.\")\n"
                    ]
                    new_source.extend(vis_code)
            cell['source'] = new_source

with codecs.open('src/data_processing/BGLC_KG_Data_Pipeline.ipynb', 'w', 'utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
