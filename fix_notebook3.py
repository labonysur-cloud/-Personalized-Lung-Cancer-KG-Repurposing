import json

with open('src/inference/BGLC_KG_Personalized_Inference.ipynb', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'code' and 'Dummy Patient Profile' in ''.join(cell['source']):
        new_source = [
            "# 4. Extracting Real Bangladeshi Population Profile (BEB Cohort)\n",
            "# INSTEAD OF A DUMMY PATIENT, we extract the actual highly frequent genetic variants\n",
            "# for the Bengali (BEB) population directly from the Knowledge Graph built in Notebook 1.\n",
            "\n",
            "print(\"\\n--- Extracting Real Bengali (BEB) Genomic Profile ---\")\n",
            "\n",
            "mutated_gene_indices = []\n",
            "profile_name = \"Real_Bangladeshi_BEB_Cohort\"\n",
            "\n",
            "if 'variant' in data.node_types and hasattr(data['variant'], 'x'):\n",
            "    # Index 0 in variant.x is BEB_AF (Bengali Allele Frequency)\n",
            "    # We filter variants that have a high frequency (> 5%) in Bangladesh\n",
            "    beb_af = data['variant'].x[:, 0]\n",
            "    frequent_beb_variants = (beb_af > 0.05).nonzero(as_tuple=True)[0]\n",
            "    \n",
            "    print(f\"Found {len(frequent_beb_variants)} highly frequent variants in the Bangladeshi population.\")\n",
            "    \n",
            "    if ('variant', 'affects', 'gene') in data.edge_types:\n",
            "        var_gene_edges = data[('variant', 'affects', 'gene')].edge_index\n",
            "        for v_idx in frequent_beb_variants:\n",
            "            mask = var_gene_edges[0] == v_idx\n",
            "            genes = var_gene_edges[1][mask].tolist()\n",
            "            mutated_gene_indices.extend(genes)\n",
            "        mutated_gene_indices = list(set(mutated_gene_indices))\n",
            "\n",
            "# Fallback to general highly connected lung cancer genes if variant linking is sparse\n",
            "if len(mutated_gene_indices) == 0:\n",
            "    print(\"Using core topological NSCLC target genes for baseline...\")\n",
            "    if ('drug', 'targets', 'gene') in data.edge_types:\n",
            "        gene_degrees = torch.bincount(data[('drug', 'targets', 'gene')].edge_index[1])\n",
            "        mutated_gene_indices = torch.topk(gene_degrees, k=5).indices.tolist()\n",
            "\n",
            "patient_profile = {\n",
            "    'patient_id': profile_name,\n",
            "    'mutated_gene_indices': mutated_gene_indices\n",
            "}\n",
            "\n",
            "print(f\"Profile ID: {patient_profile['patient_id']}\")\n",
            "print(f\"Extracted Gene Graph Indices for Personalization: {patient_profile['mutated_gene_indices']}\")\n"
        ]
        cell['source'] = new_source

with open('src/inference/BGLC_KG_Personalized_Inference.ipynb', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
