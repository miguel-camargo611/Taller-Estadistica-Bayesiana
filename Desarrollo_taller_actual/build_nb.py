"""Script to rebuild solucion_taller.ipynb using nbformat for guaranteed VS Code compatibility."""
import nbformat
import os

path = os.path.join(os.path.dirname(__file__), "solucion_taller.ipynb")

def md(text):
    return nbformat.v4.new_markdown_cell(text)

def code(text):
    c = nbformat.v4.new_code_cell(text)
    c.outputs = []
    c.execution_count = None
    return c

cells = []

# ── Portada ──────────────────────────────────────────────────────────────────
cells.append(md(
    "# Taller Integrado de Regresión Bayesiana\n"
    "## Caso UBER Pool y Venta de Boletas en el Movistar Arena\n\n"
    "**Estudiantes:** Miguel Camargo, Nicolas Cardenas y Camilo Hernandez  \n"
    "**Curso:** Estadística Bayesiana — Universidad Externado de Colombia  \n"
    "**Fecha:** 2026\n\n---"
))

# ── Imports ───────────────────────────────────────────────────────────────────
cells.append(md("## 1. Configuración Inicial e Importación de Librerías"))
cells.append(code(
    "import numpy as np\n"
    "import pandas as pd\n"
    "import scipy.stats as stats\n"
    "from scipy.special import expit\n"
    "import matplotlib.pyplot as plt\n"
    "import seaborn as sns\n"
    "import pymc as pm\n"
    "import arviz as az\n"
    "import warnings\n"
    "warnings.filterwarnings('ignore')\n\n"
    "sns.set_theme(style='whitegrid', palette='muted')\n"
    "az.style.use('arviz-darkgrid')\n"
    "plt.rcParams['figure.figsize'] = (10, 6)\n"
    "print(f'PyMC version: {pm.__version__}')\n"
    "print(f'ArviZ version: {az.__version__}')"
))

# ── PARTE I ───────────────────────────────────────────────────────────────────
cells.append(md(
    "---\n"
    "## Parte I: Regresión Lineal Bayesiana — UBER Pool\n\n"
    "UBER desea cuantificar si su campaña de UBER Pool (`treat=True`) afectó el pago total al conductor "
    "(`total_driver_payout`). Usamos la familia conjugada **Normal-Inversa-Gamma** para obtener la "
    "distribución *a posteriori* exacta (sin MCMC)."
))

cells.append(md("### 1.1 Carga de Datos"))
cells.append(code(
    "df_uber = pd.read_excel('../Taller actual/BaseUBER.xlsx')\n"
    "df_uber['total_matches_thousands'] = df_uber['total_matches'] / 1000\n"
    "print(f'Dataset UBER: {df_uber.shape[0]} registros')\n"
    "df_uber.head()"
))

cells.append(code(
    "df_uber['Intercept'] = 1\n"
    "variables = ['Intercept', 'treat', 'commute', 'total_matches_thousands']\n"
    "X = df_uber[variables].values.astype(float)\n"
    "y = df_uber['total_driver_payout'].values.astype(float)\n"
    "n, p = X.shape\n"
    "print(f'n={n}, p={p}')\n"
    "print(f'Variables: {variables}')"
))

cells.append(md(
    "### 1.2 Solución Analítica Cerrada: Normal-Inversa-Gamma\n\n"
    "El modelo es:\n"
    r"$$\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}, "
    r"\quad \boldsymbol{\varepsilon} \sim \mathcal{N}(0, \sigma^2 \mathbf{I})$$"
    "\n\nFórmulas de actualización:\n"
    r"$$\mathbf{V}_n = \left(\mathbf{V}_0^{-1} + \mathbf{X}^\top \mathbf{X}\right)^{-1},"
    r"\quad \boldsymbol{\beta}_n = \mathbf{V}_n \left(\mathbf{V}_0^{-1}\boldsymbol{\beta}_0 + \mathbf{X}^\top \mathbf{y}\right)$$"
    "\n"
    r"$$a_n = a_0 + \frac{n}{2}, \quad b_n = b_0 + \frac{1}{2}\left(\mathbf{y}^\top\mathbf{y} + "
    r"\boldsymbol{\beta}_0^\top\mathbf{V}_0^{-1}\boldsymbol{\beta}_0 - "
    r"\boldsymbol{\beta}_n^\top\mathbf{V}_n^{-1}\boldsymbol{\beta}_n\right)$$"
    "\n\n**Priors difusos:** $\\boldsymbol{\\beta}_0=\\mathbf{0}$, $\\kappa_0=10^{-8}$, $a_0=2$."
))

