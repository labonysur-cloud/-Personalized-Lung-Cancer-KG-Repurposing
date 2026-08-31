import json
import codecs

with codecs.open('src/models/BGLC_KG_Model_Training.ipynb', 'r', 'utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'code' and any('--- ADVANCED REAL-TIME VISUALIZATIONS' in line for line in cell['source']):
        source = "".join(cell['source'])
        
        # 1. Update Heatmap to Top 30
        source = source.replace('top_15 = df_novel.head(15)', 'top_N = df_novel.head(30)')
        source = source.replace('Top 15', 'Top 30')
        source = source.replace('top_15', 'top_N')
        
        # 2. Update Subgraph to loop over Top 5
        subgraph_start = source.find('    # 4. Real-Time Knowledge Graph Connection')
        if subgraph_start != -1:
            new_subgraph = """    # 4. Real-Time Knowledge Graph Connection (Top 5 Candidates Subgraphs)
    print("\\n--- Plotting Real-Time Knowledge Graph Connections for Top 5 Candidates ---")
    for rank in range(5):
        top_drug_idx = int(top_N.iloc[rank]['Drug_Node_ID'])
        prob = top_N.iloc[rank]['Predicted_Probability']
        G_sub = nx.Graph()
        G_sub.add_node(f"Drug_{top_drug_idx}", color='red', size=800)
        G_sub.add_node(f"Disease_{target_disease_idx}", color='green', size=800)
        G_sub.add_edge(f"Drug_{top_drug_idx}", f"Disease_{target_disease_idx}", label=f"Predicted ({prob:.2f})")
        
        if ('drug', 'targets', 'gene') in data.edge_types:
            drug_targets_gene = data[('drug', 'targets', 'gene')].edge_index
            drug_mask = drug_targets_gene[0] == top_drug_idx
            for gene_idx in drug_targets_gene[1][drug_mask]:
                G_sub.add_node(f"Gene_{gene_idx.item()}", color='lightblue', size=500)
                G_sub.add_edge(f"Drug_{top_drug_idx}", f"Gene_{gene_idx.item()}", label="targets")
                
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G_sub, seed=42)
        colors = [nx.get_node_attributes(G_sub, 'color').get(n, 'grey') for n in G_sub.nodes()]
        sizes = [nx.get_node_attributes(G_sub, 'size').get(n, 500) for n in G_sub.nodes()]
        nx.draw(G_sub, pos, with_labels=True, node_color=colors, node_size=sizes, font_size=10, font_weight='bold', edge_color='gray')
        edge_labels = nx.get_edge_attributes(G_sub, 'label')
        nx.draw_networkx_edge_labels(G_sub, pos, edge_labels=edge_labels, font_size=8)
        plt.title(f"Rank {rank+1} Candidate Subgraph (Drug {top_drug_idx})", fontweight='bold')
        plt.savefig(os.path.join(VIS_DIR, f'realtime_kg_connection_rank_{rank+1}.png'), dpi=300)
        plt.close() # Close to prevent overlapping and save memory
        
    print("\\nPipeline execution and Visualizations 100% complete.")
"""
            source = source[:subgraph_start] + new_subgraph
            
        # Split back into proper lines
        cell['source'] = [line + '\n' for line in source.split('\n')]
        # Fix trailing newline issue
        if cell['source'][-1] == '\n':
            cell['source'].pop()

with codecs.open('src/models/BGLC_KG_Model_Training.ipynb', 'w', 'utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
