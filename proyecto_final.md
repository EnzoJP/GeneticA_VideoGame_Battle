
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
- [Análisis y Discusión de Resultados](#análisis-y-discusión-de-resultados)
- [Conclusiones Finales](#conclusiones-finales)
- [Bibliografía y referencias](#bibliografía-y-referencias)


## Introducción

Persona 3 es un videojuego de rol lanzado en 2006 para la consola PlayStation 2. En este juego, el jugador controla a un grupo de estudiantes que se enfrentan contra criaturas conocidas como sombras en combates por turnos. En estos combates, el jugador debe elegir las acciones de sus personajes, como atacar, usar habilidades especiales, defenderse, usar ítems diversos, etc. Además, el jugador debe tener en cuenta las debilidades y resistencias de los enemigos, ya que algunos enemigos son débiles a ciertos tipos de ataques y resistentes a otros.

El enemigo que se eligió para realizar el proyecto es **Sleeping Table**, un enemigo que aparece en el piso 135 de la torre de Tartarus, la cual es una mazmorra que el jugador debe explorar. Este es un enemigo que tiene una alta resistencia a la mayoría de los ataques y no tiene debilidades, por lo que es considerado un *jefe* muy difícil.

Para combatir a este enemigo, se implementaron cuatro algoritmos diferentes:
1. **Algoritmo Aleatorio**: Este algoritmo selecciona una acción al azar entre las disponibles hasta que el enemigo es derrotado o el jugador es derrotado.
2. **Algoritmo Genético de modelo**: Este algoritmo genético es lo mas parecido a un algoritmo genético tradicional, descripto en el libro de *Inteligencia Artificial: Un Enfoque Moderno* de Russell y Norvig con un pequeño agregado de elitismo.
3. **Algoritmo Genético modificado**: Este algoritmo genético es una versión modificada del algoritmo genético de base, en el cual se implementaron algunas mejoras para aumentar la eficacia del algoritmo y adaptarlo mejor al problema en cuestión.
4. **Algoritmo NSGA-II**: Este algoritmo es una implementación del algoritmo NSGA-II, el cual es un algoritmo genético multiobjetivo. En este caso, se consideraron dos objetivos: minimizar las muertes de los personajes y maximizar el daño infligido al enemigo.

Finalmente, el presente informe se encuentra dividido en diferentes secciones: en la sección de [Descripción del juego](#descripción-del-juego), se detallan las mecánicas del juego, los personajes y las características del enemigo seleccionado. En la sección de [Marco Teórico](#marco-teórico), se describen los algoritmos implementados y sus fundamentos teóricos. En la sección de [Diseño Experimental](#diseño-experimental), se explica cómo se llevaron a cabo los experimentos y qué métricas se utilizaron para evaluar el desempeño de los algoritmos. En la sección de [Análisis y Discusión de Resultados](#análisis-y-discusión-de-resultados), se presentan los resultados obtenidos y se discuten las diferencias entre los algoritmos. Finalmente, en la sección de [Conclusiones Finales](#conclusiones-finales), se resumen los hallazgos más importantes y se sugieren posibles mejoras para futuros trabajos.

## Descripción del juego

### Mecánicas del juego

----Modificar----  --hablar de mejor de las probabilidades, etc todo lo de mecanicas del juego--

Los combates en la saga "Persona" son por turnos, es decir, el jugador y los enemigos se turnan para realizar determinadas acciones. Las acciones, tanto del enemigo como las propias, muchas veces se ven afectadas por distintas probabilidades, por ejemplo, el enemigo puede esquivar el ataque con una *probabilidad p*,probabilidad de daño crítico, etc.

En el caso de Persona 3, el jugador controla a un solo personaje y los demás son controlados por el propio juego, aunque uno puede darle directrices generales, llamadas tácticas, de cómo encarar el combate. Este es un grupo de 4 personajes, cada uno con habilidades y características únicas, esto mediante el uso de "personas", seres invocados por el personaje que poseen habilidades especiales y estadísticas, además de debilidades o resistencias a ciertos tipos de ataques (Por ejemplo, un persona puede ser débil al elemento fuego y resistir el elemento hielo).

En el combate, el jugador debe elegir las acciones de sus personajes, las cuales son: atacar, habilidades (dependiendo el "persona" equipado) y usar ítems .

En este juego, hay 9 tipos de ataques: Fuego, Hielo, Electricidad, Viento, Luz, Oscuridad, Físico Perforante, Físico Golpe y Físico Cortante. Cada uno de estos ataques tiene una probabilidad de causar un estado alterado en el enemigo (por ejemplo, congelar, quemar, aturdir, etc). Además, cada ataque tiene un multiplicador de daño dependiendo de la debilidad o resistencia del enemigo. Por ejemplo, si un enemigo es débil al fuego, un ataque de fuego le hará más daño que uno normal.

### Personajes

- Listar cada uno de los personajes, sus habilidades,características y tacticas.

### Enemigo: Sleeping Table

- idem de arriba

### Ítems disponibles

Hay varios ítems disponibles en el juego, pero para este combate se utilizaron los siguientes:

- **Un Soma**: completar

- **Dos Precious Egg**: completar

- **Un Magic Mirror**: completar

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

- **Tiempo de Ejecución:** Es el tiempo total que tarda cada algoritmo en completar todas las simulaciones requeridas. Se mide utilizando temporizadores en el código durante la ejecución de cada algoritmo. Es relevante porque permite comparar la eficiencia computacional y la viabilidad práctica de cada enfoque, especialmente en contextos donde el tiempo de cómputo es limitado.

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

## Análisis y Discusión de Resultados

- Presentar los resultados obtenidos y discutir las diferencias entre los algoritmos y el porque de cada resultado
usar todos los plots aca y tablas necesarias

## Conclusiones Finales

- Resumir los hallazgos más importantes y sugerir posibles mejoras para futuros trabajos

## Bibliografía y referencias


1. S. Russell and P. Norvig, *Artificial Intelligence: A Modern Approach*, 3rd ed. Upper Saddle River, NJ, USA: Prentice Hall, 2010.

2. Fandom,Megami Tensei Wiki - Sleeping Table. https://megamitensei.fandom.com/wiki/Sleeping_Table

3. Fandom,Megami Tensei Wiki - Persona 3. https://megamitensei.fandom.com/wiki/Persona_3

4. J. Blank and K. Deb, "Pymoo: Multi-Objective Optimization in Python," 2020. https://pymoo.org/algorithms/moo/nsga2.html

5. Nathan Ambuehl Thesis, "Investigating Genetic Algorithm Optimization Techniques in Video Games", East Tennessee State University, https://dc.etsu.edu/cgi/viewcontent.cgi?article=1788&context=honors

6. GeeksforGeeks, "Genetic Algorithms", https://www.geeksforgeeks.org/dsa/genetic-algorithms/

7. GeeksforGeeks, "Non-Dominated Sorting Genetic Algorithm 2 (NSGA-II)",https://www.geeksforgeeks.org/deep-learning/non-dominated-sorting-genetic-algorithm-2-nsga-ii/
