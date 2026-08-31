import json
import glob
import re

def clean_text(text):
    # Remove emojis (High surrogate ranges and specific emojis)
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    text = text.replace('??', '').replace('???', '').replace('??', '').replace('??', '').replace('?', '').replace('??', '')
    
    # Remove Bengali characters (Unicode block 0980-09FF)
    text = re.sub(r'[\u0980-\u09FF]', '', text)
    
    # Remove big dashes / decorative lines (e.g., # ----------)
    text = re.sub(r'# -{5,}', '#', text)
    
    # Clean up print statements like print("\n--- Text ---") to print("\nText")
    # This regex looks for '--- ' and ' ---' inside print statements and removes the dashes
    if 'print(' in text and '---' in text:
        text = text.replace('--- ', '').replace(' ---', '')
        
    return text

# Clean all Notebooks
for nb_file in glob.glob('src/**/*.ipynb', recursive=True):
    with open(nb_file, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    for cell in nb.get('cells', []):
        if 'source' in cell:
            cell['source'] = [clean_text(line) for line in cell['source']]
    with open(nb_file, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

# Clean README
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
readme = clean_text(readme)
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

print("Cleanup complete.")
