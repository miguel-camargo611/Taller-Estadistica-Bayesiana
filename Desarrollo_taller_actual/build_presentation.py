import json
import base64
from io import BytesIO

def get_image_base64(nb, cell_id, img_index=0):
    for cell in nb['cells']:
        if cell.get('id') == cell_id:
            imgs = [out['data']['image/png'] for out in cell.get('outputs', []) if 'data' in out and 'image/png' in out.get('data', {})]
            if len(imgs) > img_index:
                return imgs[img_index]
    return ""

with open('solucion_taller.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

import os

img_uber_resid   = get_image_base64(nb, '5f181143', 0)
img_forest_beta  = get_image_base64(nb, '23a6d370', 0)
img_trace = [get_image_base64(nb, 'f16d741b', i) for i in range(7)]
img_ordinal_prob = get_image_base64(nb, 'd31efefc', 0)

uber_crops = []
for i in range(4):
    with open(f'imagenes/uber_post_{i}.png', 'rb') as imgf:
        uber_crops.append(base64.b64encode(imgf.read()).decode('utf-8'))

eda_crops = []
eda_files = [
    'eda_box_Age.png', 
    'eda_box_Num_Tickets_Purchased.png', 
    'eda_box_Ticket_Price.png', 
    'eda_box_Concession_Purchases.png',
    'eda_bar_Fan_Mailing_List.png', 
    'eda_bar_Seat_Location.png'
]
for f in eda_files:
    try:
        with open(f'imagenes/{f}', 'rb') as imgf:
            eda_crops.append(base64.b64encode(imgf.read()).decode('utf-8'))
    except:
        eda_crops.append("")

html = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Regresión Bayesiana — UBER Pool & Movistar Arena</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@400;600;700;800&display=swap" rel="stylesheet">
<script>
MathJax = {
  tex: { inlineMath: [['\\(','\\)'], ['$','$']], displayMath: [['\\[','\\]'], ['$$','$$']] },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre'] }
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:         #080d17;
  --surface:    rgba(255,255,255,0.04);
  --surface-hi: rgba(255,255,255,0.08);
  --border:     rgba(255,255,255,0.10);
  --accent:     #6c8eff;
  --gold:       #f5c842;
  --red:        #ff5f5f;
  --green:      #4ddfb0;
  --text-1:     #eef0f8;
  --text-2:     #9aa3bf;
  --text-3:     #6370a0;
  --r:          12px;
  --r-sm:       6px;
}

html, body { height: 100%; overflow: hidden; }

body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text-1);
  line-height: 1.65;
}

#show {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}

.slide {
  height: 100vh;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 30px 60px;
  position: relative;
  overflow: hidden;
}

.slide::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse 80% 60% at 50% -20%, rgba(108,142,255,0.12) 0%, transparent 70%);
  pointer-events: none;
}

h1, h2, h3, h4 { font-family: 'Sora', sans-serif; line-height: 1.2; }

.slide-tag {
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 14px;
}

.slide-title {
  font-size: 2.3rem;
  font-weight: 800;
  color: var(--text-1);
  text-align: center;
  margin-bottom: 24px;
}

.slide-title span.gold { color: var(--gold); }
.slide-title span.accent { color: var(--accent); }

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--r);
  padding: 22px 26px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.card-accent { border-left: 3px solid var(--accent); }
.card-gold { border-left: 3px solid var(--gold); }
.card-red { border-left: 3px solid var(--red); }
.card-green { border-left: 3px solid var(--green); }

.content {
  width: 100%;
  max-width: 1120px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  z-index: 1;
}

.row { display: flex; gap: 16px; align-items: flex-start; justify-content: center; }
.col { flex: 1; }

.math-block {
  background: rgba(108,142,255,0.07);
  border: 1px solid rgba(108,142,255,0.2);
  border-radius: var(--r-sm);
  padding: 10px 16px;
  text-align: center;
  font-size: 0.95rem;
  overflow-x: auto;
  color: var(--text-1);
}

table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
thead tr { background: rgba(108,142,255,0.15); }
th {
  padding: 8px 14px; text-align: left; font-family: 'Sora', sans-serif;
  font-weight: 600; font-size: 0.78rem; letter-spacing: 0.06em;
  text-transform: uppercase; color: var(--accent); border-bottom: 1px solid var(--border);
}
td { padding: 7px 14px; border-bottom: 1px solid var(--border); color: var(--text-2); }
td.hl { color: var(--red); font-weight: 600; }
td.pos { color: var(--green); font-weight: 600; }
tbody tr:hover td { background: var(--surface-hi); }

.img-wrap { width: 100%; text-align: center; }
.img-wrap img { max-width: 100%; max-height: 48vh; border-radius: var(--r-sm); object-fit: contain; }
.img-wrap.bg img { max-height: 65vh; }
.img-wrap.giant img { max-height: 70vh; }
.img-wrap.tall img { max-height: 52vh; }
.img-wrap.short img { max-height: 32vh; }

