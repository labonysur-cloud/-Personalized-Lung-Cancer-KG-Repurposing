import json
import codecs

with codecs.open('src/data_processing/BGLC_KG_Data_Pipeline.ipynb', 'r', 'utf-8') as f:
    data = json.load(f)

for cell in data['cells']:
    if cell['cell_type'] == 'code':
        new_source = []
        for line in cell['source']:
            if "return ('disease', None)" in line and len(new_source) >= 2 and 'asthma' in new_source[-1]:
                new_source.append('        n = node["name"].lower()\n')
                new_source.append('        if "lung" in n and ("cancer" in n or "carcinoma" in n or "neoplasm" in n):\n')
                new_source.append('            return ("disease", "EFO_0003060")\n')
                new_source.append('        return ("disease", None)\n')
            else:
                new_source.append(line)
        cell['source'] = new_source

with codecs.open('src/data_processing/BGLC_KG_Data_Pipeline.ipynb', 'w', 'utf-8') as f:
    json.dump(data, f, indent=1, ensure_ascii=False)
