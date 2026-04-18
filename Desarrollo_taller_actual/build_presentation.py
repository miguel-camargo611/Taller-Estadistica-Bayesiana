# -*- coding: utf-8 -*-
import json

def get_image_base64(nb, cell_id, img_index=0):
    for cell in nb['cells']:
        if cell.get('id') == cell_id:
            imgs = [out['data']['image/png'] for out in cell.get('outputs', []) if 'data' in out and 'image/png' in out['data']]
            if len(imgs) > img_index:
                return imgs[img_index]
    return ""

# Usamos raw string (r"") para proteger los backslashes de LaTeX para MathJax.
html_template = r"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taller Integrado de Regresión Bayesiana</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Montserrat:wght@500;700;800&display=swap" rel="stylesheet">
    <!-- MathJax -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {
            --dark-blue: #1a2a4a;
            --gold: #d4a017;
            --light-bg: #f9fafc;
            --text-dark: #333;
            --text-light: #fff;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--light-bg);
            color: var(--text-dark);
            line-height: 1.6;
            overflow: hidden; /* Disabled main scroll to enforce snap */
        }

        h1, h2, h3, h4 {
            font-family: 'Montserrat', sans-serif;
        }

        .slideshow-container {
            width: 100%;
            height: 100vh;
            overflow-y: scroll;
            scroll-snap-type: y mandatory;
            scroll-behavior: smooth;
        }

        .slide {
            height: 100vh;
            width: 100%;
            scroll-snap-align: start;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 40px 80px;
            position: relative;
            background-color: var(--light-bg);
        }

        .slide:nth-child(even) {
            background-color: #fff;
        }

        .slide-title {
            color: var(--dark-blue);
            font-size: 2.2rem;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 700;
        }

        .slide-title::after {
            content: '';
            display: block;
            width: 80px;
            height: 4px;
            background-color: var(--gold);
            margin: 10px auto 0;
        }

        .content {
            max-width: 1100px;
            width: 100%;
            font-size: 1.1rem;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        /* Slide 1: Portada */
        #slide-1 {
            background-color: var(--dark-blue);
            color: var(--text-light);
            text-align: center;
        }
        #slide-1 .slide-title {
            color: var(--gold);
            font-size: 3.2rem;
        }
        #slide-1 .slide-title::after {
            display: none;
        }
        #slide-1 h3 {
            font-size: 1.5rem;
            font-weight: 400;
            margin-top: 10px;
            opacity: 0.9;
        }
        .authors {
            margin-top: 40px;
            font-size: 1.1rem;
            font-weight: 300;
            color: rgba(255,255,255,0.8);
        }

        /* Componentes Comunes */
        .highlight {
            color: #d84b2a;
            font-weight: 600;
        }

        .box {
            background-color: #fff;
            padding: 15px 25px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            border-left: 5px solid var(--dark-blue);
        }

        .flex-row {
            display: flex;
            justify-content: center;
            gap: 20px;
            align-items: flex-start;
            width: 100%;
        }

        .flex-col {
            flex: 1;
        }

        ul {
            padding-left: 20px;
            list-style-type: none;
        }

        ul li {
            position: relative;
            margin-bottom: 8px;
        }

        ul li::before {
            content: "•";
            color: var(--gold);
            font-weight: bold;
            display: inline-block;
            width: 1em;
            margin-left: -1em;
        }

        .math-box {
            background-color: #f1f3f8;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size: 1rem;
            overflow-x: auto;
        }

        .img-container {
            text-align: center;
            margin-top: 10px;
        }

        .img-container img {
            max-width: 100%;
            max-height: 48vh;
            border-radius: 5px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .img-large img {
            max-height: 62vh;
        }

        .img-medium img {
            max-height: 50vh;
            height: auto;
            width: auto;
        }

        .grid-3 {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 10px;
            max-height: 40vh;
        }
        
        .grid-3 img {
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .carousel-container {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            gap: 20px;
            padding: 15px 0;
            width: 100%;
            max-height: 60vh;
        }
        
        .carousel-item {
            flex: 0 0 100%;
            scroll-snap-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .carousel-item img {
            max-height: 50vh;
            max-width: 80vw;
            border-radius: 5px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .data-dict table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
            background-color: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .data-dict th, .data-dict td {
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
        }
        
        .data-dict th {
            background-color: var(--dark-blue);
            color: white;
            font-family: 'Montserrat', sans-serif;
            font-weight: 500;
        }

        /* Nav Helper */
        .progress-indicator {
            position: fixed;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 8px;
            z-index: 100;
        }

        .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: rgba(26, 42, 74, 0.3);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .dot.active {
            background-color: var(--gold);
            transform: scale(1.3);
        }

        /* Animaciones on scroll */
        .anim-fade {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }

        .slide.is-visible .anim-fade {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Footer pagenum */
        .page-num {
            position: absolute;
            bottom: 20px;
            right: 30px;
            font-size: 0.9rem;
            color: #888;
        }

        .scroll-hint {
            text-align: center;
            font-size: 0.8rem;
            color: #888;
            margin-top: -10px;
        }
    </style>
</head>
<body>

    <div class="progress-indicator" id="dots"></div>

    <div class="slideshow-container" id="slideshow">

        <!-- SLIDE 1 -->
        <section class="slide" id="slide-1">
            <h1 class="slide-title anim-fade">Taller Integrado de Regresión Bayesiana</h1>
            <h3 class="anim-fade">Casos: UBER Pool y Movistar Arena</h3>
            <div class="authors anim-fade">
                <p>Estudiantes: Miguel Camargo, Nicolas Cardenas y Camilo Hernandez</p>
                <p>Estadística Bayesiana — Universidad Externado de Colombia</p>
                <p>2026</p>
            </div>
            <div class="page-num" style="color:rgba(255,255,255,0.5)">1</div>
        </section>

        <!-- SLIDE 2 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Introducción: El Hilo Conductor</h2>
            <div class="content anim-fade flex-row">
                <div class="flex-col box" style="text-align:center;">
                    <h3 style="color:var(--dark-blue);">🚗 Movilidad Compartida</h3>
                    <p style="margin-top:10px;">Experimento UBER Pool</p>
                </div>
                <div style="font-size:2rem; color:var(--gold);">⟷</div>
                <div class="flex-col box" style="text-align:center;">
                    <h3 style="color:var(--dark-blue);">🎤 Entretenimiento</h3>
                    <p style="margin-top:10px;">Eventos en Movistar Arena</p>
                </div>
            </div>
            <div class="content anim-fade" style="margin-top:30px; text-align:center;">
                <p style="font-size:1.4rem;"><strong>Preguntas centrales:</strong></p>
                <p>¿Cómo predecir y entender las decisiones logísticas y personales basándose en cuantificación de incertidumbre?</p>
            </div>
            <div class="page-num">2</div>
        </section>

        <!-- SLIDE 3 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Parte I: Caso UBER Pool & Setup Bayesiano</h2>
            <div class="content anim-fade">
                <p><strong>Objetivo:</strong> Evaluar si la introducción de UBER Pool logró aumentar la remuneración de los conductores.</p>
                <div class="flex-row">
                    <div class="flex-col box">
                        <p>Variable Y: <code style="color:var(--dark-blue)">total_driver_payout</code></p>
                        <p style="margin-top:5px;"><strong>Variables de control \(\mathbf{X}\):</strong></p>
                        <ul>
                            <li><code class="highlight">treat</code>: Tratamiento (Activar Pool)</li>
                            <li><code style="color:var(--dark-blue)">commute</code>: Alta congestión</li>
                            <li><code style="color:var(--dark-blue)">total_matches_thousands</code>: Emparejamientos netos</li>
                        </ul>
                    </div>
                    <div class="flex-col box" style="background-color:#fef8e7; border-left-color:var(--gold);">
                        <h4 style="color:#b8860b;">Priors Asignados (Informativos/Difusos)</h4>
                        <div style="font-size:0.95rem; margin-top:10px;">
                            <p>Familia <strong style="color:#d84b2a">Normal-Inversa-Gamma</strong> analítica:</p>
                            <p>$$ \boldsymbol{\beta}_0 = \mathbf{0}, \quad \kappa_0 = 10^{-8} $$</p>
                            <p>$$ \sigma^2 \sim \mathcal{IG}(a_0=2, b_0) $$</p>
                            <p style="font-size:0.85rem; color:#555;">(Altísima incertidumbre a priori, \(\sigma=10000\))</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="page-num">3</div>
        </section>

        <!-- SLIDE 4 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Resultados Posteriores: Efecto UBER Pool</h2>
            <div class="content anim-fade">
                <div class="math-box" style="font-size:0.9rem; padding:8px;">
                    Las fórmulas cerradas \(\mathbf{V}_n = (\mathbf{V}_0^{-1} + \mathbf{X}^\top \mathbf{X})^{-1}; \; \boldsymbol{\beta}_n = \mathbf{V}_n (\mathbf{V}_0^{-1}\boldsymbol{\beta}_0 + \mathbf{X}^\top \mathbf{y})\) arrojaron:
                </div>
                <div class="img-container img-medium" style="margin-top:0;">
                    <img src="data:image/png;base64,{IMG_UBER_POST}" alt="Distribuciones Posteriores UBER">
                </div>
                <div class="box flex-row" style="text-align:center; padding: 15px;">
                    <div class="flex-col">
                        <p style="font-size:1.2rem; margin-bottom:5px;">El Parámetro <span class="highlight">treat (\(\beta_1\))</span> es netamente inferior a cero</p>
                    </div>
                    <div class="flex-col">
                        <p style="font-size:1.4rem; margin-bottom:5px;">\( P(\beta_1 < 0) = \) <strong style="color:#d84b2a; font-size:1.6rem;">98.7%</strong></p>
                    </div>
                </div>
            </div>
            <div class="page-num">4</div>
        </section>

        <!-- SLIDE 5 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Diagnóstico Residual del Modelo (UBER)</h2>
            <div class="content anim-fade">
                <p>Verificamos que el modelo esté correctamente especificado evaluando la dispersión de los residuos a posteriori.</p>
                <div class="img-container img-large">
                    <img src="data:image/png;base64,{IMG_UBER_RESID}" alt="Residuos vs Valores Ajustados">
                </div>
                <p style="text-align:center; font-size:1rem; color:#666;">La ausencia de patrones sistemáticos (forma de embudo, o curvas no-lineales) confirma la validez homosedástica de la regresión.</p>
            </div>
            <div class="page-num">5</div>
        </section>

        <!-- SLIDE 6 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Parte II: Movistar Arena & Setup Bayesiano</h2>
            <div class="content anim-fade">
                <p><strong>Meta:</strong> Modelar la propensión ordinal de los usuarios a comprar entradas con anticipación.</p>
                <div class="flex-row">
                    <div class="flex-col box" style="max-height: 400px; overflow-y: auto;">
                        <h4>Diccionario de Features (\(N=1000\)):</h4>
                        <ul style="font-size:0.9rem; margin-top:5px;">
                            <li><strong>\( Y \) (Target Ordinal):</strong> Last-Minute (0) < In-Between (1) < Planner (2)</li>
                            <li><strong>Age (\(\beta_0\)):</strong> Edad del comprador (norm.)</li>
                            <li><strong>Num_Tickets (\(\beta_1\)):</strong> Cantidad de boletos (norm.)</li>
                            <li><strong>Ticket_Price (\(\beta_2\)):</strong> Precio del boleto (norm.)</li>
                            <li><strong>Concession (\(\beta_3\)):</strong> Compras adicionales (norm.)</li>
                            <li><strong>Fan_Mailing (\(\beta_4\)):</strong> Suscrito a correos (1=Sí)</li>
                            <li><strong>Seat_Front (\(\beta_5\)):</strong> Asiento Frontal (1=Sí)</li>
                            <li><strong>Seat_Balcony (\(\beta_6\)):</strong> Asiento Balcón (1=Sí)</li>
                        </ul>
                    </div>
                    <div class="flex-col box" style="background-color:#fef8e7; border-left-color:var(--gold);">
                        <h4 style="color:#b8860b;">MCMC y Priors Asignados</h4>
                        <div style="font-size:0.95rem; margin-top:10px;">
                            <p><strong>Regresión Logística Ordinal</strong> estimada con factor NUTS (PyMC).</p>
                            <p style="margin-top:10px;">Priors débiles sobre los coeficientes y las brechas (puntos de corte ordenados):</p>
                            <p>$$ \boldsymbol{\beta} \sim \mathcal{N}(0, 100) $$</p>
                            <p>$$ \boldsymbol{\theta_{k}} \sim \text{NormalOrdenada}(0, 100) $$</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="page-num">6</div>
        </section>

        <!-- SLIDE 7 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">EDA y Pruebas de Asociación (Kruskal-Wallis)</h2>
            <div class="content anim-fade">
                <p>Verificamos estadísticamente si los Target Groups difieren antes de entrenar el modelo. </p>
                <div class="box" style="padding:10px;">
                    <p style="font-size:0.95rem;"><strong>Resultados Numéricos (p<0.05):</strong> Age (\(1.6e^{-127}\)), Num_Tickets (\(2.6e^{-97}\)), Price (\(3.1e^{-7}\)), Concession (\(5.2e^{-59}\)), Mailing (\(2.2e^{-30}\))</p>
                </div>
                <div class="grid-3">
                    <img src="data:image/png;base64,{IMG_EDA_1}" alt="Boxplot Edad">
                    <img src="data:image/png;base64,{IMG_EDA_2}" alt="Boxplot Tickets">
                    <img src="data:image/png;base64,{IMG_EDA_3}" alt="Boxplot Price">
                </div>
                <p style="text-align:center; font-size:1.1rem;"><span class="highlight">A mayor planeación, mayor consumo, edad y boletos comprados.</span></p>
            </div>
            <div class="page-num">7</div>
        </section>

        <!-- SLIDE 8 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Resultados Posteriores: Ordinal Beta</h2>
            <div class="content anim-fade">
                <div class="img-container img-medium" style="margin-top:0;">
                    <img src="data:image/png;base64,{IMG_ORDINAL_BETA}" alt="Forest Plot HDI Beta">
                </div>
                <div class="data-dict" style="margin:5px 0;">
                    <table>
                        <tr>
                            <td class="highlight">beta[0]:</td><td>Age</td>
                            <td class="highlight">beta[1]:</td><td>Num_Tickets</td>
                            <td class="highlight">beta[2]:</td><td>Ticket_Price</td>
                            <td class="highlight">beta[3]:</td><td>Concession_Purch.</td>
                        </tr>
                        <tr>
                            <td class="highlight">beta[4]:</td><td>Fan_Mailing</td>
                            <td class="highlight">beta[5]:</td><td>Seat_Front</td>
                            <td class="highlight">beta[6]:</td><td>Seat_Balcony</td>
                            <td></td><td></td>
                        </tr>
                    </table>
                </div>
                <div class="box" style="padding:10px 20px; font-size:1rem;">
                    Ser <strong style="color:var(--dark-blue)">Mayor de edad</strong>, tener <strong style="color:var(--dark-blue)">Altos gastos de comida/mercancía</strong>, y comprar múltiples boletas, marcan el claro perfil <em>Planner</em>. Si esas métricas decaen fuertemente, nos adentramos al espectro del <em>Last-Minute</em>.
                </div>
            </div>
            <div class="page-num">8</div>
        </section>

        <!-- SLIDE 9 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Diagnóstico Cadenas MCMC: Trazas Individuales (Betas)</h2>
            <p class="scroll-hint anim-fade">(Desliza la barra horizontal para observar la convergencia de las 7 características)</p>
            <div class="content anim-fade">
                <div class="carousel-container box">
                    <div class="carousel-item"><img src="data:image/png;base64,{IMG_TRACE_0}" alt="Traza Beta 0"></div>
                    <div class="carousel-item"><img src="data:image/png;base64,{IMG_TRACE_1}" alt="Traza Beta 1"></div>
                    <div class="carousel-item"><img src="data:image/png;base64,{IMG_TRACE_2}" alt="Traza Beta 2"></div>
                    <div class="carousel-item"><img src="data:image/png;base64,{IMG_TRACE_3}" alt="Traza Beta 3"></div>
                    <div class="carousel-item"><img src="data:image/png;base64,{IMG_TRACE_4}" alt="Traza Beta 4"></div>
                    <div class="carousel-item"><img src="data:image/png;base64,{IMG_TRACE_5}" alt="Traza Beta 5"></div>
                    <div class="carousel-item"><img src="data:image/png;base64,{IMG_TRACE_6}" alt="Traza Beta 6"></div>
                </div>
                <p style="text-align:center; font-size:1rem; margin-top:5px;">El muestreo de NUTS y los Cutpoints ostentan un \(\hat{R} \approx 1\). Las cadenas son compactas, sin sesgos a largo plazo.</p>
            </div>
            <div class="page-num">9</div>
        </section>
        
        <!-- SLIDE 10 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Curva Ordinal Latente (Probabilidades)</h2>
            <div class="content anim-fade">
                <p>Las funciones de paso estocástico (Cutpoints \(\boldsymbol{\theta}\)) delimitan la clasificación predictiva de los clientes en función del log-odds.</p>
                <div class="img-container img-large" style="margin-top:0;">
                    <img src="data:image/png;base64,{IMG_ORDINAL_PROB}" alt="Curva de Probabilidad Logit Ordinal">
                </div>
            </div>
            <div class="page-num">10</div>
        </section>

        <!-- SLIDE 11 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Sinergia Operativa: Propuesta Estratégica</h2>
            <div class="content anim-fade">
                <div class="flex-row">
                    <div class="flex-col box" style="background-color: var(--dark-blue); color:white; border:none; padding:25px;">
                        <h3>El Cuello de Botella</h3>
                        <p style="opacity:0.9; margin-top:10px;">La Plataforma pierde ingresos por la abrupta asincronía asimétrica y demanda repentina inmanejable de pasajeros <em>Last-Minute</em> que salen del concierto intentando activar Pool.</p>
                    </div>
                    <div class="flex-col box" style="border-left: 5px solid #d84b2a; padding:25px;">
                        <h3>El Puente de Solución</h3>
                        <p style="margin-top:10px;">Encontramos un grupo hiper-receptivo a ofertas (<em>Planners</em>), y muy estructurado. Si emparejamos este perfil del Arena, UBER consolida su densidad operacional.</p>
                    </div>
                </div>
                <div style="text-align:center; margin-top:20px;">
                    <h3 style="font-size:1.8rem; color:var(--gold);">Combos Logísticos Anticipados</h3>
                    <p style="font-size:1.15rem; margin-top:10px; width:90%; margin:10px auto 0;">Integrar la Reserva Oficial de <em>Uber Pool Exclusivo</em> en las entradas más caras dirigidas a Planners durante la fase de inicio de venta para garantizar despachos coordinados automáticos post-concierto.</p>
                </div>
            </div>
            <div class="page-num">11</div>
        </section>

        <!-- SLIDE 12 -->
        <section class="slide">
            <h2 class="slide-title anim-fade">Conclusión</h2>
            <div class="content anim-fade">
                <div class="box">
                    <h3 style="color:var(--dark-blue); margin-bottom:15px;">Modelar para mitigar la Incertidumbre</h3>
                    <p>La regresión bayesiana nos posibilitó:</p>
                    <ul style="margin-top:10px; margin-bottom:20px; font-size:1.1rem; gap:10px; display:flex; flex-direction:column;">
                        <li>Certificar de manera categórica el revés financiero del experimento de movilidad UBER con una cota rigurosa mayor al <strong>98.7%</strong>.</li>
                        <li>Delimitar el perfil granular de un consumidor de eventos midiendo el impacto probabilístico directo de su anticipación y poder adquisitivo individual.</li>
                    </ul>
                    <p style="font-size:1.1rem; border-top: 1px solid #eee; padding-top: 15px;"><strong>Lección Final:</strong> Las métricas exactas basadas en riesgo y probabilidad impulsan a negocios aparentemente dispares a cooperar asertivamente para subsanar sus colapsos logísticos operativos de forma recíproca.</p>
                </div>
            </div>
            <div class="page-num">12</div>
        </section>

    </div>

    <script>
        const slides = document.querySelectorAll('.slide');
        const dotsContainer = document.getElementById('dots');

        // Generar dots
        slides.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => {
                slides[i].scrollIntoView({ behavior: 'smooth' });
            });
            dotsContainer.appendChild(dot);
        });

        const dots = document.querySelectorAll('.dot');
        const observerOptions = {
            root: document.getElementById('slideshow'),
            threshold: 0.5
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    const index = Array.from(slides).indexOf(entry.target);
                    dots.forEach(d => d.classList.remove('active'));
                    if (dots[index]) dots[index].classList.add('active');
                }
            });
        }, observerOptions);

        slides.forEach(slide => observer.observe(slide));
        setTimeout(() => { slides[0].classList.add('is-visible'); }, 100);
    </script>
