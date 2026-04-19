import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs('imagenes', exist_ok=True)

# Parámetros analíticos exactos de las curvas Posteriores de UBER (NIG)
stats = [
    {"name": "Intercept", "mean": 16874.0, "lo": 13157.0, "hi": 20591.0},
    {"name": r"treat ($\beta_1$)", "mean": -1253.0, "lo": -2371.0, "hi": -135.0},
    {"name": "commute", "mean": 5455.0, "lo": 3009.0, "hi": 7900.0},
    {"name": "matches", "mean": 4387.0, "lo": 2890.0, "hi": 5883.0}
]

np.random.seed(42)
for i, st in enumerate(stats):
    mean = st["mean"]
    # Reversando la desviación estándar del límite superior HDI 95% (asumiendo Normalidad NIG posterior aproximada)
    std = (st["hi"] - st["mean"]) / 1.96
    
    s = np.random.normal(loc=mean, scale=std, size=20000)
    lo, hi = np.percentile(s, [2.5, 97.5])
    
    plt.figure(figsize=(6,4))
    plt.hist(s, bins=80, density=True, color='#5b9bd5', alpha=0.8, ec='white')
    plt.axvline(mean, color='red', lw=2, label=f'Media: {mean:.1f}')
    plt.axvline(lo, color='orange', lw=1.5, ls='--', label=f'2.5%: {lo:.1f}')
    plt.axvline(hi, color='orange', lw=1.5, ls='--', label=f'97.5%: {hi:.1f}')
    
    plt.title(f'Posterior: {st["name"]}', fontsize=12, fontweight='bold')
    plt.legend(fontsize=9)
    plt.tight_layout()
    plt.savefig(f'imagenes/uber_post_{i}.png', dpi=200)
    plt.close()

print("Imágenes generadas correctamente en la carpeta /imagenes/")
