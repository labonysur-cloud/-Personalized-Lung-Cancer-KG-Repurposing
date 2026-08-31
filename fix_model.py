import json
import codecs

with codecs.open('src/models/BGLC_KG_Model_Training.ipynb', 'r', 'utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'code':
        # Fix cell 8 (uncomment ablation study)
        if any('Execute Ablation Studies' in line for line in cell['source']):
            new_source = []
            for line in cell['source']:
                if line.startswith('# results = {') or line.startswith('#     \"Baseline') or line.startswith('#     \"No Bio') or line.startswith('#     \"Single') or line.startswith('# }') or line.startswith('# df_ablation') or line.startswith('# print(') or line.startswith('# print(\"\\n--- Real'):
                    new_source.append(line.replace('# ', '', 1))
                elif line.startswith('# Execute Ablation Studies'):
                    new_source.append('# Execute Ablation Studies (Fully functional for Kaggle)\n')
                else:
                    new_source.append(line)
            cell['source'] = new_source

        # Fix cell 9 (missing extraction logic)
        elif any('Extraction of Novel Repurposing Candidates' in line for line in cell['source']):
            new_source = [
                "# 7. Knowledge Extraction: Top Novel Repurposing Candidates\n",
                "# We predict probabilities across ALL drugs for a specific target disease.\n\n",
                "print(\"\\n--- Extraction of Novel Repurposing Candidates ---\")\n",
                "model.eval()\n",
                "with torch.no_grad():\n",
                "    num_drugs = data['drug'].num_nodes\n",
                "    num_diseases = data['disease'].num_nodes\n",
                "    \n",
                "    # Target Disease: e.g., Disease Index 0 (Assuming it represents NSCLC EFO_0003060)\n",
                "    # We iterate over all drugs to find unmapped, high-probability connections.\n",
                "    target_disease_idx = 0\n",
                "    \n",
                "    candidate_drugs = torch.arange(num_drugs)\n",
                "    target_diseases = torch.full((num_drugs,), target_disease_idx, dtype=torch.long)\n",
                "    candidate_edge_label_index = torch.stack([candidate_drugs, target_diseases], dim=0).to(device)\n",
                "    \n",
                "    # Extract known indications to filter them out\n",
                "    known_edges = data[target_edge].edge_index\n",
                "    known_mask = known_edges[1] == target_disease_idx\n",
                "    known_drugs = set(known_edges[0][known_mask].numpy())\n",
                "    \n",
                "    # We use LinkNeighborLoader to generate the embeddings dynamically for candidate edges\n",
                "    candidate_loader = LinkNeighborLoader(\n",
                "        data,\n",
                "        num_neighbors=[15, 10],\n",
                "        edge_label_index=(target_edge, candidate_edge_label_index),\n",
                "        edge_label=torch.zeros(num_drugs), # dummy labels\n",
                "        batch_size=512,\n",
                "        shuffle=False,\n",
                "    )\n",
                "    \n",
                "    novel_preds = []\n",
                "    drug_indices = []\n",
                "    \n",
                "    for batch in candidate_loader:\n",
                "        batch = batch.to(device)\n",
                "        out = model(batch.x_dict, batch.edge_index_dict, batch[target_edge].edge_label_index)\n",
                "        probs = torch.sigmoid(out).cpu().numpy()\n",
                "        novel_preds.extend(probs)\n",
                "        drug_indices.extend(batch[target_edge].edge_label_index[0].cpu().numpy())\n",
                "        \n",
                "    results = []\n",
                "    for d_idx, prob in zip(drug_indices, novel_preds):\n",
                "        if d_idx not in known_drugs:\n",
                "            results.append({'Drug_Node_ID': d_idx, 'Predicted_Probability': prob})\n",
                "            \n",
                "    df_novel = pd.DataFrame(results).sort_values(by='Predicted_Probability', ascending=False)\n",
                "    \n",
                "    print(f\"\\nTop 10 Novel Repurposing Candidates for Disease Node {target_disease_idx}:\")\n",
                "    print(df_novel.head(10).to_string(index=False))\n",
                "    \n",
                "    out_path = os.path.join(MODEL_DIR, 'top_novel_candidates.csv')\n",
                "    df_novel.to_csv(out_path, index=False)\n",
                "    print(f\"\\nFull prediction list saved to {out_path}\")\n",
                "    print(\"\\nPipeline execution is 100% complete. Ready for target-specific XAI inference.\")\n"
            ]
            cell['source'] = new_source

with codecs.open('src/models/BGLC_KG_Model_Training.ipynb', 'w', 'utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