.img-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
.img-grid-3 img { width: 100%; border-radius: var(--r-sm); max-height: 48vh; object-fit: contain; }

.carousel-wrap { position: relative; width: 100%; }
.carousel {
  display: flex; overflow-x: auto; scroll-snap-type: x mandatory;
  scroll-behavior: smooth; gap: 0; border-radius: var(--r-sm);
}
.carousel::-webkit-scrollbar { height: 4px; }
.carousel::-webkit-scrollbar-track { background: var(--surface); }
.carousel::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 2px; }
.carousel-slide {
  flex: 0 0 100%; scroll-snap-align: center; display: flex;
  flex-direction: column; align-items: center; justify-content: center; padding: 10px;
}
.carousel-slide img { max-height: 60vh; max-width: 100%; border-radius: var(--r-sm); object-fit: contain; }
.carousel-label {
  font-size: 0.75rem; color: var(--text-3); margin-top: 6px;
  font-family: 'Sora', sans-serif; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase;
}
.carousel-nav { display: flex; justify-content: center; gap: 8px; margin-top: 12px; }
.carousel-dot {
  width: 8px; height: 8px; border-radius: 50%; background: var(--border);
  border: none; cursor: pointer; transition: background 0.2s;
}
.carousel-dot.active { background: var(--accent); }

.badge {
  display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px;
  border-radius: 99px; font-size: 0.75rem; font-weight: 600; font-family: 'Sora', sans-serif;
}
.badge-blue { background: rgba(108,142,255,0.15); color: var(--accent); }
.badge-gold { background: rgba(245,200,66,0.15); color: var(--gold); }

.list { list-style: none; display: flex; flex-direction: column; gap: 7px; }
.list li { display: flex; align-items: flex-start; gap: 10px; font-size: 0.95rem; color: var(--text-2); }
.list li::before { content: '▸'; color: var(--accent); flex-shrink: 0; margin-top: 1px; }

#nav {
  position: fixed; right: 18px; top: 50%; transform: translateY(-50%);
  display: flex; flex-direction: column; gap: 7px; z-index: 200;
}
.nav-dot {
  width: 7px; height: 7px; border-radius: 50%; background: var(--text-3);
  cursor: pointer; border: none; transition: all 0.25s;
}
.nav-dot:hover { background: var(--text-2); transform: scale(1.3); }
.nav-dot.on { background: var(--gold); transform: scale(1.4); }

.pg { position: absolute; bottom: 20px; right: 32px; font-size: 0.75rem; color: var(--text-3); font-family: 'Sora', sans-serif; }

