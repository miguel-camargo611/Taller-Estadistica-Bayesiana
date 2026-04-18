import json

with open('solucion_taller.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if 'outputs' in cell:
        imgs = [i for i, out in enumerate(cell['outputs']) if 'data' in out and 'image/png' in out['data']]
        if imgs:
            source = ''.join(cell.get('source', []))
            print(f"CELL ID: {cell.get('id')}")
            print(f"Num images: {len(imgs)}")
            print(f"Source snippet: {source[:150]}")
            print("-" * 40)
