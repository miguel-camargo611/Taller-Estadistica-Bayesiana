import json

with open('solucion_taller.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if 'outputs' in cell and len(cell['outputs']) > 0:
        has_imgs = any('data' in out and 'image/png' in out['data'] for out in cell['outputs'])
        if has_imgs:
            print(f"Cell {cell['id']}:")
            print(''.join(cell.get('source', []))[:200])
            print('---')