#s1 { background: linear-gradient(135deg, #060c1b 0%, #0d1b40 60%, #07101f 100%); }
#s1::before { background: radial-gradient(ellipse 100% 80% at 50% 0%, rgba(108,142,255,0.22) 0%, transparent 65%); }
.cover-logo {
  width: 52px; height: 52px; border-radius: 14px;
  background: linear-gradient(135deg, var(--accent), #a78bfa);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.6rem; margin: 0 auto 28px; box-shadow: 0 0 40px rgba(108,142,255,0.4);
}
.cover-title { font-family: 'Sora', sans-serif; font-size: 3rem; font-weight: 800; text-align: center; line-height: 1.15; color: var(--text-1); }
.cover-title span { color: var(--gold); }
.cover-sub { text-align: center; color: var(--text-2); font-size: 1.1rem; margin-top: 14px; }
.cover-authors { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 32px; }
.author-chip { background: var(--surface); border: 1px solid var(--border); border-radius: 99px; padding: 6px 16px; font-size: 0.85rem; color: var(--text-2); }

.part-banner {
  background: linear-gradient(90deg, rgba(108,142,255,0.12), transparent);
  border-left: 3px solid var(--accent); border-radius: 0 var(--r-sm) var(--r-sm) 0;
  padding: 10px 20px; font-family: 'Sora', sans-serif; font-size: 0.85rem;
  font-weight: 600; color: var(--accent); letter-spacing: 0.06em; text-transform: uppercase;
}

.fade-in { opacity: 0; transform: translateY(18px); transition: opacity 0.65s ease, transform 0.65s ease; }
.slide.visible .fade-in { opacity: 1; transform: none; }
.fade-in:nth-child(2) { transition-delay: 0.1s; }
.fade-in:nth-child(3) { transition-delay: 0.2s; }
.fade-in:nth-child(4) { transition-delay: 0.3s; }
.fade-in:nth-child(5) { transition-delay: 0.4s; }

.var-chips {
  display: flex; flex-wrap: wrap; justify-content:center; gap: 8px; margin-bottom: 2px;
}
.var-chip {
  background: rgba(108,142,255,0.1); border: 1px solid rgba(108,142,255,0.3);
  color: var(--text-1); padding: 4px 10px; border-radius: 6px; font-size: 0.82rem; font-family: monospace;
}
</style>
</head>
<body>

<div id="nav"></div>

<div id="show">

<!-- SLIDE 1 -->
<section class="slide" id="s1">
  <div class="cover-logo">🎯</div>
  <h1 class="cover-title fade-in">Taller Integrado de<br><span>Regresión Bayesiana</span></h1>
  <p class="cover-sub fade-in">UBER Pool &nbsp;·&nbsp; Movistar Arena &nbsp;·&nbsp; Estadística Bayesiana</p>
  <div class="cover-authors fade-in">
    <div class="author-chip">Miguel Camargo</div>
    <div class="author-chip">Nicolás Cardenas</div>
    <div class="author-chip">Camilo Hernandez</div>
  </div>
  <p class="fade-in" style="margin-top:20px; color:var(--text-3); font-size:0.82rem;">Universidad Externado de Colombia · 2026</p>
  <div class="pg">1 / 12</div>
</section>

<!-- SLIDE 2 -->
<section class="slide" id="s2">
  <div class="content">
    <p class="slide-tag fade-in">Motivación</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:16px;">El Hilo <span class="gold">Conductor</span></h2>
    <div class="row fade-in">
      <div class="col card card-accent">
        <div style="font-size:2rem;margin-bottom:10px;">🚗</div>
        <h3 style="font-size:1.1rem;margin-bottom:8px;color:var(--text-1);">UBER Pool</h3>
        <p style="font-size:0.9rem;color:var(--text-2);">Experimento de movilidad compartida. ¿Aumentaron las ganancias de los conductores?</p>
        <div style="margin-top:10px;"><span class="badge badge-blue">Regresión Lineal NIG</span></div>
      </div>
      <div style="display:flex;align-items:center;font-size:1.8rem;color:var(--text-3);padding:0 8px;">⤳</div>
      <div class="col card card-gold">
        <div style="font-size:2rem;margin-bottom:10px;">🎤</div>
        <h3 style="font-size:1.1rem;margin-bottom:8px;color:var(--text-1);">Movistar Arena</h3>
        <p style="font-size:0.9rem;color:var(--text-2);">¿Qué perfila a un comprador como <em>Planner</em>? Modelado ordinal de comportamiento.</p>
        <div style="margin-top:10px;"><span class="badge badge-gold">Logit Ordinal NUTS</span></div>
      </div>
    </div>
    <div class="card fade-in" style="text-align:center;padding:16px;">
      <p style="font-size:1.1rem;color:var(--text-1);">¿Cómo la <strong style="color:var(--accent)">Inferencia Bayesiana</strong> nos permite cuantificar la incertidumbre en decisiones de consumidores en entornos de alta presión?</p>
    </div>
  </div>
  <div class="pg">2 / 12</div>
</section>

<!-- SLIDE 3 -->
<section class="slide" id="s3">
  <div class="content">
    <div class="part-banner fade-in">Parte I — UBER Pool</div>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:16px;">Caso <span class="accent">UBER Pool</span> &amp; Setup Bayesiano</h2>
    <div class="row fade-in">
      <div class="col card card-accent">
        <h4 style="color:var(--text-1);margin-bottom:10px;font-size:0.9rem;">Estructura del Modelo</h4>
        <div class="math-block" style="margin:6px 0;">
          \[ \mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}, \quad \boldsymbol{\varepsilon} \sim \mathcal{N}(\mathbf{0}, \sigma^2\mathbf{I}) \]
        </div>
        <ul class="list" style="margin-top:10px;">
          <li><strong style="color:var(--text-1)">treat</strong> — Si el pasajero activó UBER Pool</li>
          <li><strong style="color:var(--text-1)">commute</strong> — Hora pico / alta congestión</li>
          <li><strong style="color:var(--text-1)">total_matches_thousands</strong> — Emparejamientos</li>
        </ul>
      </div>
      <div class="col card card-gold">
        <h4 style="color:var(--gold);margin-bottom:12px;font-size:0.85rem;letter-spacing:0.08em;text-transform:uppercase;">Priors (Difusos)</h4>
        <div class="math-block" style="margin-bottom:10px;">
          \[ \boldsymbol{\beta} \sim \mathcal{N}(\mathbf{0}, V_0), \quad \sigma^2 \sim \mathcal{IG}(a_0, b_0) \]
        </div>
        <p style="font-size:0.9rem;color:var(--text-2);margin-bottom:10px;">
          Asumimos pre-distribuciones con máxima incertidumbre inicial:
        </p>
        <table>
          <thead><tr><th>Parámetro</th><th>Distribución</th><th>Media</th><th>Varianza</th></tr></thead>
          <tbody>
            <tr><td>\(\boldsymbol{\beta}\)</td><td>Normal (\(\mathcal{N}\))</td><td>0</td><td>Alta (\(10^8\))</td></tr>
            <tr><td>\(\sigma^2\)</td><td>Inversa-Gamma</td><td>Nocalc</td><td>Amplia (~10,000)</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="pg">3 / 12</div>
</section>

