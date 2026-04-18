# Taller de Estadística Bayesiana: Análisis de Mercado Musical

Este repositorio contiene la resolución detallada del taller de Estadística Bayesiana aplicado a la industria de la música, específicamente para el sello discográfico **Loop Entertainment**.

## Estructura del Proyecto

El proyecto se divide en dos grandes bloques analíticos:

1.  **Parte I: Modelo de Aceptación de Canciones (Dirichlet-Multinomial)**
    *   Análisis de la percepción de 100 oyentes sobre una obra experimental.
    *   Visualización mediante **proporciones marginales** y **contornos pentagonales** (proyección del simplex de 5 categorías).
    *   Estudio de sensibilidad a la elección de la prior (Informativa, Débilmente Informada y No Informada).

2.  **Parte II: Modelo de Reproducciones en Plataformas (Bayesiano Normal)**
    *   Estimación de la media ($\mu$) y varianza ($\sigma^2_n$) del volumen de streaming diario en 4 plataformas (YouTube, Spotify, Deezer, Apple Music).
    *   Visualización avanzada mediante **grillas 3D y mapas de contorno** para cada escenario de prior.
    *   Comparativa de incertidumbre y volumen entre plataformas líderes y de nicho.

## Entregables

*   **[`solucion_taller.ipynb`](./solucion_taller.ipynb)**: Cuaderno de Jupyter con la resolución paso a paso de las 20 preguntas del taller. Incluye:
    *   Formulaciones matemáticas en LaTeX.
    *   Código en Python para el cálculo de parámetros posteriores.
    *   Análisis conceptual de cada resultado.
*   **[`solucion_taller.tex`](./solucion_taller.tex)**: Reporte técnico formal en LaTeX diseñado para la alta gerencia. Sintetiza los hallazgos en tres decisiones críticas:
    1.  Validación de la aceptación de la obra.
    2.  Identificación de plataformas con mayor potencial (Spotify/YouTube).
    3.  Recomendación estratégica de festival para el lanzamiento (Rock al Parque).

## Requisitos Técnicos

Para ejecutar el notebook, se requiere un entorno de Python 3 con las siguientes librerías:
*   `numpy`
*   `matplotlib`
*   `scipy`
*   `pandas`
*   `seaborn`

## Conclusiones Principales

Basándose en el escenario de **Prior No Informada** (para garantizar la objetividad), se concluye que:
*   Spotify es el canal con mayor tracción diaria (~5180+ reproducciones).
*   La canción tiene una aceptación base del 51.5\%, lo que la hace viable para un lanzamiento en nichos alternativos.
*   Se recomienda invertir el presupuesto publicitario mayoritariamente en Spotify y YouTube.

---
**Autores:** Miguel Camargo, Nicolas Cardenas y Camilo Hernandez  
**Institución:** Universidad Externado de Colombia  
**Fecha:** Marzo 2026
