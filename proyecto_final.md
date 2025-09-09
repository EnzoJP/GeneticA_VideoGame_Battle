
# Comparación de algoritmos genéticos para combatir un jefe del videojuego, basado en turnos, Persona 3

### Integrantes: Martínez Paula Y Enzo Palau

---

## Índice
- [Introducción](#introducción)
- [Descripción del juego](#descripción-del-juego)
    - [Mecánicas del juego](#mecánicas-del-juego)
    - [Personajes](#personajes)
    - [Enemigo: Sleeping Table](#enemigo-sleeping-table)
    - [Ítems disponibles](#ítems-disponibles)
- [Marco Teórico](#marco-teórico)
    - [Algoritmo Aleatorio](#algoritmo-aleatorio)
    - [Algoritmo Genético: Fundamentos Teóricos](#algoritmo-genético-fundamentos-teóricos)
    - [Algoritmo Genético modelo](#algoritmo-genético-modelo)
    - [Algoritmo Genético modificado](#algoritmo-genético-modificado)
    - [Algoritmo NSGA-II](#algoritmo-nsga-ii)
- [Diseño Experimental](#diseño-experimental)
    - [Métricas Utilizadas](#métricas-utilizadas)
    - [Configuración y parámetros de los algoritmos](#configuración-y-parámetros-de-los-algoritmos)
        - [Algoritmo Genético Modelo](#algoritmo-genético-modelo)
        - [Algoritmo Genético Modificado](#algoritmo-genético-modificado)
        - [Algoritmo NSGA-II](#algoritmo-nsga-ii)
    - [Funciones de Fitness (Aptitud)](#funciones-de-fitness-aptitud)
        - [Funciones de fitness para los algoritmos genéticos](#funciones-de-fitness-para-los-algoritmos-genéticos)
        - [Función de fitness para NSGA-II](#función-de-fitness-para-nsga-ii)
    - [Descripción de los experimentos realizados](#descripción-de-los-experimentos-realizados)
    - [Resultados Obtenidos](#resultados-obtenidos)
        - [Daños Realizados](#daños-realizados)
        - [Daños recibidos por algoritmo](#daños-recibidos-por-algoritmo)
        - [Muertes por algoritmo](#muertes-por-algoritmo)
        - [Turnos en partidas ganadas por algoritmo](#turnos-en-partidas-ganadas-por-algoritmo)
        - [Winrate](#winrate)
        - [Tabla comparativa de resultados obtenidos en 1000 simulaciones - función de fitness 1](#tabla-comparativa-de-resultados-obtenidos-en-1000-simulaciones---función-de-fitness-1)
        - [Tabla comparativa de resultados obtenidos en 1000 simulaciones - función de fitness 2](#tabla-comparativa-de-resultados-obtenidos-en-1000-simulaciones---función-de-fitness-2)
        - [Frente de pareto obtenido con NSGA-II](#frente-de-pareto-obtenido-con-nsga-ii)
- [Análisis y Discusión de Resultados](#análisis-y-discusión-de-resultados)
- [Conclusiones Finales](#conclusiones-finales)
- [Bibliografía y referencias](#bibliografía-y-referencias)


## Introducción

Persona 3 es un videojuego de rol japonés por turnos (o sus siglas JRPG) desarrollado por Atlus en el año 2006 para la consola PlayStation 2. En este juego, el jugador controla a un grupo de estudiantes que se enfrentan contra criaturas conocidas como "sombras" en combates por turnos. En estos combates, el jugador debe elegir las acciones de sus personajes, como atacar, usar habilidades especiales, usar ítems diversos, etc. Además, el jugador debe tener en cuenta las debilidades y resistencias de los enemigos, ya que algunos enemigos son débiles a ciertos tipos de ataques y resistentes a otros.

El enemigo que se eligió para realizar el proyecto es **Sleeping Table**, un enemigo que aparece en el piso 135 de la torre de Tartarus, la cual es una mazmorra que el jugador debe explorar. Este es un enemigo que tiene una alta resistencia a la mayoría de los ataques y no tiene debilidades, por lo que es considerado un *jefe* muy difícil.

Para combatir a este enemigo, se implementaron cuatro algoritmos diferentes:
1. **Algoritmo Aleatorio**: Este algoritmo selecciona una acción al azar entre las disponibles hasta que el enemigo es derrotado o el jugador es derrotado.
2. **Algoritmo Genético de modelo**: Este algoritmo genético es lo mas parecido a un algoritmo genético tradicional, descripto en el libro de *Inteligencia Artificial: Un Enfoque Moderno* de Russell y Norvig con un pequeño agregado de elitismo.
3. **Algoritmo Genético modificado**: Este algoritmo genético es una versión modificada del algoritmo genético de base, en el cual se implementaron algunas mejoras para aumentar la eficacia del algoritmo y adaptarlo mejor al problema en cuestión.
4. **Algoritmo NSGA-II**: Este algoritmo es una implementación del algoritmo NSGA-II, el cual es un algoritmo genético multiobjetivo. En este caso, se consideraron dos objetivos: minimizar las muertes de los personajes y maximizar el daño infligido al enemigo.

Finalmente, el presente informe se encuentra dividido en diferentes secciones: en la sección de [Descripción del juego](#descripción-del-juego), se detallan las mecánicas del juego, los personajes y las características del enemigo seleccionado. En la sección de [Marco Teórico](#marco-teórico), se describen los algoritmos implementados y sus fundamentos teóricos. En la sección de [Diseño Experimental](#diseño-experimental), se explica cómo se llevaron a cabo los experimentos y qué métricas se utilizaron para evaluar el desempeño de los algoritmos. En la sección de [Análisis y Discusión de Resultados](#análisis-y-discusión-de-resultados), se presentan los resultados obtenidos y se discuten las diferencias entre los algoritmos. Finalmente, en la sección de [Conclusiones Finales](#conclusiones-finales), se resumen los hallazgos más importantes y se sugieren posibles mejoras para futuros trabajos.

## Descripción del juego

Persona 3 es un videojuego de rol japonés por turnos (o sus siglas JRPG). En un RPG por turnos, el combate funciona de una manera parecida a un juego de mesa de estrategia: los participantes actúan por turnos. El jugador tiene un tiempo para decidir qué acción realizará su personaje (atacar, defenderse, usar un objeto, lanzar un hechizo, etc.), y luego el enemigo responde en su propio turno. Esto continúa hasta que uno de los bandos es derrotado.
El sistema de combate de Persona 3 se basa en este formato. El jugador controla a un personaje que pertenece a un grupo, y estos enfrentan a diferentes enemigos. Cada personaje puede usar ataques físicos, usar [ítems](#ítems-disponibles) o invocar “Personas”, entidades o manifestaciones de sus "yo" interior que representan sus habilidades mágicas o espirituales, para realizar otro tipo de habilidades. El combate gira en torno a identificar y aprovechar las debilidades del enemigo (por ejemplo, un enemigo puede ser débil al fuego, pero resistente al hielo), ya que de esta forma este recibirá más daño. 

### Mecánicas del juego

* **HP (Health Points)**: representan la vida del personaje. Si bajan a cero, el personaje queda incapacitado.
* **SP (Skill Points)**: son equivalentes al “maná” en otros juegos; sirven para usar habilidades especiales (hechizos, curaciones, técnicas avanzadas) las cuales consumen SP, por lo que es importante gestionarlos adecuadamente.
* **Ataques físicos y mágicos**: cada personaje puede realizar ataques físicos o usar habilidades mágicas a través de su *Persona*, además de poder hacer ataques básicos físicos que no consumen nada.
* **Debilidades y resistencias**: cada enemigo o personaje tiene afinidades elementales. Por ejemplo, algunos pueden ser débiles al fuego pero resistentes al hielo.

  * *Débil*: el que es débil a un elemento, recibe daño multiplicado de ese mismo.
  * *Resistente*: recibe menos daño.
  * *Bloquea*: el ataque no surte efecto y no recibirá daño en absoluto.
  * *Absorbe*: en lugar de recibir daño, recuperará una cantidad de HP (generalmente el mismo valor que el daño que habría recibido o una menor cantidad).
  * *Repele*: devuelve parte del ataque al atacante (menos para los ataques de tipo "Almighty" o nuclear).

En *Persona 3* existen 10 tipos de daño: fuego, hielo, electricidad, viento, luz, oscuridad, nuclear, físico perforante, físico cortante y físico de golpe. Cada uno de estos ataques tiene una probabilidad de causar un estado alterado en el enemigo (por ejemplo, congelar, quemar, aturdir, etc).

* **Probabilidades y azar**: el combate no es determinista, sino que cada acción tiene una chance de éxito o fallo:
  - Un ataque, ya sea físico o mágico, puede fallar o ser esquivado.
  - Algunos ataques infligen estados alterados (miedo, sueño, parálisis, etc.) con una probabilidad determinada.
  - Existen “críticos” (golpes especialmente fuertes) que dependen de la suerte.

Esto significa que cada batalla tiene un componente de incertidumbre, y la estrategia debe adaptarse a esas probabilidades.

Los personajes y enemigos tienen estadísticas que afectan estas probabilidades, como la precisión, la evasión, la resistencia a estados alterados, etc. Por ejemplo, un personaje con alta precisión tendrá más chances de acertar sus ataques, mientras que un enemigo con alta evasión será más difícil de golpear (porque esquiva más seguido). Estas probabilidades pueden modificarse durante el combate mediante habilidades especiales, ítems o efectos de estado.

En el caso de Persona 3, el jugador controla completamente a un solo personaje, el protagonista, y los demás son controlados por el propio juego, aunque uno puede darle directrices generales, llamadas tácticas, de cómo encarar el combate. En nuestra implementación, le dejamos ciertas tácticas por defecto a los personajes no controlables.

La forma de perder una pelea es un tanto particular en este videojuego. El jugador pierde si el protagonista (Makoto Yuki), muere, independientemente de si los otros personajes del grupo están vivos o no. Si Makoto muere, el juego termina y el jugador debe reiniciar desde el último punto de guardado. Por lo tanto, la supervivencia de el protagonista es crucial para continuar en el juego y poder ganar la batalla (lo cual sucede si la vida del o los enemigos llega a cero).

### Personajes
El grupo de personajes o "*party*" está compuesto por 4 personajes:

- Makoto Yuki: El protagonista, un personaje equilibrado con habilidades de ataque y soporte. Es el personaje controlable por el jugador, por lo que sus tácticas son decididas por el algoritmo que esté jugando.
    - Estadísticas:
        - HP: 366
        - SP: 246
        - Defensa: 24
        - Ataque: 20
        - Probabilidad de crítico: 15%
        - Resiste: Fuego
    - Habilidades:
        - Ataque básico: Inflinge daño físico cortante leve. Sin costo.
        - Recarm: Revive a un aliado caído con un 50% de su HP. Cuesta 20 SP.
        - Mediarama: Cura moderadamente a todos los aliados. Cuesta 16 SP.
        - Rakunda: Le sube la defensa a un aliado a elección. Cuesta 6 SP.
        - Bufula: Inflinge daño moderado de hielo a un enemigo con 10% de probabilidad de congelarlo. Cuesta 8 SP.
        - Torrent Shot: Inflinge daño físico perforante leve a un enemigo. Cuesta el 10% del HP actual del usuario.
        - Hamaon: Ataque de tipo "luz" que mata instantáneamente a un enemigo con un 40% de probabilidad. Cuesta 12 SP.

- Yukari Takeba: Especialista en ataques de viento y habilidades de curación. Su táctica es la siguiente: prioriza revivir a los aliados caídos, si están todos en el grupo vivos entonces prioriza curar. Si todos los aliados tienen más del 70% de su HP, entonces verifica que no hayan compañeros con estados alterados (pánico, miedo o angustia). Si no los hay, entonces ataca con ataques de viento o con su ataque básico.
    - Estadísticas:
        - HP: 287
        - SP: 285
        - Defensa: 24
        - Ataque: 18
        - Probabilidad de crítico: 10%
        - Bloquea: Viento
        - Debilidad: Electricidad
    - Habilidades:
        - Ataque básico: Inflinge daño físico perforante leve. Sin costo.
        - Recarm: Revive a un aliado caído con un 50% de su HP. Cuesta 20 SP
        - Mediarama: Cura moderadamente a todos los aliados. Cuesta 16 SP.
        - Me Patra: Cura los estados alterados de pánico, miedo y angustia a todos los aliados. Cuesta 6 SP.
        - Garula: Inflinge daño moderado de viento al enemigo. Cuesta 6 SP.
        - Diarama: Cura moderadamente a un aliado a elección. Cuesta 8 SP.

- Junpei Iori: Luchador ágil con habilidades físicas. NN tiene una táctica definida, por lo que sus habilidades son elegidas al azar (las que suben la defensa a los aliados solo son agregadas a la lista de elecciones si los aliados no tienen la defensa subida).
    - Estadísticas:
        - HP: 381
        - SP: 201
        - Defensa: 24
        - Ataque: 20
        - Probabilidad de crítico: 25%
        - Resiste: Fuego
        - Debilidad: Viento
    - Habilidades: 
        - Ataque básico: Inflinge daño físico cortante leve. Sin costo.
        - Rakukaja: Le sube la defensa a un aliado a elección. Cuesta 6 SP.
        - Mararukaja: Sube la defensa de todos los aliados. Cuesta 12 SP.
        - Torrent Shot: Inflinge daño físico perforante leve a un enemigo. Cuesta el 10% del HP actual del usuario.
        - Blade of Fury: Inflinge daño físico cortante moderado a un enemigo. Cuesta el 16% del HP actual del usuario.
        - Counterstrike: 15% de probabilidad de contraatacar un ataque físico con un ataque físico leve. Habildad pasiva.

- Akihiko Sanada: Guerrero con habilidades de electricidad. Su táctica es la siguiente: Prioriza las habilidades de "buffos" o "debuffos", las cuales aumentan las estadísticas de los aliados o disminuyen las del enemigo. Tiene un 85% de probabilidad de usar estas habilidades (si es que no están activas en ese momento. Es decir, si el enemigo ya tiene la defensa baja entonces no va a bajarle la defensa al enemigo), sino ataca con ataques físicos o de electricidad.
    - Estadísticas:
        - HP: 369
        - SP: 210
        - Defensa: 24
        - Ataque: 22
        - Probabilidad de crítico: 10%
        - Bloquea: Electricidad
        - Debilidad: Hielo
    - Habilidades:
        - Ataque básico: Inflinge daño físico de golpe leve. Sin costo.
        - Zionga: Inflinge daño moderado de electricidad a un enemigo con 10% de probabilidad de paralizarlo. Cuesta 8 SP.
        - Tarunda: Le baja el ataque a un enemigo a elección. Cuesta 6 SP.
        - Rakunda: Le baja la defensa a un enemigo a elección. Cuesta 6 SP.
        - Sukunda: Le baja la evasión a un enemigo a elección. Cuesta 6 SP.
        - Sonic Punch: Inflinge daño físico de golpe leve a un enemigo. Cuesta el 9% del HP actual del usuario.
    

### Enemigo: Sleeping Table

El enemigo elegido fue "Sleeping Table", un jefe que aparece en el piso 135 de la torre de Tartarus, la cual podría decirse que es el "nido" de los "Shadows", quienes son los enemigos. Esta torre tiene 264 pisos en total la cual cuenta con 25 jefes (y uno opcional). Este enemigo es muy resistente y no tiene debilidades, por lo que es considerado un jefe muy difícil.
- Estadísticas:
    - HP:1700
    - SP: 500
    - Resiste: Físico cortante, Físico perforante, Físico de golpe, Fuego.
    - Bloquea: Luz, Oscuridad.
    - Defensa: 20
    - Ataque: 24
    - Probabilidad de crítico: 20%
    - Probabilidad de fallar: 5%
- Habilidades:
    - Strike attack: Ataque básico que inflinge daño físico de golpe leve. Sin costo.
    - Hamaon: Ataque de tipo "luz" que mata instantáneamente a un enemigo con un 40% de probabilidad. Cuesta 12 SP.
    - Maragidyne: Inflinge daño fuerte de fuego a todos los enemigos. Cuesta 24 SP.
    - Megidola: Inflinge daño fuerte de "nuclear" a todos los enemigos. Cuesta 65 SP.
    - Evil Touch: Aplica el estado alterado "miedo" a un enemigo con un 40% de probabilidad de acertar. Cuesta 5 SP.
    - Ghastly Wail: Mata instantáneamente a todos los enemigos que tengan el estado de "miedo" con un 100% de probabilidad de acertar. Cuesta 15 SP.
    - Fear Boost: Incrementa la probabilidad de acertar el estado de "miedo" en un 15%. Habilidad Pasiva.

Cada ataque de 'Sleeping Table', menos 2, tiene una probabilidad de ser usado en cada turno:
    - Hamaon: 25%
    - Maragidyne: 40%
    - Megidola: 15%
    - Evil Touch: 20%
Si no tiene SP suficiente para usar alguna de estas habilidades, usa su ataque básico. 
Ghastly Wail solo lo usará si hay al menos un enemigo que tiene el estado de "miedo" en ese turno.

### Ítems disponibles

Hay varios ítems disponibles en el juego, pero para este combate se utilizaron los siguientes:

- **Un Soma**: Se utiliza en todos los miembros del grupo, restaurando por completo tanto su HP como su SP. No se puede utilizar en aliados caídos. 

- **Dos Precious Egg**: Restaura completamente los SP de un aliado. No se puede utilizar en aliados caídos.

- **Un Magic Mirror**: Inflinge a todos los miembros del grupo el estado "Repeler elemento", una barrera que repele un ataque mágico (excepto ataques Almighty o "nuclear") durante un turno.

## Marco Teórico

### Algoritmo Aleatorio

Es un algoritmo muy simple que selecciona una acción al azar entre las disponibles hasta que el enemigo es derrotado o el jugador es derrotado. Este algoritmo no tiene en cuenta las características del enemigo ni las habilidades de los personajes, por lo que su desempeño es muy variable.

-> Problemas encontrados:

Al generar una acción al azar, el algoritmo puede seleccionar acciones que no son legales en el contexto del juego, como usar un ítem que no está disponible o encadenar ataques que no son posibles debido a el número de sp disponible.
Para solucionar esto, se implementaron ciertas restricciones en la generación de acciones:
+ No se pueden usar ítems si no hay ítems disponibles, si el algoritmo selecciona un ítem en este caso, se selecciona otra acción al azar.
+ No se pueden encadenar ataques si no hay sp disponible, si el algoritmo selecciona un ataque en este caso, se usará un ítem reservado de "Precious Egg" para recuperar sp y luego se seguirá con la siguiente acción al azar.

Este algoritmo se utiliza como una línea base para comparar el desempeño de los otros algoritmos implementados.

### Algoritmo Genético: Fundamentos Teóricos

Un algoritmo genético es un algoritmo de búsqueda y optimización inspirado en el proceso de selección natural. Estos algoritmos utilizan técnicas como la selección, el cruce y la mutación para evolucionar una población de soluciones hacia una solución óptima o cercana a la óptima.

Consta de los siguientes pasos:
1. **Inicialización**: Se genera una población inicial de soluciones aleatorias asegurando que sean válidas dentro del contexto del juego.
2. **Evaluación**: Se evalúa la aptitud (Fitness) de cada solución en la población utilizando una función de aptitud que reproduce el combate contra el enemigo y mide el desempeño de la solución.
3. **Selección**: Se seleccionan las soluciones más aptas para reproducirse y generar una nueva población.
4. **Cruzamiento (Crossover)**: Se combinan las soluciones seleccionadas para crear nuevas soluciones mediante un proceso de cruce.
5. **Mutación**: Se aplican pequeñas modificaciones aleatorias a algunas soluciones para mantener la diversidad genética.
6. **Reemplazo**: Se reemplaza la población actual con la nueva población generada.
7. **Terminación**: Se repiten los pasos 2 a 6 hasta que se cumple un criterio de terminación, como alcanzar un número máximo de generaciones o encontrar una solución satisfactoria.

En adición, se pueden implementar técnicas adicionales como el elitismo, que consiste en conservar las mejores soluciones de una generación a la siguiente o eliminar las menos aptas para asegurar que no se pierdan las mejores soluciones encontradas hasta el momento, torneos de selección, etc.

### Algoritmo Genético modelo

Es un algoritmo genético tradicional, descripto en el libro de *Inteligencia Artificial: Un Enfoque Moderno* de Russell y Norvig, este algoritmo está compuesto por los siguientes componentes:

- **Representación de la solución**: Cada solución es representada como una secuencia de acciones (genes) que el personaje debe realizar en el combate. Cada acción puede ser un ataque, un ataque mágico o el uso de un ítem. La longitud de la secuencia es fija y se determina antes de la ejecución del algoritmo, se determino que una longitud de 50 acciones es mas que suficiente para derrotar al enemigo.
Por supuesto, se deben tener en cuenta las restricciones mencionadas anteriormente en [Algoritmo Aleatorio](#algoritmo-aleatorio) para asegurar que las soluciones generadas sean válidas.

- **Función de aptitud (Fitness)**: La función de aptitud evalúa el desempeño de cada solución en la población. En este caso, se simula el combate contra el enemigo utilizando la secuencia de acciones representada por la solución las dos funciones utilizadas se describen en detalle en la sección [Funciones de Fitness (Aptitud)](#funciones-de-fitness-aptitud).

- **Cruce (Crossover)**: Se utiliza un cruce de un punto estándar, donde se selecciona un punto aleatorio en la secuencia de acciones y se mezclan las acciones de dos soluciones para crear hijos.

-> Problemas encontrados:

1. El cruce puede generar soluciones inválidas si las acciones seleccionadas no son legales en el contexto del juego por ejemplo, usar un ítem que no está disponible(es decir en la secuencia generada esta duplicado dicho ítem)

- Solución: Para ser justos y no perder de vista soluciones potencialmente buenas, se decidió que si se generaba una solución con ítems duplicados, se aplicaría el siguiente procedimiento: se contaba cuántas veces se había usado cada ítem en la secuencia y si se había usado más veces de las disponibles, medimos el fitness de la solución quedandonos solo con la primera aparición de cada ítem y reemplazando las apariciones restantes por ataques aleatorios y luego se medía el fitness de la solución quedandonos con la aparición última de cada ítem y reemplazando las apariciones restantes por ataques aleatorios, finalmente se tomaba el fitness más alto de las dos soluciones generadas.

2. El cruce puede generar soluciones que no fueran legales en términos de sp disponible (por ejemplo, encadenar ataques que no son posibles debido a el número de sp disponible).

- Solución: Se procedió de la misma manera que en el caso de [Algoritmo Aleatorio](#algoritmo-aleatorio), es decir, si se generaba una solución con ataques encadenados sin sp suficiente, se usaba un ítem reservado de "Precious Egg" para recuperar sp y luego se seguía con la siguiente acción aleatoria.

- **Mutación**: Se aplica una mutación aleatoria a cada acción en la secuencia con una cierta probabilidad. Si se selecciona una acción para mutar, se reemplaza por una acción aleatoria válida.

-> Problemas encontrados:

1. La mutación puede generar soluciones inválidas si por ejemplo se muta una acción a un ítem que no está disponible.
- Solución: El criterio que adoptamos fue de no permitir la mutación a un ítem si no hay ítems disponibles, en ese caso se selecciona otra acción al azar.

- **Elitismo**: Para asegurar que podamos converger rápidamente a una buena solución, se implementó elitismo, conservando las mejores soluciones de una generación a la siguiente y reemplazando a las peores 10 soluciones de la nueva generación con las mejores soluciones de la generación anterior.

- **Selección final**: El criterio de parada de la evolución es alcanzar un número máximo de generaciones y devolver la mejor solución encontrada de la última generación.

Se decidió implementar este algoritmo genético de modelo para tener una línea de base para comparar con el algoritmo genético modificado ya que este representa un enfoque más tradicional, sencillo y general, mientras que el algoritmo modificado está más adaptado al problema en cuestión plasmando nuestras ideas y mejoras.

### Algoritmo Genético modificado

Es una versión modificada del algoritmo genético modelo, en el cual se implementaron algunas mejoras para aumentar la eficacia del algoritmo y adaptarlo mejor al problema en cuestión. Las modificaciones realizadas son las siguientes:

- **Cruce (Crossover)**: Se implementó un cruce de dos puntos en lugar de un cruce de un punto. Esto permite una mayor diversidad en las soluciones generadas y puede ayudar a evitar la convergencia prematura.

- **Cortado de secuencia**: Se implementó un mecanismo para cortar la secuencia de acciones si el enemigo es derrotado antes de que se complete la secuencia. Esto permite que las soluciones sean más eficientes y evita acciones innecesarias, ya que en el algoritmo modelo, si el enemigo era derrotado en la acción 30 de una secuencia de 50, las acciones 31 a 50 seguían siendo tenidas en cuenta en las posteriores evaluaciones, cruces, etc, lo que no tiene sentido e introduce ruido en la evaluación de la aptitud; para solucionar esto, se decidió que si el enemigo era derrotado antes de completar la secuencia, se cortaban todas las secuencias de acciones en la posición donde el enemigo fue derrotado.

-> Problemas encontrados:

1. Al cortar la secuencia demasiado temprano, debido a la cantidad de probabilidades en el combate, se podría estar perdiendo la oportunidad de encontrar soluciones mejores que podrían haber surgido en las acciones restantes o que podrían haber sido útiles pero tienen demasiado poco margen de error en un combate donde hay muchas probabilidades involucradas y cada combate es diferente al anterior.

- Solución: Se decidió que si el enemigo era derrotado antes de completar la secuencia el cortado se podía cortar las soluciones hasta la posición numero 15, es decir, si el enemigo era derrotado en la acción 10, se cortaba la secuencia en la posición 15, si era derrotado en la acción 20, se cortaba en la posición 20 y así sucesivamente, esto permite que las soluciones tengan un cierto margen de error y no se pierdan soluciones potencialmente buenas.

- **Función de sentido común**: Se implementó una función de sentido común que analiza la secuencia de acciones y realiza ajustes para mejorar la eficiencia y efectividad de la solución. Esta función se aplica después de la mutación,cruce y antes de la evaluación de la aptitud.
Mas concretamente, esta función mira las 10 primeras acciones de la secuencia en búsqueda de acciones potencialmente ineficientes, como por ejemplo, usar un ítem de "Precious Egg" para recuperar sp cuando no se ha usado tantos ataques mágicos que consuman sp, usar ataques físicos cuando los mágicos son más efectivos contra el enemigo, etc. Si se encuentra una acción ineficiente, se reemplaza por una acción aleatoria mejor.

- **Selección final y torneo**: Para decidir que soluciones son las mejores, en cada nueva generación se guardan en una lista a las mejores 3 soluciones, de esta manera, podemos guardar soluciones potencialmente buenas que luego,de otra forma se perderían en el proceso.
Una vez que se alcanza el número máximo de generaciones, se realiza un torneo entre las mejores 10 soluciones de todas las generaciones para determinar la mejor solución final. En este torneo, cada solución se evalúa en múltiples combates (25 c/u) contra el enemigo y se mide su desempeño. La solución que obtiene el mejor desempeño en el torneo es seleccionada como la mejor solución final.

La implementación de estas modificaciones tiene como objetivo mejorar la eficiencia y efectividad del algoritmo genético,tratando de que con nuestro conocimiento del problema, podamos guiar la evolución hacia soluciones con mayor probabilidad de éxito.

### Algoritmo NSGA-II

NSGA-II (Non-dominated Sorting Genetic Algorithm II) es un algoritmo evolutivo multiobjetivo ampliamente utilizado para resolver problemas en los que se busca optimizar simultáneamente dos o más objetivos que pueden ser conflictivos entre sí. A diferencia de los algoritmos genéticos tradicionales, que suelen trabajar con una única función de aptitud, NSGA-II mantiene una población de soluciones y utiliza conceptos de dominancia y diversidad para aproximar el conjunto de soluciones óptimas conocido como *frontera de Pareto*.

#### Principales características de NSGA-II

- **Ordenamiento por dominancia no dominada:** NSGA-II clasifica la población en diferentes frentes según el principio de dominancia de Pareto. Una solución domina a otra si es al menos igual de buena en todos los objetivos y mejor en al menos uno. El primer frente contiene las soluciones no dominadas (las mejores), el segundo frente contiene las soluciones dominadas solo por las del primer frente, y así sucesivamente.

- **Preservación de la diversidad (crowding distance):** Para mantener la diversidad entre las soluciones y evitar la convergencia prematura, NSGA-II utiliza una métrica llamada *crowding distance*, que mide cuán cerca están las soluciones entre sí en el espacio de los objetivos. Al seleccionar soluciones para la siguiente generación , se da preferencia a aquellas con mayor crowding distance, promoviendo así una distribución más uniforme a lo largo de la frontera de Pareto.

- **Selección elitista:** NSGA-II combina la población actual con la descendencia generada y selecciona las mejores soluciones (según el orden de dominancia y la crowding distance) para formar la nueva población. Esto asegura que las mejores soluciones encontradas hasta el momento no se pierdan entre generaciones.

- **Operadores genéticos estándar:** Utiliza operadores de cruce (crossover) y mutación similares a los de los algoritmos genéticos tradicionales para generar nuevas soluciones a partir de las existentes.

#### Aplicación en el proyecto

En el contexto de este trabajo, NSGA-II se implementó para optimizar simultáneamente dos objetivos principales en el combate contra el jefe Sleeping Table:

1. **Minimizar la cantidad de muertes de los personajes:** Se busca que la estrategia elegida permita que la mayor cantidad posible de personajes sobreviva al combate.
2. **Maximizar el daño infligido al enemigo:** Se intenta que la secuencia de acciones cause el mayor daño posible al jefe, incrementando las probabilidades de victoria.

Cada individuo en la población representa una secuencia de acciones (ataques o ítems) que los personajes pueden realizar durante el combate. La evaluación de cada individuo se realiza simulando el combate y calculando los valores de ambos objetivos.

Se decidió utilizar la misma función de sentido común, crossover de dos puntos y mutación del algoritmo genético modificado para mantener la coherencia en la representación de las soluciones y aprovechar las mejoras introducidas en dicho algoritmo.

Para la implementación se utilizó la librería `pymoo`, que facilita la aplicación de NSGA-II y el manejo de problemas multiobjetivo en Python.

La elección de NSGA-II para este proyecto se basó en su capacidad para manejar múltiples objetivos de manera efectiva, lo que es crucial en un entorno de combate donde se deben equilibrar diferentes aspectos del desempeño ya que a priori no existe una única solución óptima, sino un conjunto de soluciones que ofrecen diferentes compromisos entre los objetivos.

## Diseño Experimental

### Métricas Utilizadas

En este trabajo se utilizaron las siguientes métricas para evaluar el desempeño de los algoritmos:

- **Winrate (Tasa de Victoria):** Es la métrica principal y representa el porcentaje de combates ganados sobre el total de simulaciones realizadas por cada algoritmo. Se calcula como la cantidad de veces que el grupo de personajes derrota al jefe dividido por el número total de combates simulados. Esta métrica es fundamental porque refleja directamente la efectividad de la estrategia generada por cada algoritmo.

- **Muertes:** Indica el número de personajes que mueren durante el combate en las simulaciones. Se mide contando cuántos personajes quedan fuera de combate al finalizar cada pelea. Es relevante porque un menor número de muertes implica una estrategia más segura y sostenible para el grupo.

- **Daño Realizado:** Es el daño total infligido al jefe por los personajes durante el combate. Se obtiene sumando el daño causado en cada turno. Esta métrica es importante porque muestra la capacidad ofensiva de la estrategia.

- **Daño Recibido:** Representa el daño total recibido por los personajes a lo largo del combate. Se calcula sumando el daño recibido en cada turno. Es relevante porque estrategias que minimizan el daño recibido tienden a ser más robustas y a aumentar la supervivencia del grupo.

- **Promedio de Turnos en Soluciones Ganadoras:** Indica la cantidad promedio de turnos necesarios para derrotar al jefe en aquellas simulaciones donde se obtuvo la victoria. Se mide contando los turnos en cada victoria y promediando. Esta métrica es útil para evaluar la eficiencia temporal de la estrategia: menos turnos suelen implicar una estrategia más directa y efectiva.

- **Tiempo de Ejecución:** Es el tiempo que tarda cada algoritmo en completar la simulación. Se mide utilizando temporizadores en el código durante la ejecución de cada algoritmo. Es relevante porque permite comparar la eficiencia computacional y la viabilidad práctica de cada enfoque, especialmente en contextos donde el tiempo de cómputo es limitado.

Estas métricas fueron seleccionadas porque, en conjunto, permiten evaluar tanto la efectividad (ganar el combate), la seguridad (minimizar muertes y daño recibido), la eficiencia (daño realizado y turnos necesarios) y el costo computacional (tiempo de ejecución) de las estrategias generadas por los diferentes algoritmos.

### Configuración y parámetros de los algoritmos

A continuación se detallan los parámetros utilizados en cada uno de los algoritmos implementados,cabe destacar que cada uno recibe una secuencia de acciones inicial aleatoria y luego evoluciona dicha secuencia.

#### Algoritmo Genético Modelo

- **Tamaño de la población:** 25
- **Número de generaciones:** 30
- **Probabilidad de mutación:** 0.10
- **Longitud de la secuencia de acciones:** 50

- Se decidió usar estos parámetros para tener una población suficientemente diversa y permitir una evolución adecuada sin un costo computacional excesivo, ya que cada evaluación de fitness implica simular un combate completo y esto tendría un impacto significativo en el tiempo de ejecución. Se realizaron diversas pruebas y estos fueron los mejores parámetros encontrados en relación costo-beneficio.

#### Algoritmo Genético Modificado

- **Tamaño de la población:** 25
- **Número de generaciones:** 30
- **Probabilidad de mutación:** 0.10
- **Longitud de la secuencia de acciones:** 50

- Se mantuvieron los mismos parámetros que en el algoritmo genético modelo para asegurar una comparación justa entre ambos algoritmos y evaluar el impacto de las modificaciones introducidas.

#### Algoritmo NSGA-II

- **Tamaño de la población:** 35
- **Número de generaciones:** 55
- **Probabilidad de mutación:** 0.10
- **Longitud de la secuencia de acciones:** 50
- **Número de objetivos:** 2 (Minimizar muertes y maximizar daño infligido)

- Se eligieron estos parámetros para permitir una exploración más amplia del espacio de soluciones, dado que NSGA-II maneja múltiples objetivos y requiere una población más grande para mantener la diversidad y cubrir adecuadamente la frontera de Pareto, ademas el uso de la librería `pymoo` permite manejar poblaciones más grandes sin un costo computacional tan elevado.

### Funciones de Fitness (Aptitud)

En esta sección se detallan las funciones de fitness utilizadas en cada uno de los algoritmos implementados, junto con la justificación de su elección. Para los algoritmos genéticos (modelo y modificado) se diseñaron dos funciones de fitness diferentes, mientras que para NSGA-II se utilizó una función de fitness simple adaptada al enfoque multiobjetivo.

#### Funciones de fitness para los algoritmos genéticos

**Función de fitness 1:**
```python
if won:
    enemy_max_hp = enemy.max_HP
    return 1000000 - turns*1000 - deaths*100 + (damage / enemy_max_hp)
else:
    return damage - deaths*10 - turns
```

En esta función de fitness, se asigna una alta recompensa por ganar el combate (1.000.000 puntos) y se penaliza el número de turnos y muertes, además de considerar el daño realizado al jefe. Si el combate no se gana, se penaliza el daño recibido y las muertes restándole puntos a el nivel de daño realizado, lo que nos asegura que las soluciones que ganen tengan una variedad de puntajes altos y las que no ganen tengan puntajes bajos, facilitando la selección de las mejores soluciones.

**Función de fitness 2:**
```python
# --- 1) if loose -> fitness very low
if not stats["won"]:
    return -1000 + (stats["damage_done"] / enemy.max_HP) * 500 - stats["deaths"] * 50

# --- 2) if won ->
# calculate score
turn_score   = 1 - (stats["turns"] / 50)
death_score  = 1 - (stats["deaths"] / 4)
damage_score = stats["damage_done"] / enemy.max_HP
hp_bonus     = (1 - stats["damage_taken"] / (4*Makoto.max_HP))

# wheights
W_TURN   = 0.4
W_DEATH  = 0.99
W_DAMAGE = 0.2
W_HP     = 0.1

score = (
    10000   # big bonus for winning
    + W_TURN   * turn_score   * 1000
    + W_DEATH  * death_score  * 1000
    + W_DAMAGE * damage_score * 1000
    + W_HP     * hp_bonus     * 1000
)

return score
```

Esta función de fitness es más compleja basada en pesos y considera múltiples aspectos del combate. Si el combate no se gana, se penaliza fuertemente la solución. Si se gana, se calcula un puntaje basado en varios factores: la cantidad de turnos (menos es mejor), las muertes (menos es mejor), el daño realizado (más es mejor) y el daño recibido (menos es mejor).Cada puntaje esta normalizado en relación al combate, en los turnos se divide por 50 (cantidad máxima de turnos), en las muertes por 4 (cantidad de personajes), en el daño realizado por la vida máxima del enemigo y en el daño recibido por la vida máxima total del grupo (aproximadamente).

Cada uno de estos factores tiene un peso diferente, reflejando su importancia relativa en la evaluación de la estrategia (por ejemplo se pondera mucho las muertes ya que es una métrica escencial). Luego se suman estos puntajes ponderados junto con un gran bono por ganar el combate para obtener el puntaje final de la solución.


#### Función de fitness para NSGA-II

**Función de fitness NSGA-II:**
```python
if not win:
    out["F"] = [deaths + 10, -damage]  # penalize losses heavily
else:
    out["F"] = [deaths, -damage]  # minimize deaths, maximize damage
```

En el caso de NSGA-II, se utilizó una función de fitness simple que retorna directamente los dos objetivos principales: la cantidad de muertes de los personajes y el daño infligido al jefe. Esto permite que el algoritmo construya la frontera de Pareto y explore los compromisos entre ambos objetivos, sin necesidad de combinar los valores en una única métrica.


### Descripción de los experimentos realizados

Para evaluar y comparar el desempeño de los diferentes algoritmos implementados, primero teníamos la tarea de codificar el combate contra el jefe Sleeping Table, asegurándonos de que todas las mecánicas del juego fueran representadas con precisión.
Para esto primeramente se planteo una extensa fase de investigación y recopilación de datos sobre las estadísticas, habilidades de los personajes, las características del jefe y las probabilidades asociadas a cada acción en el combate. Se consultaron diversas fuentes, incluyendo wikis especializadas en la saga Persona, para obtener información detallada sobre las mecánicas del juego, ademas de ver muchos videos donde se enfrentaban a este jefe en particular para entender mejor su comportamiento y las estrategias utilizadas por los jugadores.
Una vez que se tuvo una comprensión sólida del combate, los personajes, los ítems y las probabilidades involucradas, se procedió a implementar el entorno de simulación del combate en Python. Este entorno debía ser capaz de reproducir fielmente las reglas del juego, incluyendo la gestión de turnos, ataques mágicos, uso de ítems, la aplicación de probabilidades en los resultados de las acciones (como golpes críticos, esquives,etc) aplicar estados alterados y sus probabilidades (congelar, miedo, etc) , la gestión de la salud y el SP de los personajes, el comportamiento del jefe durante el combate, la gestión de aumentos y reducciones de estadísticas (buff y debuff) y cualquier otra mecánica relevante para el combate.

Con el entorno de simulación listo, se implementaron los cuatro algoritmos y la capacidad de ejecutar múltiples simulaciones de combate para evaluar el desempeño de cada algoritmo. Se decidió ejecutar pruebas de 1000,500 y 100 simulaciones por cada algoritmo para obtener una muestra representativa de su desempeño, considerando el tiempo de ejecución y la variabilidad inherente a las probabilidades del combate.

### Resultados Obtenidos

Se usaron dos funciones de fitness diferentes para los algoritmos en distinta cantidad de simulaciones. A continuación se presentan los resultados obtenidos en 100, 500 y 1000 simulaciones.

#### Daños Realizados

- 100 simulaciones:
Fitness 1:
<image src="/images/fitness_1/100_iteraciones/damage_done_comparison.png" alt="Daño realizado fitness 1 en 100 iteraciones"/>
Fitness 2:
<image src="/images/fitness_2/100_iteraciones/damage_done_comparison.png" alt="Daño realizado fitness 2 en 100 iteraciones"/>

- 500 simulaciones:

<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/500_iteraciones/damage_done_comparison.png" ></td><td> Fitness  2<img  width="400" src="/images/fitness_2/500_iteraciones/damage_done_comparison.png"></td></tr></table>

- 1000 simulaciones:

<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/1000_iteraciones/damage_done_comparison.png" ></td><td> Fitness  2<img  width="400" src="/images/fitness_2/1000_iteraciones/damage_done_comparison.png"></td></tr></table>


#### Daños recibidos por algoritmo:

- 100 simulaciones:

<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/100_iteraciones/damage_taken_comparison.png" ></td><td> Fitness  2<img  width="400" src="/images/fitness_2/100_iteraciones/damage_taken_comparison.png"></td></tr></table>

- 500 simulaciones:
Fitness 1: 
<img src="/images/fitness_1/500_iteraciones/damage_taken_comparison.png" alt="Daño recibido fitness 1 en 500 iteraciones"/>
Fitness 2:
<img src="/images/fitness_2/500_iteraciones/damage_taken_comparison.png" alt="Daño recibido fitness 2 en 500 iteraciones"/>

- 1000 simulaciones:
Fitness 1:
<img src="/images/fitness_1/1000_iteraciones/damage_taken_comparison.png" alt="Daño recibido fitness 1 en 1000 iteraciones"/>
Fitness 2:
<img src="/images/fitness_2/1000_iteraciones/damage_taken_comparison.png" alt="Daño recibido fitness 2 en 1000 iteraciones"/>

#### Muertes por algoritmo:

- 100 simulaciones:
Fitness 1:
<img src="/images/fitness_1/100_iteraciones/deaths_comparison.png" alt="Muertes fitness 1 en 100 iteraciones"/>
Fitness 2:
<img src="/images/fitness_2/100_iteraciones/deaths_comparison.png" alt="Muertes fitness 2 en 100 iteraciones"/>

- 500 simulaciones:

<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/500_iteraciones/deaths_comparison.png" ></td><td> Fitness  2<img  width="400" src="/images/fitness_2/500_iteraciones/deaths_comparison.png"></td></tr></table>

- 1000 simulaciones:
Fitness 1:
<img src="/images/fitness_1/1000_iteraciones/deaths_comparison.png" alt="Muertes fitness 1 en 1000 iteraciones"/>
Fitness 2:
<img src="/images/fitness_2/1000_iteraciones/deaths_comparison.png" alt="Muertes fitness 2 en 1000 iteraciones"/>

#### Turnos en partidas ganadas por algoritmo:

- 100 simulaciones:
Fitness 1:
<img src="/images/fitness_1/100_iteraciones/turns_comparison.png" alt="Turnos fitness 1 en 100 iteraciones"/>
Fitness 2:
<img src="/images/fitness_2/100_iteraciones/turns_comparison.png" alt="Turnos fitness 2 en 100 iteraciones"/>

- 500 simulaciones:
<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/500_iteraciones/turns_comparison.png" ></td><td> Fitness  2<img  width="400" src="/images/fitness_2/500_iteraciones/turns_comparison.png"></td></tr></table>

- 1000 simulaciones:
<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/1000_iteraciones/turns_comparison.png" ></td><td> Fitness  2<img  width="400" src="/images/fitness_2/1000_iteraciones/turns_comparison.png"></td></tr></table>

#### Winrate

- 100 simulaciones:
<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/100_iteraciones/win_rate_comparison.png" ></td><td> Fitness 2<img  width="400" src="/images/fitness_2/100_iteraciones/win_rate_comparison.png"></td></tr></table>
- 500 simulaciones:
<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/500_iteraciones/win_rate_comparison.png" ></td><td> Fitness 2<img  width="400" src="/images/fitness_2/500_iteraciones/win_rate_comparison.png"></td></tr></table>
- 1000 simulaciones:
<table ><tr><td> Fitness 1<img  width="400" src="/images/fitness_1/1000_iteraciones/win_rate_comparison.png" ></td><td> Fitness 2<img  width="400" src="/images/fitness_2/1000_iteraciones/win_rate_comparison.png"></td></tr></table>

### Tabla comparativa de resultados obtenidos en 1000 simulaciones - función de fitness 1

Estas tablas son de extrema importancia ya que resumen los resultados obtenidos por cada algoritmo en las 1000 simulaciones realizadas, permitiendo una comparación directa de su desempeño en términos de las métricas evaluadas pudiendo sintetzar y ver de manera mas clara que los gráficos las diferencias entre cada uno

| Algoritmo | Tasa de Victoria (%) | Turnos Promedio (±DE) | Daño Infligido Promedio (±DE) | Daño Recibido Promedio (±DE) | Muertes Promedio (±DE) | Tiempo por Simulación (s) |
|-----------|----------------------|-----------------------|-------------------------------|-------------------------------|------------------------|---------------------------|
| Random | 24.20 | 7.88 ± 3.92 | 245.80 ± 193.92 | 1690.28 ± 995.32 | 0.95 ± 1.08 | 0.045139 |
| Model Genetic | 28.30 | 7.80 ± 3.47 | 387.11 ± 206.92 | 1533.93 ± 948.02 | 0.87 ± 1.05 | 54.833753 |
| Modified Genetic | 38.80 | 8.95 ± 3.61 | 339.12 ± 172.42 | 1752.44 ± 1061.90 | 0.90 ± 1.09 | 72.177844 |
| NSGA-II | 34.80 | 8.26 ± 3.60 | 400.87 ± 213.41 | 1606.19 ± 952.13 | 0.82 ± 1.03 | 64.35 |

### Tabla comparativa de resultados obtenidos en 1000 simulaciones - función de fitness 2

| Algoritmo | Tasa de Victoria (%) | Turnos Promedio (±DE) | Daño Infligido Promedio (±DE) | Daño Recibido Promedio (±DE) | Muertes Promedio (±DE) | Tiempo por Simulación (s) |
|-----------|----------------------|-----------------------|-------------------------------|-------------------------------|------------------------|---------------------------|
| Random | 24.20 | 7.88 ± 3.92 | 245.80 ± 193.92 | 1690.28 ± 995.32 | 0.95 ± 1.08 | 0.045139 |
| Model Genetic | 29.00 | 8.04 ± 3.61 | 383.03 ± 214.05 | 1601.11 ± 1012.53 | 0.83 ± 1.04 | 41.783550 |
| Modified Genetic | 39.70 | 8.98 ± 3.72 | 317.51 ± 175.47 | 1769.01 ± 1064.27 | 0.85 ± 1.06 | 120.794004 |
| NSGA-II | 34.80 | 8.26 ± 3.60 | 400.87 ± 213.41 | 1606.19 ± 952.13 | 0.82 ± 1.03 | 64.35 |

### Frente de pareto obtenido con NSGA-II

Por ultimo se presenta el frente de pareto obtenido en una simulación al azar con NSGA-II, donde se puede observar la relación entre las muertes y el daño infligido al jefe, en azul se muestran las soluciones no dominadas y en gris las soluciones consideradas pero dominadas.

<img src="/images/Figure_1.png" alt="Frente de pareto obtenido con NSGA-II"/>

## Análisis y Discusión de Resultados

A continuación se presenta un análisis de los resultados obtenidos, desglosado por cada una de las métricas evaluadas:

#### 1. Tasa de Victoria (Winrate)

- El algoritmo genético modificado con ambas funciones de fitness mostró la mejor tasa de victoria, alcanzando un 39.70%. con la función de fitness 2 y un 38.80% con la función de fitness 1. Esto indica que las modificaciones introducidas en el algoritmo genético, como el cruce de dos puntos,corte temprano y la función de sentido común, fueron efectivas para mejorar la capacidad del algoritmo para encontrar estrategias ganadoras.

- NSGA-II también mostró un buen desempeño en segundo lugar con una tasa de victoria del 34.80%, lo cual es para destacar ya que no se diseñó específicamente para adaptarse a la pelea, con un mayor tiempo dedicadoa él, como hicimos en el algoritmo genético modificado, podría haber alcanzado tasas de victoria aún más altas. Por otro lado,el alto winrate se puede deber a que la metrica de muertes es la mas importante para ganar la pelea, y NSGA-II se enfoca en minimizar las muertes y maximizar el daño infligido.

- El algoritmo genético modelo tuvo una tasa de victoria del 29.00% con la función de fitness 2 y un 28.30% con la función de fitness 1, si bien es mejor que el algoritmo aleatorio, no logró superar a la versión modificada.

- El algoritmo aleatorio tuvo la tasa de victoria más baja con un 24.20%, lo cual es esperado dado que no utiliza ninguna estrategia para optimizar las acciones durante el combate, sin enbargo, su desempeño no fue tan bajo como se podría esperar, lo que sugiere que incluso estrategias simples pueden tener cierto éxito en este combate debido a las muchas probabilidades involucradas y a las ayudas de los demás personajes.

#### 2. Turnos Promedio en Soluciones Ganadoras

- Si bien todos los algoritmos mostraron un número similar de turnos promedio en las partidas ganadas (alrededor de 7-8 turnos), los algortimos random y el genético modelo tendieron a ganar en menos turnos en promedio en comparación con el genético modificado y NSGA-II. Esto podría indicar que las estrategias generadas por los algoritmos más avanzados tienden a ser más conservadoras, priorizando la supervivencia, lo que puede resultar en un mayor número de turnos para asegurar la victoria, otra posible explicación es que al tener un mayor winrate, tienen más combates ganados en situaciones difíciles que requieren más turnos, lo que nos deja como conclusión que ganar en menos turnos no es necesariamente sinónimo de una mejor estrategia.

#### 3. Daño Infligido

- NSGA-II fue el algoritmo que logró infligir el mayor daño promedio al jefe lo cual es coherente con su objetivo de maximizar el daño infligido. El algoritmo genético modelo también mostró un buen desempeño en esta métrica, mientras que el algoritmo genético modificado tuvo un daño infligido promedio ligeramente menor, lo que podría estar relacionado con el enfoque de usar la función de sentido común para optimizar las primeras acciones, lo que podría llevar a estrategias más equilibradas pero con un daño total ligeramente menor. Por último, el algoritmo aleatorio tuvo el daño infligido promedio más bajo, lo cual es esperado dado que no optimiza las acciones de ninguna manera.

#### 4. Daño Recibido

- NSGA-II logró minimizar el daño recibido por los personajes debido a su enfoque en minimizar las muertes, el algoritmo genético modelo también mostró un buen desempeño en esta métrica. El algoritmo genético modificado tuvo un daño recibido promedio ligeramente mayor, lo que podría estar relacionado con su alto winrate, ya que al durar más turnos en promedio, los personajes tienen más oportunidades de recibir daño, el algoritmo aleatorio tampoco logró unos resultados destacados en esta métrica.

#### 5. Muertes Promedio

- NSGA-II fue el algoritmo que logró minimizar el número de muertes promedio, lo cual es coherente con su objetivo de minimizar las muertes. Los algoritmos genéticos (modelo y modificado) también mostraron un buen desempeño en esta métrica, con un número de muertes promedio similar. El algoritmo aleatorio tuvo el mayor número de muertes promedio, lo cual es esperado y se corresponde con su baja tasa de victoria.

#### 6. Tiempo por Simulación

- El algoritmo aleatorio fue el más rápido por una gran diferencia, lo cual es esperado dado que no realiza ninguna optimización. Entre los algoritmos genéticos, el modelo fue el más rápido, pero el algoritmo genético modificado fue el más lento debido a las modificaciones introducidas, ya que al cortar las secuencias se debe evaluar la función de fitness en las demás soluciones que fueron cortadas, la solución de torneo también implica evaluar múltiples combates por cada una de las mejores soluciones, lo que incrementa el tiempo de cómputo. NSGA-II tuvo un tiempo de ejecución intermedio, lo cual es razonable dado su enfoque multiobjetivo, la población más grande y el mayor número de generaciones.

En resumen, el análisis por métricas muestra que las modificaciones introducidas en el algoritmo genético, juento con la función de fitness 2 y el uso de NSGA-II permiten obtener estrategias más efectivas y equilibradas, superando ampliamente al enfoque aleatorio y mejorando sobre el modelo genético tradicional en la mayoría de los aspectos relevantes para el combate, destacar que no nos detuvimos a analizar tanto la información de la desviación estándar, ya que no es tan relevante para el análisis en este caso ya que dado el alto componente de azar en el combate, es esperable que haya una alta variabilidad en los resultados por ejemplo si el jefe ataca a el protagonista en el primer turno y le aplica "miedo", la pelea se vuelve mucho más difícil y es probable que el protagonista muera, lo que afecta todas las métricas, pero no necesariamente refleja una mala estrategia, sino simplemente un mal resultado debido al azar.


## Conclusiones Finales

En este trabajo se compararon diferentes algoritmos genéticos y un enfoque multiobjetivo (NSGA-II) para optimizar estrategias de combate en un entorno complejo y estocástico como Persona 3. Se observó que las modificaciones introducidas en el algoritmo genético tradicional, como el cruce de dos puntos, el corte temprano de secuencias y la función de sentido común, permitieron mejorar significativamente la tasa de victoria y la robustez de las soluciones a costa de un aumento significativo en el tiempo de ejecución. NSGA-II demostró ser eficaz para equilibrar múltiples objetivos, logrando minimizar muertes y maximizar el daño infligido, lo que resultó en estrategias más seguras y eficientes, con un tiempo de ejecución razonable.

Como posibles mejoras, para este tipo de combate sería muy interesante aplicar técnicas de aprendizaje por refuerzo para adaptar dinámicamente las estrategias durante el combate, también se podría adaptar mejor el algoritmo NSGA-II poniendole un mayor ezfuerzo y tiempo de desarrollo para adaptarlo mejor al problema en cuestión, ya que en este trabajo se lo utilizó de manera más general, nuestra solución propuesta siempre fue la de adaptar el algoritmo genético modificado al problema en cuestión, pero NSGA-II tiene un gran potencial que no fue explotado completamente en este trabajo. Por otro lado, se podría explorar la utilización de otra función de fitness ya que al pasar de la función de fitness 1 a la 2, se observaron mejoras en el desempeño de los algoritmos genéticos, lo que sugiere que una función de fitness mejor diseñada puede tener un impacto significativo en la calidad de las soluciones encontradas. Otra posible mejora sería optimizar el tiempo de ejecución tratando de paralelizar las simulaciones de combate, o usar técnicas de algoritmos genéticos paralelos.

Para finalizar, este trabajo demuestra el potencial de los algoritmos evolutivos y multiobjetivo para resolver problemas complejos en entornos con alta incertidumbre, ya que en un primer momento se pensó que el alto componente de azar en el combate haría que los algoritmos no pudieran encontrar buenas soluciones y se pensó que un enfoque de aprendizaje por refuerzo sería más adecuado, pero los resultados obtenidos muestran que con un buen diseño y ajustes, los algoritmos genéticos y NSGA-II pueden ser herramientas poderosas para optimizar estrategias en este tipo de escenarios.

## Bibliografía y referencias


1. S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 3rd ed. Upper Saddle River, NJ, USA: Prentice Hall, 2010.

2. Fandom,Megami Tensei Wiki - Sleeping Table. https://megamitensei.fandom.com/wiki/Sleeping_Table

3. Fandom,Megami Tensei Wiki - Persona 3. https://megamitensei.fandom.com/wiki/Persona_3

4. J. Blank and K. Deb, "Pymoo: Multi-Objective Optimization in Python," 2020. https://pymoo.org/algorithms/moo/nsga2.html

5. Nathan Ambuehl Thesis, "Investigating Genetic Algorithm Optimization Techniques in Video Games", East Tennessee State University, https://dc.etsu.edu/cgi/viewcontent.cgi?article=1788&context=honors

6. GeeksforGeeks, "Genetic Algorithms", https://www.geeksforgeeks.org/dsa/genetic-algorithms/

7. GeeksforGeeks, "Non-Dominated Sorting Genetic Algorithm 2 (NSGA-II)",https://www.geeksforgeeks.org/deep-learning/non-dominated-sorting-genetic-algorithm-2-nsga-ii/