<!-- SLIDE 4 -->
<section class="slide" id="s4">
  <div class="content">
    <p class="slide-tag fade-in">Parte I — Resultados</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:4px;">Distribuciones <span class="accent">Posteriores</span> — UBER Pool</h2>
    
    <div class="row fade-in" style="width:100%; align-items:center; justify-content:center;">
        
      <!-- Tabla aislada inmensa en el costado -->
      <div class="col card card-accent" style="flex:1.2; max-width: 520px;">
        <h4 style="color:var(--accent);margin-bottom:14px;font-size:0.95rem;text-transform:uppercase;">Tabla Analítica y Conclusión</h4>
        <table style="font-size: 0.92rem;">
          <thead><tr><th>Variable</th><th>Media Posterior</th><th>CrI 95% Inferior</th><th>CrI 95% Superior</th></tr></thead>
          <tbody>
            <tr><td style="padding:10px;">Intercept</td><td class="pos" style="padding:10px;">$16,874</td><td style="padding:10px;">$13,157</td><td style="padding:10px;">$20,591</td></tr>
            <tr style="background: rgba(255,95,95,0.06);"><td style="padding:10px; color:var(--text-1);"><strong>treat (\(\beta_1\))</strong></td><td class="hl" style="padding:10px; font-size:1.05rem;">-$1,253</td><td class="hl" style="padding:10px;">-$2,371</td><td class="hl" style="padding:10px;">-$135</td></tr>
            <tr><td style="padding:10px;">commute</td><td class="pos" style="padding:10px;">$5,455</td><td style="padding:10px;">$3,009</td><td style="padding:10px;">$7,900</td></tr>
            <tr><td style="padding:10px;">matches</td><td class="pos" style="padding:10px;">$4,387</td><td style="padding:10px;">$2,890</td><td style="padding:10px;">$5,883</td></tr>
          </tbody>
        </table>
        <p style="font-size:0.92rem;color:var(--text-2);margin-top:20px;line-height:1.6; text-align:center;">El 95% del Intervalo de Credibilidad para el tratamiento es estrictamente negativo. Su efecto no cruza el cero.<br><strong style="color:var(--red);">Conclusión:</strong> UBER Pool redujo las ganancias de sus conductores.</p>
      </div>
        
      <!-- TABS MÁGICOS DE VISUALIZACIÓN EN GRANDE -->
      <div class="carousel-wrap fade-in" style="flex:1.6;">
        <div class="carousel">
          <div class="carousel-slide">
            <div class="img-wrap giant">
              <img src="data:image/png;base64,__IMG_UBER_POST_0__" alt="Intercept" style="max-height: 48vh;">
            </div>
            <div class="carousel-label" style="margin-top:15px; font-size:1rem;">Intercepto</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant">
              <img src="data:image/png;base64,__IMG_UBER_POST_1__" alt="Treat" style="max-height: 48vh;">
            </div>
            <div class="carousel-label" style="margin-top:15px; font-size:1rem; color:var(--red)">Tratamiento (UBER Pool)</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant">
              <img src="data:image/png;base64,__IMG_UBER_POST_2__" alt="Commute" style="max-height: 48vh;">
            </div>
            <div class="carousel-label" style="margin-top:15px; font-size:1rem;">Commute (Alta congestión)</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant">
              <img src="data:image/png;base64,__IMG_UBER_POST_3__" alt="Matches" style="max-height: 48vh;">
            </div>
            <div class="carousel-label" style="margin-top:15px; font-size:1rem;">Total Emparejamientos</div>
          </div>
        </div>
        <div class="carousel-nav">
          <button class="carousel-dot active"></button>
          <button class="carousel-dot"></button>
          <button class="carousel-dot"></button>
          <button class="carousel-dot"></button>
        </div>
      </div>
      
    </div>
  </div>
  <div class="pg">4 / 12</div>
</section>

<!-- SLIDE 5 -->
<section class="slide" id="s5">
  <div class="content">
    <p class="slide-tag fade-in">Parte I — Diagnóstico</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:16px;">Diagnóstico <span class="accent">Residual</span></h2>
    <div class="row fade-in">
      <div style="flex:2;">
        <div class="img-wrap tall">
          <img src="data:image/png;base64,__IMG_UBER_RESID__" alt="Residuos UBER">
        </div>
      </div>
      <div class="col" style="display:flex;flex-direction:column;gap:12px;">
        <div class="card card-green">
          <h4 style="color:var(--green);margin-bottom:8px;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">Resultado</h4>
          <p style="color:var(--text-2);font-size:0.92rem;">Nube aleatoria sin patrones sistemáticos → <strong style="color:var(--text-1)">Homosedasticidad validada</strong>.</p>
        </div>
        <div class="card">
          <ul class="list">
            <li>Sin forma de embudo (varianza constante)</li>
            <li>Sin curvas no-lineales detectadas</li>
            <li>Estimadores Bayesianos consistentes</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <div class="pg">5 / 12</div>
</section>

