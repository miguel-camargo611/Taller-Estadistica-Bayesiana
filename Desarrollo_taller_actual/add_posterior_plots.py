import json
import os

nb_path = r"c:\Users\Miguel Camargo\Desktop\Nuevo_Taller\Desarrollo_taller_actual\solucion_taller.ipynb"

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# 1. Update Part II to include az.plot_posterior
for i, cell in enumerate(nb["cells"]):
    if "az.plot_forest(trace, var_names=[\"beta\"]" in "".join(cell["source"]):
        # Create the new code cell for plot_posterior
        new_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Gráfico de Campanas (Distribución Posterior Completa)\n",
                "az.plot_posterior(trace, var_names=[\"beta\"], hdi_prob=0.95, color=\"teal\", figsize=(15, 8));\n",
                "plt.suptitle(\"Distribuciones Posteriores de los Coeficientes (Ordinal Logit)\", fontsize=16)\n",
                "plt.tight_layout()\n",
                "plt.show()"
            ]
        }
        # Insert it right after the forest plot cell
        nb["cells"].insert(i + 1, new_cell)
        break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("az.plot_posterior added to Part II.")