</body>
</html>
"""

# Reemplazamos los identificadores extraídos
with open('solucion_taller.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

final_html = html_template.replace('{IMG_UBER_POST}', get_image_base64(nb, 'eecc1444', 0))
final_html = final_html.replace('{IMG_UBER_RESID}', get_image_base64(nb, '5f181143', 0))

# EDA Kruskal (3 image boxplots)
final_html = final_html.replace('{IMG_EDA_1}', get_image_base64(nb, 'c40d571d', 0))
final_html = final_html.replace('{IMG_EDA_2}', get_image_base64(nb, 'c40d571d', 1))
final_html = final_html.replace('{IMG_EDA_3}', get_image_base64(nb, 'c40d571d', 2))

# Beta Forest
final_html = final_html.replace('{IMG_ORDINAL_BETA}', get_image_base64(nb, '23a6d370', 0))

# Trazas Betas Individuales (7 imágenes loop)
final_html = final_html.replace('{IMG_TRACE_0}', get_image_base64(nb, 'f16d741b', 0))
final_html = final_html.replace('{IMG_TRACE_1}', get_image_base64(nb, 'f16d741b', 1))
final_html = final_html.replace('{IMG_TRACE_2}', get_image_base64(nb, 'f16d741b', 2))
final_html = final_html.replace('{IMG_TRACE_3}', get_image_base64(nb, 'f16d741b', 3))
final_html = final_html.replace('{IMG_TRACE_4}', get_image_base64(nb, 'f16d741b', 4))
final_html = final_html.replace('{IMG_TRACE_5}', get_image_base64(nb, 'f16d741b', 5))
final_html = final_html.replace('{IMG_TRACE_6}', get_image_base64(nb, 'f16d741b', 6))

# Ordinal Probability Curve
final_html = final_html.replace('{IMG_ORDINAL_PROB}', get_image_base64(nb, 'd31efefc', 0))

with open('presentacion_taller.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Presentación HTML renderizada exitosamente con la corrección escape MathJax, Trazas MCMC, Priors, EDA y Gráficos!")