<!-- SLIDE 6 -->
<section class="slide" id="s6">
  <div class="content">
    <div class="part-banner fade-in">Parte II — Movistar Arena</div>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:16px;">Caso <span class="gold">Movistar Arena</span> &amp; Setup Bayesiano</h2>
    <div class="row fade-in">
      <div class="col card card-gold">
        <h4 style="color:var(--gold);margin-bottom:10px;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">Priors (Difusos)</h4>
        <div class="math-block" style="margin-bottom:10px;">
          \[ \boldsymbol{\beta} \sim \mathcal{N}(0, 100) \quad |\quad \boldsymbol{\theta} \sim \mathcal{N_{ord}}(0,100) \]
        </div>
        <p style="font-size:0.92rem;color:var(--text-2);margin-bottom:10px;">
          Utilizamos priors probabilísticos altamente dispersos:
        </p>
        <table>
          <thead><tr><th>Parámetro</th><th>Distribución</th><th>Media / Varianza</th></tr></thead>
          <tbody>
            <tr><td>\(\boldsymbol{\beta}\) (Predictores)</td><td>Normal (\(\mathcal{N}\))</td><td>0 \(\,/\,\) 100</td></tr>
            <tr><td>\(\boldsymbol{\theta}\) (Cutpoints)</td><td>Normal Ordenada</td><td>Sin cruces</td></tr>
          </tbody>
        </table>
        <div style="margin-top:10px;">
          <p style="font-size:0.82rem;color:var(--text-3);">Muestreo numérico: MCMC NUTS (No-U-Turn Sampler)</p>
        </div>
      </div>
      <div class="col card card-accent">
        <h4 style="color:var(--accent);margin-bottom:10px;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">Logit Ordinal</h4>
        <div class="math-block" style="margin-bottom:10px;">
          \[ P(Y_i \leq k \mid \mathbf{x}_i) = \sigma\!\left(\theta_k - \mathbf{x}_i^\top\boldsymbol{\beta}\right) \]
        </div>
        <p style="font-size:0.85rem;color:var(--text-2);margin-bottom:5px;">Variable objetivo Ordinal:</p>
        <p style="font-size:0.9rem;font-weight:600;color:var(--text-1);text-align:center;padding:8px 0;">Last-Minute (0) <span style="color:var(--text-3)">&lt;</span> In-Between (1) <span style="color:var(--text-3)">&lt;</span> Planner (2)</p>
      </div>
    </div>
  </div>
  <div class="pg">6 / 12</div>
</section>

<!-- SLIDE 7 -->
<section class="slide" id="s7">
  <div class="content">
    <p class="slide-tag fade-in">Parte II — Variables y Test</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:4px;">Selección de Variables y <span class="gold">Análisis Bivariado</span></h2>
    
    <div class="row fade-in" style="width:100%; align-items:center; justify-content:center; margin-top:10px;">
        
      <!-- Tabla fija aislada -->
      <div class="col card card-gold" style="flex:1.2; max-width: 520px;">
        <h4 style="color:var(--gold);margin-bottom:14px;font-size:1.05rem;text-transform:uppercase;text-align:left;">Pruebas de Inclusión (P-Values)</h4>
        <table style="font-size: 0.95rem;">
          <thead><tr><th>Variable</th><th>Test Estadístico</th><th>P-Value</th></tr></thead>
          <tbody>
            <tr><td style="padding:10px;">Age</td><td style="padding:10px;">Kruskal</td><td class="hl" style="padding:10px;">1.6×10⁻¹²⁷</td></tr>
            <tr><td style="padding:10px;">Num_Tickets</td><td style="padding:10px;">Kruskal</td><td class="hl" style="padding:10px;">2.7×10⁻⁹⁷</td></tr>
            <tr><td style="padding:10px;">Ticket_Price</td><td style="padding:10px;">Kruskal</td><td class="hl" style="padding:10px;">3.2×10⁻⁷</td></tr>
            <tr><td style="padding:10px;">Concession</td><td style="padding:10px;">Kruskal</td><td class="hl" style="padding:10px;">5.2×10⁻⁵⁹</td></tr>
            <tr style="background: rgba(255,255,255,0.03);"><td style="padding:10px;">Fan_Mailing</td><td style="padding:10px;">Chi²</td><td class="hl" style="padding:10px;">2.3×10⁻³⁰</td></tr>
            <tr style="background: rgba(255,255,255,0.03);"><td style="padding:10px;">Seat_Location</td><td style="padding:10px;">Chi²</td><td class="hl" style="padding:10px;">2.8×10⁻⁴⁷</td></tr>
          </tbody>
        </table>
        <p style="font-size:0.9rem;color:var(--text-2);margin-top:18px;line-height:1.5;">Rechazo rotundo de hipótesis nula (\(p \approx 0\)) para todos los Features evaluados.</p>
      </div>

      <!-- TABS MÁGICOS PARA CADA BOXPLOT/BARCHART -->
      <div class="carousel-wrap fade-in" style="flex:1.6;">
        <div class="carousel">
          <div class="carousel-slide">
            <div class="img-wrap giant"><img src="data:image/png;base64,__IMG_EDA_TAG_0__" style="max-height: 50vh;"></div>
            <div class="carousel-label">Edad (Boxplot)</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant"><img src="data:image/png;base64,__IMG_EDA_TAG_1__" style="max-height: 50vh;"></div>
            <div class="carousel-label">Número Boletos (Boxplot)</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant"><img src="data:image/png;base64,__IMG_EDA_TAG_2__" style="max-height: 50vh;"></div>
            <div class="carousel-label">Precio Boleta (Boxplot)</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant"><img src="data:image/png;base64,__IMG_EDA_TAG_3__" style="max-height: 50vh;"></div>
            <div class="carousel-label">Concesiones (Boxplot)</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant"><img src="data:image/png;base64,__IMG_EDA_TAG_4__" style="max-height: 50vh;"></div>
            <div class="carousel-label">Mailing de Fan (Barras Stack)</div>
          </div>
          <div class="carousel-slide">
            <div class="img-wrap giant"><img src="data:image/png;base64,__IMG_EDA_TAG_5__" style="max-height: 50vh;"></div>
            <div class="carousel-label">Locación (Barras Stack)</div>
          </div>
        </div>
        <div class="carousel-nav">
          <button class="carousel-dot active"></button>
          <button class="carousel-dot"></button>
          <button class="carousel-dot"></button>
          <button class="carousel-dot"></button>
          <button class="carousel-dot"></button>
          <button class="carousel-dot"></button>
        </div>
      </div>
      
    </div>
  </div>
  <div class="pg">7 / 12</div>