cells.append(code(
    "# Hiperparámetros Prior (difusos)\n"
    "beta_0  = np.zeros(p)\n"
    "kappa_0 = 1e-8\n"
    "V_0     = (1.0 / kappa_0) * np.eye(p)\n"
    "a_0     = 2.0\n"
    "b_0     = np.var(y) * (a_0 - 1)\n\n"
    "# Actualización Analítica\n"
    "V_0_inv = np.linalg.inv(V_0)\n"
    "XtX     = X.T @ X\n"
    "Xty     = X.T @ y\n"
    "V_n_inv = V_0_inv + XtX\n"
    "V_n     = np.linalg.inv(V_n_inv)\n"
    "beta_n  = V_n @ (V_0_inv @ beta_0 + Xty)\n"
    "a_n     = a_0 + n / 2.0\n"
    "b_n     = b_0 + 0.5 * (y @ y + beta_0 @ V_0_inv @ beta_0 - beta_n @ V_n_inv @ beta_n)\n"
    "sigma2_post_mean = b_n / (a_n - 1)\n\n"
    "print('=' * 50)\n"
    "print('PARÁMETROS DE LA DISTRIBUCIÓN POSTERIOR')\n"
    "print('=' * 50)\n"
    "print(f'  a_n = {a_n:.2f},  b_n = {b_n:.2f}')\n"
    "print(f'  E[sigma^2 | y] = {sigma2_post_mean:.2f}')\n"
    "print()\n"
    "for name, val in zip(variables, beta_n):\n"
    "    print(f'  {name:30s} = {val:12.4f}')"
))

cells.append(md("### 1.3 Intervalos de Credibilidad al 95%"))
cells.append(code(
    "scale_marginal = np.sqrt((b_n / a_n) * np.diag(V_n))\n"
    "df_t   = 2 * a_n\n"
    "t_crit = stats.t.ppf(0.975, df=df_t)\n\n"
    "results = pd.DataFrame({\n"
    "    'Variable'   : variables,\n"
    "    'Media Post.' : beta_n,\n"
    "    'CrI 95% Inf' : beta_n - t_crit * scale_marginal,\n"
    "    'CrI 95% Sup' : beta_n + t_crit * scale_marginal,\n"
    "}).set_index('Variable')\n"
    "print(results.round(2))"
))

cells.append(md(
    "**Interpretación:**\n"
    "- **treat**: Efecto medio ≈ −1,253. El CrI 95% es completamente negativo: UBER Pool **redujo** el pago al conductor.\n"
    "- **total_matches_thousands**: Fuerte efecto positivo (~9,800 por cada 1,000 matches), confirmando economía de escala."
))

