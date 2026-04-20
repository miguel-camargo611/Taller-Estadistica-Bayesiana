import json

with open('solucion_taller.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Buscar celdas con selección de variables / correlación / VIF
keywords = ['vif', 'corr', 'selec', 'multicollin', 'variable', 'feature', 'num_cols', 'cat_cols']
for cell in nb['cells']:
    src = ''.join(cell.get('source', []))
    if any(k in src.lower() for k in keywords):
        cell_id = cell.get('id', 'N/A')
        n_imgs = sum(1 for out in cell.get('outputs', []) if 'data' in out and 'image/png' in out.get('data', {}))
        print(f"CELL {cell_id} | imgs={n_imgs}")
        print(src[:300])
        print("---")