</section>

<!-- SLIDE 8 -->
<section class="slide" id="s8">
  <div class="content">
    <p class="slide-tag fade-in">Parte II — Resultados MCMC</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:12px;">Resultados Posteriores — <span class="accent">94% HDI</span></h2>
    <div class="row fade-in" style="align-items:flex-start;">
      <div style="flex:2;">
        <div class="img-wrap tall">
          <img src="data:image/png;base64,__IMG_FOREST__" alt="Forest Plot Beta">
        </div>
      </div>
      <div class="col card card-accent">
        <h4 style="color:var(--accent);margin-bottom:10px;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.08em;">Leyenda de betas</h4>
        <table>
          <thead><tr><th>Beta</th><th>Variable</th><th>Efecto Crítico</th></tr></thead>
          <tbody>
            <tr><td>\(\beta_0\)</td><td>Age</td><td class="pos">↑ Positivo</td></tr>
            <tr><td>\(\beta_1\)</td><td>Num_Tickets</td><td class="pos">↑ Positivo</td></tr>
            <tr><td>\(\beta_2\)</td><td>Ticket_Price</td><td class="pos">↑ Positivo</td></tr>
            <tr><td>\(\beta_3\)</td><td>Concession</td><td class="pos">↑ Positivo</td></tr>
            <tr><td>\(\beta_4\)</td><td>Fan_Mailing</td><td class="pos">↑ Positivo</td></tr>
            <tr><td>\(\beta_5\)</td><td>Seat_Front</td><td style="color:var(--text-3);">Cero / Neutro</td></tr>
            <tr><td>\(\beta_6\)</td><td>Seat_Balcony</td><td style="color:var(--text-3);">Cero / Neutro</td></tr>
          </tbody>
        </table>
        <p style="font-size:0.8rem;color:var(--text-2);margin-top:12px;line-height:1.5;">* Los betas 5 y 6 cruzan el Cero (HDIs interceptan la barrera nula), por lo que NO tienen un efecto definitivo. El resto sí impulsa la clase.</p>
      </div>
    </div>
  </div>
  <div class="pg">8 / 12</div>
</section>

