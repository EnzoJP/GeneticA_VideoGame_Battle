# Algoritmos Genéticos para vencer jefe del videojuego Persona 3

Proyecto realizado para la materia de Inteligencia Artificial 1

Integrantes: Martinez Paula y Enzo Palau

-------

El objetivo de este proyecto es implementar algoritmos genéticos que permita encontrar la mejor estrategia para vencer al jefe del videojuego Persona 3 "Sleeping Table", utilizando las habilidades y características de los personajes disponibles.

Este combate será simulado por consola y dará como resultado la secuencia de acciones que deben realizar los personajes para derrotar al jefe según diferentes criterios, si el usuario lo desea el combate puede ser jugado manualmente.

Los algoritmos genéticos implementados incluyen:
- Algoritmo aleatorio
- Algoritmo genético básico
- Algoritmo genético modificado y adaptado al problema
- Algoritmo NSGA-II (utilizando la librería pymoo)

----

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/usuario/proyecto-persona3-genetico.git
   cd proyecto-persona3-genetico
   ```

2. Instalar la librería `pymoo` (solo necesario si se utiliza para el algoritmo nsga-ii):

   ```bash
   pip install pymoo
   ```

## Ejecución

Para correr la simulación del algoritmo genético y ver los resultados en consola:

```bash
python main.py
```

Durante la ejecución, el programa mostrará en pantalla:

- El usuario puede elegir entre jugar el combate manualmente (eligiendo acciones por turno) o simular el combate utilizando distintos algoritmos (aleatorio, genético, genético modificado, NSGA-II).
- En modo simulación, se ejecutan múltiples combates automáticos y se muestran estadísticas como cantidad de victorias, derrotas, promedio de turnos y porcentaje de victorias para cada algoritmo.
- No se imprime la mejor secuencia de acciones ni el progreso de generaciones; el enfoque está en comparar el desempeño general de cada algoritmo.
- Al finalizar cada simulación, se muestran los resultados agregados (winrate, promedio de turnos, tiempo de ejecución).

## Estructura del Proyecto

- `main.py`: Archivo principal para ejecutar el juego y las simulaciones.
- `combat/party.py`, `combat/enemy.py`: Definición de personajes y jefe, junto con sus habilidades.
- `combat/combat.py`: Lógica de simulación del combate y menú de usuario.
- `genetics/`: Implementaciones de los distintos algoritmos (random, model_genetic, modified_genetic, NGSA_ii).
- `combat/metrics_and_plots.py`: Cálculo de métricas y generación de gráficos.
- `proyecto_final.md`: Documentación detallada del proyecto, explicación de los algoritmos, decisiones de diseño y análisis de resultados.

## Documentación

La documentación completa del proyecto, incluyendo la explicación de los algoritmos, parámetros utilizados, análisis de resultados y posibles mejoras, se encuentra en el archivo [`proyecto_final.md`](proyecto_final.md).