cells.append(md("### 1.4 Muestreo de la Posterior NIG y Visualización"))
cells.append(code(
    "np.random.seed(42)\n"
    "N = 50_000\n\n"
    "# Paso 1: sigma^2 ~ Inv-Gamma(a_n, b_n)\n"
    "sigma2_s = 1.0 / np.random.gamma(shape=a_n, scale=1.0/b_n, size=N)\n\n"
    "# Paso 2: beta | sigma^2 ~ Normal(beta_n, sigma^2 * V_n)\n"
    "L = np.linalg.cholesky(V_n)\n"
    "z = np.random.randn(N, p)\n"
    "beta_s = beta_n + np.sqrt(sigma2_s[:, None]) * (z @ L.T)\n\n"
    "prob_neg = (beta_s[:, 1] < 0).mean()\n"
    "print(f'P(beta_treat < 0 | y) = {prob_neg:.4f} ({prob_neg*100:.1f}%)')\n\n"
    "fig, axes = plt.subplots(1, p, figsize=(16, 4))\n"
    "for i, (ax, name) in enumerate(zip(axes, variables)):\n"
    "    s = beta_s[:, i]\n"
    "    lo, hi = np.percentile(s, [2.5, 97.5])\n"
    "    ax.hist(s, bins=80, density=True, color='#5b9bd5', alpha=0.8, ec='white')\n"
    "    ax.axvline(s.mean(), color='red', lw=2, label=f'Media: {s.mean():.1f}')\n"
    "    ax.axvline(lo, color='orange', lw=1.5, ls='--', label=f'2.5%: {lo:.1f}')\n"
    "    ax.axvline(hi, color='orange', lw=1.5, ls='--', label=f'97.5%: {hi:.1f}')\n"
    "    ax.set_title(f'Posterior: {name}', fontsize=11)\n"
    "    ax.legend(fontsize=7)\n"
    "plt.suptitle('Distribuciones Posteriores de β — NIG', fontsize=13, y=1.02)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(md("### 1.5 Chequeo Residual"))
cells.append(code(
    "y_hat = X @ beta_n\n"
    "res   = y - y_hat\n"
    "plt.figure(figsize=(9, 5))\n"
    "sns.scatterplot(x=y_hat, y=res, alpha=0.8, color='navy')\n"
    "plt.axhline(0, color='crimson', ls='--')\n"
    "plt.title('Residuos vs Valores Ajustados')\n"
    "plt.xlabel('Fitted')\n"
    "plt.ylabel('Residuales')\n"
    "plt.show()"
))

# ── PARTE II ──────────────────────────────────────────────────────────────────
cells.append(md(
    "---\n"
    "## Parte II: Regresión Logística Ordinal Bayesiana — Movistar Arena\n\n"
    "Variable respuesta `Customer_Type` con orden natural: "
    "`Last-Minute` (0) < `In-Between` (1) < `Planner` (2)."
))

cells.append(md("### 2.1 Carga de Datos y EDA"))
cells.append(code(
    "df_arena = pd.read_excel('../Taller actual/movistar.xlsx')\n"
    "order    = ['Last-Minute', 'In-Between', 'Planner']\n"
    "num_cols = ['Age', 'Num_Tickets_Purchased', 'Ticket_Price',\n"
    "            'Concession_Purchases', 'Days_Before_Concierto']\n"
    "cat_cols = ['Fan_Mailing_List', 'Seat_Location']\n"
    "print(f'Dataset: {df_arena.shape[0]} registros')\n"
    "df_arena.head()"
))

cells.append(code(
    "fig, axs = plt.subplots(3, 2, figsize=(16, 18))\n"
    "axs = axs.flatten()\n"
    "print('--- Kruskal-Wallis ---')\n"
    "for i, col in enumerate(num_cols):\n"
    "    df_arena[col] = pd.to_numeric(df_arena[col], errors='coerce')\n"
    "    sns.boxplot(data=df_arena, x='Customer_Type', y=col, order=order,\n"
    "                ax=axs[i], palette='viridis')\n"
    "    axs[i].set_title(f'{col} por Tipo de Cliente', fontsize=12)\n"
    "    groups = [df_arena[df_arena['Customer_Type']==ct][col].dropna() for ct in order]\n"
    "    _, pv = stats.kruskal(*groups)\n"
    "    sig = '*' if pv < 0.05 else ''\n"
    "    print(f'  {col:30s}: p={pv:.3e} {sig}')\n"
    "if len(num_cols) < len(axs):\n"
    "    fig.delaxes(axs[-1])\n"
    "plt.tight_layout()\n"
    "plt.show()\n\n"
    "print('\\n--- Chi-cuadrado ---')\n"
    "for col in cat_cols:\n"
    "    ct = pd.crosstab(df_arena['Customer_Type'], df_arena[col])\n"
    "    _, pv, *_ = stats.chi2_contingency(ct)\n"
    "    sig = '*' if pv < 0.05 else ''\n"
    "    print(f'  {col:30s}: p={pv:.3e} {sig}')\n"
    "    pct = pd.crosstab(df_arena['Customer_Type'], df_arena[col], normalize='index')\n"
    "    pct.loc[order].plot(kind='bar', stacked=True, figsize=(8, 4), colormap='Accent')\n"
    "    plt.title(f'Proporción de {col}')\n"
    "    plt.ylabel('Prop.')\n"
    "    plt.legend(bbox_to_anchor=(1.05, 1))\n"
    "    plt.show()"
))

cells.append(md(
    "### 2.2 Modelo Ordinal Bayesiano\n\n"
    r"$$P(Y_i \leq k | \mathbf{X}_i) = \sigma(\theta_k - \mathbf{X}_i\boldsymbol{\beta})$$"
    "\n\n**Priors:** "
    r"$\beta \sim \mathcal{N}(0,1)$, $\sigma_{cp} \sim \text{Exp}(1)$, "
    r"$\boldsymbol{\theta} \sim \mathcal{N}(0, \sigma_{cp})$ con transformación ordenada."
))

cells.append(code(
    "mapping = {'Last-Minute': 0, 'In-Between': 1, 'Planner': 2}\n"
    "df_arena['Y_ordinal']      = pd.to_numeric(\n"
    "    df_arena['Customer_Type'].map(mapping), downcast='integer')\n"
    "df_arena['Fan_Mailing_Yes'] = (df_arena['Fan_Mailing_List'] == 'Yes').astype(int)\n"
    "df_arena['Seat_Front']      = (df_arena['Seat_Location'] == 'Front').astype(int)\n"
    "df_arena['Seat_Balcony']    = (df_arena['Seat_Location'] == 'Balcony').astype(int)\n\n"
    "features = ['Age', 'Num_Tickets_Purchased', 'Ticket_Price',\n"
    "            'Concession_Purchases', 'Fan_Mailing_Yes', 'Seat_Front', 'Seat_Balcony']\n"
    "X_arena = df_arena[features].copy()\n"
    "for f in ['Age', 'Num_Tickets_Purchased', 'Ticket_Price', 'Concession_Purchases']:\n"
    "    X_arena[f] = (X_arena[f] - X_arena[f].mean()) / X_arena[f].std()\n\n"
    "X_mat = X_arena.values\n"
    "y_ord = df_arena['Y_ordinal'].values\n"
    "k_classes, n_pred = 3, X_mat.shape[1]\n"
    "print(f'Shape: {X_mat.shape}')\n"
    "print(f'Y dist: {dict(pd.Series(y_ord).value_counts().sort_index())}')"
))

cells.append(code(
    "with pm.Model() as ordinal_model:\n"
    "    beta      = pm.Normal('beta', mu=0, sigma=1, shape=n_pred)\n"
    "    sigma_cp  = pm.Exponential('sigma_cp', lam=1)\n"
    "    cutpoints = pm.Normal(\n"
    "        'cutpoints', mu=0, sigma=sigma_cp,\n"
    "        transform=pm.distributions.transforms.ordered,\n"
    "        shape=k_classes - 1,\n"
    "        initval=np.array([-1.0, 1.0])\n"
    "    )\n"
    "    eta   = pm.math.dot(X_mat, beta)\n"
    "    y_obs = pm.OrderedLogistic('y_obs', eta=eta, cutpoints=cutpoints, observed=y_ord)\n"
    "    trace = pm.sample(draws=10_000, tune=2_000, chains=4, target_accept=0.9, random_seed=42)"
))

cells.append(md("### 2.3 Diagnóstico MCMC"))
cells.append(code(
    "az.plot_trace(trace, var_names=['cutpoints'])\n"
    "plt.tight_layout()\n"
    "plt.show()"
))
cells.append(code(
    "summary_diag = az.summary(trace, var_names=['beta', 'cutpoints', 'sigma_cp'])\n"
    "print(summary_diag[['mean','sd','hdi_3%','hdi_97%','r_hat','ess_bulk']].round(3))"
))

cells.append(md("### 2.4 Resultados"))
cells.append(code(
    "res_ord = az.summary(trace, var_names=['beta', 'cutpoints'])\n"
    "res_ord.index = features + ['cutpoint_0', 'cutpoint_1']\n"
    "res_ord[['mean','sd','hdi_3%','hdi_97%']].round(3)"
))

cells.append(md(
    "**Interpretación Estadística:**\n"
    "- Los **puntos de corte** conservan el orden $\\theta_1 < \\theta_2$, particionando correctamente el espacio latente.\n"
    "- **Edad** y **Compras en Concesión** impulsan valores positivos: mayor propensión a ser *Planner*.\n"
    "- Los **94% HDI** cuantifican la incertidumbre Bayesiana de cada efecto."
))

cells.append(md("### 2.5 Distribuciones Posteriores"))
cells.append(code(
    "az.plot_forest(trace, var_names=['beta'], combined=True, figsize=(10, 6))\n"
    "plt.title('94% HDI — Beta en Ordinal Logit')\n"
    "plt.show()"
))
cells.append(code(
    "az.plot_posterior(trace, var_names=['beta'], hdi_prob=0.95, color='teal', figsize=(16, 9))\n"
    "plt.suptitle('Distribuciones Posteriores de los Coeficientes β', fontsize=15)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))
cells.append(code(
    "az.plot_posterior(trace, var_names=['cutpoints'], hdi_prob=0.95, color='coral', figsize=(10, 4))\n"
    "plt.suptitle('Distribuciones Posteriores de los Cutpoints θ', fontsize=14)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(md("### 2.6 Probabilidades Implicadas — Individuo 0"))
cells.append(code(
    "beta_s2 = trace.posterior['beta'].values.reshape(-1, n_pred)\n"
    "cp_s    = trace.posterior['cutpoints'].values.reshape(-1, k_classes - 1)\n"
    "eta0    = np.dot(beta_s2, X_mat[0])\n"
    "pk0     = expit(cp_s[:, 0] - eta0)\n"
    "pk1     = expit(cp_s[:, 1] - eta0)\n"
    "probs   = np.array([pk0, pk1 - pk0, 1 - pk1])\n"
    "labels_cat = ['Last-Minute', 'In-Between', 'Planner']\n\n"
    "fig, ax = plt.subplots(figsize=(15, 6))\n"
    "for i in range(3):\n"
    "    ax.hist(probs[i], label=f'{labels_cat[i]} (mean={probs[i].mean():.2f})',\n"
    "            ec='white', bins=50, alpha=0.55)\n"
    "ax.set_xlabel('Probabilidad')\n"
    "ax.set_ylabel('Frecuencia')\n"
    "ax.set_title('Distribución Posterior de P(Y=k | X₀)', fontsize=16)\n"
    "ax.legend(fontsize=11)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

cells.append(md("### 2.7 Espacio Latente"))
cells.append(code(
    "beta_m  = trace.posterior['beta'].mean(dim=('chain','draw')).values\n"
    "theta_m = trace.posterior['cutpoints'].mean(dim=('chain','draw')).values\n"
    "eta_obs = X_mat @ beta_m\n"
    "eta_g   = np.linspace(eta_obs.min()-2, eta_obs.max()+2, 300)\n\n"
    "fig, ax = plt.subplots(figsize=(13, 6))\n"
    "ax.plot(eta_g, expit(theta_m[0]-eta_g), lw=2.5, color='royalblue',\n"
    "        label=f'P(Y<=0) | theta_1={theta_m[0]:.2f}')\n"
    "ax.plot(eta_g, expit(theta_m[1]-eta_g), lw=2.5, color='darkorange',\n"
    "        label=f'P(Y<=1) | theta_2={theta_m[1]:.2f}')\n"
    "ax.axvline(theta_m[0], color='royalblue', ls='--', alpha=0.5)\n"
    "ax.axvline(theta_m[1], color='darkorange', ls='--', alpha=0.5)\n"
    "for i, (cat, col) in enumerate(zip(labels_cat, ['#1f77b4','#ff7f0e','#2ca02c'])):\n"
    "    idx = (y_ord == i)\n"
    "    ax.scatter(eta_obs[idx], np.full(idx.sum(), -0.03-i*0.02),\n"
    "               alpha=0.4, s=12, color=col, label=f'Obs: {cat}')\n"
    "ax.set_xlabel('Puntuacion Latente (eta = X*beta)', fontsize=12)\n"
    "ax.set_ylabel('Probabilidad Acumulada', fontsize=12)\n"
    "ax.set_title('Modelo Logistico Ordinal', fontsize=15)\n"
    "ax.legend(bbox_to_anchor=(1.05, 1), fontsize=9)\n"
    "ax.set_ylim(-0.12, 1.05)\n"
    "ax.grid(alpha=0.3)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

# ── Conclusión ────────────────────────────────────────────────────────────────
cells.append(md(
    "---\n"
    "## Discusión Integrada\n\n"
    "**Parte I:** La solución NIG confirma $\\beta_{\\text{treat}} \\approx -1253$ "
    "(CrI 95%: [−2357, −159]). UBER Pool redujo el pago al conductor a corto plazo. "
    "Sin embargo, `total_matches_thousands` tiene un efecto masivamente positivo: "
    "la rentabilidad depende de la **densidad de emparejamientos**.\n\n"
    "**Parte II:** Los **Planners** (compradores anticipados) tienen mayor edad y gasto en concesiones. "
    "Su decisión >14 días antes permite planificación logística agregada.\n\n"
    "**Recomendación:** Una alianza Movistar Arena–Uber ofreciendo *Uber Pool Programado* a perfiles "
    "Planner resuelve simultáneamente la baja densidad (Parte I) y agrega valor al comprador premium (Parte II)."
))

# ── Escribir notebook ─────────────────────────────────────────────────────────
nb = nbformat.v4.new_notebook()
nb.cells = cells
nbformat.validate(nb)  # Falla explícitamente si hay errores de formato
nbformat.write(nb, path)
print(f"OK — Notebook escrito en: {path}")
print(f"Total celdas: {len(cells)}")