<!-- SLIDE 9 -->
<section class="slide" id="s9">
  <div class="content">
    <p class="slide-tag fade-in">Parte II — Diagnóstico</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:0px;">Diagnóstico Cadenas <span class="accent">MCMC</span></h2>
    <div class="fade-in card" style="padding: 10px; margin-bottom: 8px; margin-top:12px; background: rgba(0,0,0,0.2);">
      <p style="font-size:0.8rem;color:var(--text-2);text-align:center;font-family:monospace;">
        <span style="color:var(--gold);">[0]</span> Age &nbsp;|&nbsp; 
        <span style="color:var(--gold);">[1]</span> Num_Tickets &nbsp;|&nbsp; 
        <span style="color:var(--gold);">[2]</span> Ticket_Price &nbsp;|&nbsp; 
        <span style="color:var(--gold);">[3]</span> Concession &nbsp;|&nbsp; 
        <span style="color:var(--gold);">[4]</span> Fan_Mailing &nbsp;|&nbsp; 
        <span style="color:var(--gold);">[5]</span> Seat_Front &nbsp;|&nbsp; 
        <span style="color:var(--gold);">[6]</span> Seat_Balcony
      </p>
    </div>
    
    <div class="carousel-wrap card fade-in" style="padding:14px;">
      <div class="carousel" id="mcmc-carousel">
        <div class="carousel-slide"><img src="data:image/png;base64,__IMG_T0__" alt="beta[0]"><div class="carousel-label">β[0] — Age</div></div>
        <div class="carousel-slide"><img src="data:image/png;base64,__IMG_T1__" alt="beta[1]"><div class="carousel-label">β[1] — Num_Tickets</div></div>
        <div class="carousel-slide"><img src="data:image/png;base64,__IMG_T2__" alt="beta[2]"><div class="carousel-label">β[2] — Ticket_Price</div></div>
        <div class="carousel-slide"><img src="data:image/png;base64,__IMG_T3__" alt="beta[3]"><div class="carousel-label">β[3] — Concession</div></div>
        <div class="carousel-slide"><img src="data:image/png;base64,__IMG_T4__" alt="beta[4]"><div class="carousel-label">β[4] — Fan_Mailing</div></div>
        <div class="carousel-slide"><img src="data:image/png;base64,__IMG_T5__" alt="beta[5]"><div class="carousel-label">β[5] — Seat_Front</div></div>
        <div class="carousel-slide"><img src="data:image/png;base64,__IMG_T6__" alt="beta[6]"><div class="carousel-label">β[6] — Seat_Balcony</div></div>
      </div>
      <div class="carousel-nav" id="mcmc-dots">
        <button class="carousel-dot active"></button>
        <button class="carousel-dot"></button>
        <button class="carousel-dot"></button>
        <button class="carousel-dot"></button>
        <button class="carousel-dot"></button>
        <button class="carousel-dot"></button>
        <button class="carousel-dot"></button>
      </div>
    </div>
  </div>
  <div class="pg">9 / 12</div>
</section>

<!-- SLIDE 10 -->
<section class="slide" id="s10">
  <div class="content">
    <p class="slide-tag fade-in">Parte II — Interpretación</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:12px;">Curva Ordinal <span class="gold">Latente</span></h2>
    <div class="row fade-in" style="align-items:center;">
      <div style="flex:2.3;">
        <div class="img-wrap tall">
          <img src="data:image/png;base64,__IMG_PROB__" alt="Curva Logit Ordinal">
        </div>
      </div>
      <div class="col card card-gold">
        <h4 style="color:var(--gold);margin-bottom:12px;font-size:0.85rem;">Estructura del Modelo Ordinal</h4>
        <p style="font-size:0.88rem;color:var(--text-2);margin-bottom:14px;line-height:1.6;">La puntuación \(\eta\) (eje X) sitúa a cada usuario latiblemente. Los <strong>Cutpoints</strong> (líneas punteadas) dividen rígidamente esta escala, definiendo qué curva de probabilidad gobierna.</p>
        
        <table style="font-size: 0.85rem;">
          <thead><tr><th>Rango (\(\eta\))</th><th>Zona</th><th>Perfil Asignado</th></tr></thead>
          <tbody>
            <tr><td>A la izquierda de \(\theta_1\)</td><td style="color:var(--accent);">Azul Oscuro</td><td style="color:var(--text-1);"><strong>Last-Minute</strong></td></tr>
            <tr><td>Entre \(\theta_1\) y \(\theta_2\)</td><td style="color:var(--gold);">Transición</td><td style="color:var(--text-1);"><strong>In-Between</strong></td></tr>
            <tr><td>Derecha de \(\theta_2\)</td><td class="pos">Superior</td><td style="color:var(--text-1);"><strong>Planner</strong></td></tr>
          </tbody>
        </table>
        
        <p style="font-size:0.8rem;color:var(--text-3);margin-top:14px;">Usuarios con alta puntuación superan las barreras y se acomodan en el perfil <em>Planner</em>.</p>
      </div>
    </div>
  </div>
  <div class="pg">10 / 12</div>
</section>

<!-- SLIDE 11 -->
<section class="slide" id="s11">
  <div class="content">
    <p class="slide-tag fade-in">Propuesta Estratégica</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:16px;">Sinergia <span class="gold">Operativa</span></h2>
    <div class="row fade-in">
      <div class="col card card-red">
        <h4 style="color:var(--red);margin-bottom:10px;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">El Problema</h4>
        <p style="font-size:0.9rem;color:var(--text-2);">UBER Pool sufre de <strong style="color:var(--text-1)">demanda asincrónica masiva</strong>. Los perfiles <em>Last-Minute</em> generan peticiones repentinas que colapsan la plataforma y reducen ganancias.</p>
      </div>
      <div style="display:flex;align-items:center;font-size:1.8rem;color:var(--gold);padding:0 8px;">→</div>
      <div class="col card card-green">
        <h4 style="color:var(--green);margin-bottom:10px;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.08em;">La Solución</h4>
        <p style="font-size:0.9rem;color:var(--text-2);">El perfil <em>Planner</em> del Arena es <strong style="color:var(--text-1)">altamente receptivo</strong> a ofertas previas y gasta más en extras. Reservas anticipadas de UBER Pool hacen el puente.</p>
      </div>
    </div>
    <div class="card fade-in" style="text-align:center;border:1px solid var(--gold);background:rgba(245,200,66,0.05);padding:20px;margin-top:4px;">
      <h3 style="color:var(--gold);font-size:1.4rem;margin-bottom:10px;">💡 Combos Logísticos Anticipados</h3>
      <p style="color:var(--text-2);font-size:0.95rem;max-width:700px;margin:0 auto;">Movistar Arena integra <strong style="color:var(--text-1)">reservas de UBER Pool exclusivas</strong> en la preventa de zonas Planner. UBER obtiene densidad asegurada. El Arena elimina congestión post-concierto.</p>
    </div>
  </div>
  <div class="pg">11 / 12</div>
