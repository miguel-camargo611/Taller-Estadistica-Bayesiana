# Guión de Exposición: Taller Integrado de Regresión Bayesiana
**(Duración objetivo: 7-8 minutos)**

---

### Slide 1: Portada (15 segundos)
**Orador 1:**
"Hola a todos. Hoy presentaremos nuestro análisis bayesiano, abordando casos de dos sectores muy dinámicos en la actualidad: la movilidad compartida con **UBER Pool** y la industria del entretenimiento masivo en el **Movistar Arena**."

---

### Slide 2: Introducción - El Hilo Conductor (30 segundos)
**Orador 1:**
"A simple vista, movilidad y conciertos parecen fenómenos desconectados. Sin embargo, ambos comparten un hilo conductor muy fuerte: **el comportamiento del consumidor en entornos inciertos**. Nuestro objetivo central es entender cómo factores logísticos y personales afectan las decisiones probabilísticas. A saber: ¿cómo un servicio genera pérdidas por mala empatía temporal? O ¿cómo anticipar quién nos compra una boleta ayuda a predecir picos logísticos?"

---

### Slide 3: Parte I - Caso UBER Pool y Setup Bayesiano (40 segundos)
**Orador 2:**
"Empezaremos analizando financieramente a UBER Pool. La pregunta que motivó nuestra regresión Bayesiana fue si introducir este servicio lograba aumentar las ganancias conjuntas entre choferes. Nuestra variable observada continua es `total_driver_payout`.
Utilizamos como predictores clave el tratamiento (si activamos Pool o no), la hora de alta congestión y emparejamientos netos. Y lo más importante: asumimos ignorancia inicial estipulando que los betas se distribuyen de forma normal con media 0 y varianza alta, y priorizamos un sigma de diez mil dólares."

---

### Slide 4: Distribuciones Posteriores: Efecto UBER Pool (45 segundos)
**Orador 2:**
"Al actualizar matemáticamente la certidumbre con los datos empíricos de las fórmulas cerradas, llegamos a estos resultados posteriores en la pantalla. *(El Orador desliza los distintos gráficos por cada variable en el carrusel de la derecha)*.
Si detallamos la tabla fija que ven a su izquierda, la métrica estelar siempre es el Parámetro de Tratamiento $\beta_1$.
Ese intervalo de credibilidad que oscila entre -2300 a -135 no cruza el cero. Esto confirma categóricamente que el efecto es negativo en la mayoría absoluta de los escenarios, indicando que UBER Pool redujo estructuralmente las ganancias del chofer."

---

### Slide 5: Diagnóstico Residual del Modelo (UBER) (20 segundos)
**Orador 3:**
"Nuestra inferencia está estadísticamente blindada. Si vemos en detalle la dispersión de nuestros residuos contra los valores ajustados, notamos una nube aleatoria exenta de patrones en embudo, validando en su totalidad la homosedasticidad teórica requerida."

---

### Slide 6: Parte II - Movistar Arena & Setup Bayesiano (40 segundos)
**Orador 3:**
"Ahora, pasemos al *Movistar Arena*. Su mayor problema es predecir tipos de consumidores. Sabemos que las personas compran impulsivamente (*Last-Minute*), moderadamente, o como parte de un plan anticipado (*Planner*).
Como las variables son tres escalones sucesivos, usamos un modelo de **Logit Ordinal**. Las distribuciones A Priori aquí son formales y dispersas: los betas distribuyen Normal con media cero y varianza de 100, para que el sistema de MCMC, mediante PyMC, logre inferir de forma objetiva sobre los 'cutpoints'."

---

### Slide 7: Selección de Variables y Análisis Bivariado (35 segundos)
**Orador 3:**
"Nuestro conjunto abarca indicadores de edad, tickets comprados y gasto en concesiones. Sin embargo, para blindar la utilidad del modelo, realizamos rigurosas pruebas formales. *(El Orador desliza los boxplots hasta la cuarta pestaña: Tablas)*.
Aquí pueden ver los p-valores de Kruskal-Wallis y Chi-Cuadrado: son infinitesimalmente bajos. Todos rechazan contundentemente la hipótesis nula, lo que visualizamos en los Boxplots anteriores: un perfil Planner difiere drásticamente de un Last-Minute desde los estadísticos base."

---

### Slide 8: Resultados Posteriores: 94% HDI (40 segundos)
**Orador 1:**
"Insertadas estas variables al NUTS posterior, obtenemos este Forest Plot de estimadores Beta. La lectura es clarísima: La Edad, el bloque de Tickets y gastar en comida tienen HDIs totalmente positivos a la derecha del cero, forzando la probabilidad de ser un cliente Planner. 
Sin embargo, noten la tabla inferior: **beta 5 (Seat Front) y beta 6 (Seat Balcony)** sí traslapan la línea del Cero en su estimación, volviéndose estadísticamente neutros e incapaces de direccionar a una de las clases."

---

### Slide 9: Diagnóstico Cadenas MCMC: Trazas (30 segundos)
**Orador 1:**
"Con la tranquilidad sobre la inferencia, observamos aquí nuestro carrusel de convergencias. El tamaño efectivo de muestras es abundante y los valores de R-hat son casi 1 perfecto, por lo que el algoritmo navegó impecablemente sobre los siete estimadores."

---

### Slide 10: Curva Ordinal Latente (35 segundos)
**Orador 2:**
"El resultado paramétrico aterriza aquí: la transformación Logit Ordinal Puntuación (o `eta` en el eje X) contra la probabilidad acumulada de cada perfil. Esta visualización se lee cruzando las barras divisorias o *Cutpoints*: Si sumas positivamente métricas, como edad y snacks, te alejas puramente hacia la derecha de la gráfica, escapando del espectro inicial azul del 'Last-Minute' y adentrándote irremediablemente en la zona de Planner."

---

### Slide 11: Sinergia Operativa - Propuesta Estratégica (50 segundos)
**Orador 1:**
"Para cerrar nuestro hilo conductor, la gran oportunidad operativa es cruzar y solucionar ambos problemas. Uber pierde su dinero por culpa del azar: los usuarios piden autos de forma lenta y desorganizada, por lo que nunca logran llenar los asientos a tiempo y gastaban gasolina dando vueltas. Por su parte, el Movistar Arena sufre un caos porque, al finalizar eventos, miles de personas salen de forma abrupta a pedir transporte, colapsando la zona.
La **Sinergia** es clara: El Movistar Arena puede ofrecer a sus clientes 'Planners' (los más organizados y predecibles) un paquete exclusivo que integre su boleta VIP con asientos en rutas pre-programadas de UBER Pool para el regreso."

---

### Slide 12: Conclusiones (30 segundos)
**Orador 3:**
"Con esta estrategia propuesta, ¡ambos ganan! UBER salva su logística y asegura rentabilidad teniendo por fin autos 100% llenos desde horas calculadas exactamente. Y el Movistar Arena gana al liberar la presión de sus puertas evacuando clientes directamente en rutas listas y seguras.
El valor real de todo lo que calculamos hoy radicó en tener la capacidad analítica estricta de predecir el orden dentro del caos, aislando estadísticamente a esos 'clientes organizados' para construir esta gran alianza de negocios. Muchas gracias."
