import json

with open('solucion_taller.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Extraer texto de la tabla de resultados NIG (celda 1894a5c0)
for cell in nb['cells']:
    if cell.get('id') in ['1894a5c0', 'b84ee4a1', '89ccc1da']:
        print(f"=== CELL {cell['id']} ===")
        for out in cell.get('outputs', []):
            if 'text' in out:
                print(''.join(out['text'])[:600])
            if 'data' in out and 'text/html' in out['data']:
                print("HTML TABLE OUTPUT - truncated")
                print(''.join(out['data']['text/html'])[:800])
        print()