</section>

<!-- SLIDE 12 -->
<section class="slide" id="s12">
  <div class="content">
    <p class="slide-tag fade-in">Síntesis</p>
    <h2 class="slide-title fade-in" style="text-align:left;margin-bottom:16px;"><span class="gold">Conclusiones</span></h2>
    <div class="row fade-in">
      <div class="col card card-red">
        <h4 style="color:var(--red);margin-bottom:8px;font-size:0.82rem;text-transform:uppercase;">Hallazgo I — UBER Pool</h4>
        <p style="font-size:0.92rem;color:var(--text-2);">Con una certeza estricta del <strong style="color:var(--red);font-size:1.1rem;">98.7%</strong>, UBER Pool redujo las ganancias de los conductores a corto plazo en el experimento evaluado.</p>
      </div>
      <div class="col card card-green">
        <h4 style="color:var(--green);margin-bottom:8px;font-size:0.82rem;text-transform:uppercase;">Hallazgo II — Movistar Arena</h4>
        <p style="font-size:0.92rem;color:var(--text-2);">Atributos como la <strong style="color:var(--text-1)">Edad</strong> o <strong style="color:var(--text-1)">Consumo en Concesiones</strong> son propulsores infalibles y correlacionados hacia la actitud previsora de un <em>Planner</em>.</p>
      </div>
    </div>
    <div class="card fade-in" style="text-align:center;padding:20px;">
      <p style="font-size:1.05rem;color:var(--text-2);max-width:750px;margin:0 auto;line-height:1.7;">La <strong style="color:var(--accent)">Inferencia Bayesiana</strong> nos permitió cuantificar la incertidumbre con total precisión para conectar dos mercados aparentemente dispares, logrando formular una propuesta directiva de valor conjunta basada en estadística probabilística.</p>
    </div>
  </div>
  <div class="pg">12 / 12</div>
</section>

</div><!-- #show -->

<script>
const slides = [...document.querySelectorAll('.slide')];
const navEl  = document.getElementById('nav');
slides.forEach((_, i) => {
  const btn = document.createElement('button');
  btn.className = 'nav-dot' + (i===0?' on':'');
  btn.title = `Slide ${i+1}`;
  btn.onclick = () => slides[i].scrollIntoView({behavior:'smooth'});
  navEl.appendChild(btn);
});
const dots = [...navEl.querySelectorAll('.nav-dot')];

const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      const idx = slides.indexOf(e.target);
      dots.forEach((d,i) => d.classList.toggle('on', i===idx));
    }
  });
}, { root: document.getElementById('show'), threshold: 0.55 });
slides.forEach(s => io.observe(s));
setTimeout(()=>slides[0].classList.add('visible'), 80);

// Scripts dinámicos para TODOS los carruseles (UBER, EDA, MCMC)
document.querySelectorAll('.carousel-wrap').forEach(wrap => {
  const car  = wrap.querySelector('.carousel');
  const cdots = [...wrap.querySelectorAll('.carousel-dot')];
  
  if(cdots.length === 0) return;

  cdots.forEach((dot, i) => {
    dot.onclick = () => {
      car.scrollTo({ left: car.offsetWidth * i, behavior: 'smooth' });
      cdots.forEach(d => d.classList.remove('active'));
      dot.classList.add('active');
    };
  });
  
  car.addEventListener('scroll', () => {
    const n = Math.round(car.scrollLeft / car.offsetWidth);
    cdots.forEach((d, i) => d.classList.toggle('active', i === n));
  });
});
</script>
</body>
</html>
"""

html = html.replace('__IMG_UBER_POST_0__', uber_crops[0])
html = html.replace('__IMG_UBER_POST_1__', uber_crops[1])
html = html.replace('__IMG_UBER_POST_2__', uber_crops[2])
html = html.replace('__IMG_UBER_POST_3__', uber_crops[3])
html = html.replace('__IMG_UBER_RESID__', img_uber_resid)

for i in range(6):
    html = html.replace(f'__IMG_EDA_TAG_{i}__', eda_crops[i] if i < len(eda_crops) else "")

html = html.replace('__IMG_FOREST__', img_forest_beta)
for i, tr in enumerate(img_trace):
    html = html.replace(f'__IMG_T{i}__', tr)
html = html.replace('__IMG_PROB__', img_ordinal_prob)

with open('presentacion_taller.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("HTML Regenerado Mágico - Componentes Multi-Carrusel Habilitados")
