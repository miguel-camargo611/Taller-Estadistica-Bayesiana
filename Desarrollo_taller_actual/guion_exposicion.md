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
Utilizamos como predictores clave el tratamiento (si activamos Pool o no), la hora de alta congestión y emparejamientos netos. Y lo más importante: usamos pre-distribuciones *Normal-Inversa-Gamma* cerradas, asumiendo muchísima ignorancia inicial con una varianza altísima de diez mil dólares."

---

### Slide 4: Resultados Posteriores: Efecto UBER Pool (45 segundos)
**Orador 2:**
"Al actualizar matemáticamente la certidumbre con los datos empíricos de las fórmulas cerradas, llegamos a estos resultados posteriores. Observemos la métrica estelar: el Parámetro de Tratamiento $\beta_1$.
En nuestra tabla y distribuciones con Monte Carlo, confirmamos que el impacto de activar UBER Pool promedió un asombroso revés negativo de -$1,250 dólares por corte. La campana roja en el gráfico se localiza sólidamente por debajo de cero, con una probabilidad exacta de reducción de ganancias del **98.7%**. Categóricamente, UBER Pool fracasó a corto plazo."

---

### Slide 5: Diagnóstico Residual del Modelo (UBER) (20 segundos)
**Orador 3:**
"Nuestra afirmación del 98.7% de certeza es estadísticamente sólida. Si vemos en detalle la dispersión de nuestros residuos contra los valores ajustados, notamos una nube aleatoria exenta de patrones en embudo, validando en su totalidad la homosedasticidad inferida."

---

### Slide 6: Parte II - Movistar Arena & Setup Bayesiano (40 segundos)
**Orador 3:**
"Ahora, pasemos al *Movistar Arena*. Su mayor problema es predecir tipos de consumidores o 'Customer Types'. Sabemos que las personas compran impulsivamente (*Last-Minute*), moderadamente, o como parte de un plan anticipado (*Planner*).
Como las variables siguen un orden, usamos un enfoque numérico de **Logit Ordinal**. Aquí filtramos 1000 perfiles emparejando sus 'targets' ordinales contra precursores clave del diccionario ilustrado [Edad, Compras, etc]. Esto lo optimizamos programático a través de *MCMC*, infiriendo una Normal débil (con escala en cien) sobre tanto los betas como en los puntos de corte o _'cutpoints'_."

---

### Slide 7: EDA y Pruebas de Asociación (35 segundos)
**Orador 3:**
"Para blindar la homogeneidad de los datos, pre-testeamos con Kruskal-Wallis y Chi-Cuadrado si las categorías diferían. Y como demuestran nuestros p-valores fuertemente nulos y los boxplots, las diferencias son extremas y obvias. **Hallazgo principal:** A los compradores *Planner* es donde predomina el rango mayor de edad, la compra de muchas más boletas, y sobre todo, altísimos gastos adicionales en comida y mercancía. El ticket price, sin embargo, se comporta variable."

---

### Slide 8: Resultados Posteriores Ordinal Beta (40 segundos)
**Orador 1:**
"Tras insertar las covariables al algoritmo computacional MCMC de PyMC, obtenemos este *Forest Plot* recapitulando las medias y sus intervalos de confianza. En el recuadro inferior pueden ver a qué variable corresponde cada 'Beta'.
¿Qué explica la lealtad de un cliente hacia el estatus Planner? Como se evidencia, la edad, el número de tickets y ostentar altísimos gastos de concesión no se solapan con el cero. Por otra parte, la suscripción al fan mailing y las variables relativas al asiento muestran oscilaciones neutras menos decisivas."

---

### Slide 9: Diagnóstico Cadenas MCMC: Trazas Individuales (30 segundos)
**Orador 1:**
"Estos resultados predictivos están garantizados por el correcto mezclado de NUTS. En este carrusel horizontal o trazas, ilustramos separadamente las oscilaciones de los siete Betas. Su convergencia es ideal y no adolecen de auto-correlación fuerte, respaldando sólidamente nuestras simulaciones con un valor \(\hat{R}\) perfecto de 1."

---

### Slide 10: Curva Ordinal Latente Probabilidades (35 segundos)
**Orador 2:**
"¿Cómo se traduce esta puntuación a un comportamiento real? Este gráfico es clave: muestra las probabilidades de clasificación basándose en la puntuación latente logística (o `eta`). Las curvas y sus *cutpoints* o _theta_ actúan como divisores rígidos o barreras. Si la puntuación de nuestro modelo empuja a los individuos más allá de las fronteras naranjas impuestas, el usuario escapará probabilísticamente de la barrera de *Last-Minute* para internarse puramente en terreno *Planner*."

---

### Slide 11: Sinergia Operativa - Propuesta Estratégica (50 segundos)
**Orador 1:**
"Esto nos lleva de regreso al hilo conductual. El 'cuello de botella' logístico que quebraba los pronósticos financieros de UBER eran las peticiones masivas sorpresivas de forma asincrónica. Por decir un escenario, los jóvenes caóticos del *Last-Minute* saliendo sin advertencia de un coliseo agotando las grillas de autos y la plataforma ineficiente.
Nuestra **propuesta** integra la solución cruzando el modelo: Movistar Arena podría reservar y asegurar viajes de *Uber Pool Exclusivos* atados a las zonas *Planner* previas al concierto, asegurando densidad con anticipación."

---

### Slide 12: Conclusión (40 segundos)
**Orador 3:**
"Así las plataformas cooperarían rentablemente. UBER afianza su meta de ejecutar pools de alta densidad librándose del azar y de los fracasos de su experimento temprano, mientras el Arena disuelve congestiones caóticas en su logística externa, con una certidumbre paramétrica medible gracias al Bayes.
La moraleja del modelo es que podemos prender vínculos y alianzas productivas entre diferentes mercados basándonos explícitamente en la cuantificación de una probabilidad. Gracias."
