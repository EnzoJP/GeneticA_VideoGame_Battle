
# Comparación de algoritmos para combatir un jefe del videojuego, basado en turnos, Persona 3

### Integrantes: Martínez Paula Y Enzo Palau 

---

## Índice

- [Introducción](#introducción)
- [Descripción del juego](#descripción-del-juego)
- [Marco Teórico](#marco-teórico)
- [Diseño Experimental](#diseño-experimental)
- [Análisis y Discusión de Resultados](#análisis-y-discusión-de-resultados)
- [Conclusiones Finales](#conclusiones-finales)
- [Bibliografía y referencias](#bibliografía-y-referencias)


## Introducción

Persona 3 es un videojuego de rol lanzado en 2006 para la consola PlayStation 2. En este juego, el jugador controla a un grupo de estudiantes que se enfrentan contra criaturas conocidas como sombras en combates por turnos. En estos combates, el jugador debe elegir las acciones de sus personajes, como atacar, usar habilidades especiales, defenderse, usar items diversos, etc. Además, el jugador debe tener en cuenta las debilidades y resistencias de los enemigos, ya que algunos enemigos son débiles a ciertos tipos de ataques y resistentes a otros.

El enemigo que se eligió para realizar el proyecto es **Sleeping Table**, un enemigo que aparece en el piso 135 de la torre de Tartarus, la cual es una mazmorra que el jugador debe explorar. Este es un enemigo que tiene una alta resistencia a la mayoría de los ataques y no tiene debilidades, por lo que es considerado un *jefe* muy difícil.

Para combatir a este enemigo, se implementaron cuatro algoritmos diferentes:
1. **Algoritmo Aleatorio**: Este algoritmo selecciona una acción al azar entre las disponibles hasta que el enemigo es derrotado o el jugador es derrotado. 
2. **Algoritmo Genético de base**: Este algoritmo genético es lo mas parecido a un algoritmo genético tradicional, descripto en el libro de *Inteligencia Artificial: Un Enfoque Moderno* de Russell y Norvig con un pequeño agregado de elitismo. 
3. **Algoritmo Genético modificado**: Este algoritmo genético es una versión modificada del algoritmo genético de base, en el cual se implementaron algunas mejoras para aumentar la eficacia del algoritmo y adaparlo mejor al problema en cuestión.
4. **Algoritmo NSGA-II**: Este algoritmo es una implementación del algoritmo NSGA-II, el cual es un algoritmo genético multiobjetivo. En este caso, se consideraron dos objetivos: minimizar las muertes de los personajes y maximizar el daño infligido al enemigo.

Finalmente, el presente informe se encuentra dividido en diferentes secciones: en la sección de [Descripción del juego](#descripción-del-juego), se detallan las mecánicas del juego, los personajes y las características del enemigo seleccionado. En la sección de [Marco Teórico](#marco-teórico), se describen los algoritmos implementados y sus fundamentos teóricos. En la sección de [Diseño Experimental](#diseño-experimental), se explica cómo se llevaron a cabo los experimentos y qué métricas se utilizaron para evaluar el desempeño de los algoritmos. En la sección de [Análisis y Discusión de Resultados](#análisis-y-discusión-de-resultados), se presentan los resultados obtenidos y se discuten las diferencias entre los algoritmos. Finalmente, en la sección de [Conclusiones Finales](#conclusiones-finales), se resumen los hallazgos más importantes y se sugieren posibles mejoras para futuros trabajos.

## Descripción del juego

### Mecánicas del juego

Los combates en la saga "Persona" son por turnos, es decir, el jugador y los enemigos se turnan para realizar determinadas acciones. Las acciones, tanto del enemigo como las propias, muchas veces se ven afectadas por distintas probabilidades, por ejemplo, el enemigo puede esquivar el ataque con una *probabilidad p*.

En el caso de Persona 3, el jugador controla a un solo personaje y los demás son controlados por el propio juego, aunque uno puede darle directrices generales, llamadas tácticas, de cómo encarar el combate. Este es un grupo de 4 personajes, cada uno con habilidades y características únicas, esto mediante el uso de "personas", seres invocados por el personaje que poseen habilidades especiales y estadísticas, además de debilidades o resistencias a ciertos tipos de ataques (Por ejemplo, un persona puede ser débil al elemento fuego y resistir el elemento hielo). 

En el combate, el jugador debe elegir las acciones de sus personajes, las cuales son: atacar, habilidades (dependiendo el "persona" equipado) y usar items . 

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

Al generar una acción al azar, el algoritmo puede seleccionar acciones que no son legales en el contexto del juego, como usar un ítem que no está disponible o encadenar ataques que no son posibles debido a el número de sp disponible.
Para solucionar esto, se implementaron ciertas restricciones en la generación de acciones:
+ No se pueden usar ítems si no hay ítems disponibles, si el agoritmo selecciona un ítem en este caso, se selecciona otra acción al azar.
+ No se pueden encadenar ataques si no hay sp disponible, si el algoritmo selecciona un ataque en este caso, se usará un item reservado de "Precious Egg" para recuperar sp y luego se seguirá con la siguiente acción al azar.

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

### Algoritmo Genético de base

- contar los detalles de la implementación y el porque de cada cosa

### Algoritmo Genético modificado

- contar los detalles de la implementación y el porque de cada cosa

### Algoritmo NSGA-II

- contar los detalles de la implementación y teoría y el porque de cada cosa

## Diseño Experimental

### Metricas Utilizadas

- contar las métricas utilizadas para evaluar el desempeño de los algoritmos y como se midieron y porque son relevantes

### Configuración de los algoritmos

- Detallar los parámetros utilizados en cada algoritmo y el porque de cada uno

### Funciones de Fitness (Aptitud)

- Detallar las funciones de fitness utilizadas en cada algoritmo y el porque de cada una

### Descripción de los experimentos realizados

- Detallar como medimos las peleas, cuantas veces se corrió cada algoritmo, etc

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