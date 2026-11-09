# ADR-001: Extracción ETL de Características Visuales RGB y Textura vs. Tensores Crudos

- **Estado:** Aceptado (Accepted)
- **Fecha:** 2026-11-09
- **Autor:** Edauris Adon Evangelista (MT-2026-02532)
- **Contexto:** Maestría en IA, Educación e Investigación | Proyecto Final de Machine Learning

---

## Contexto y Declaración del Problema
En el problema de clasificación de residuos sólidos en ríos y cañadas a partir de imágenes fotográficas, los algoritmos tradicionales de Machine Learning supervisado (como Regresión Logística, Random Forest y Support Vector Machines) no pueden procesar directamente matrices tensoriales de píxeles sin aplanar, lo cual generaría un espacio de características excesivamente disperso y susceptible a la maldición de la dimensionalidad (e.g., $224 \times 224 \times 3 = 150,528$ variables por muestra).

Se requiere definir un mecanismo de extracción de características (*Feature Extraction*) que transforme los datos no estructurados en un conjunto tabular compacto, interpretable y representativo.

## Decisión
Se decidió implementar un pipeline de **Extracción, Transformación y Carga (ETL Visual)** utilizando las bibliotecas `Pillow` y `NumPy`, extrayendo 9 características numéricas continuas:
1. Promedios de intensidad por canal: `mean_r`, `mean_g`, `mean_b`.
2. Dispersión cromática: `std_r`, `std_g`, `std_b`.
3. Luminancia global: `brightness` ($\frac{R+G+B}{3}$).
4. Complejidad textural y rugosidad: `contrast` (desviación estándar en escala de grises).
5. Proporción dimensional: `aspect_ratio` ($\frac{\text{ancho}}{\text{alto}}$).

## Consecuencias

### Positivas:
- **Reducción masiva de dimensionalidad:** De 150,528 valores a exactamente 9 variables continuas por muestra.
- **Interpretabilidad analítica:** Permite aplicar herramientas de perfilado automático (`ydata-profiling`) y explicar la importancia de variables en modelos de ensamble.
- **Bajo costo computacional:** Permite entrenar clasificadores en segundos y ejecutar inferencias ultrarrápidas (< 5 ms) en procesadores convencionales o microcontroladores de bajo consumo.

### Negativas / Compensaciones (Trade-offs):
- **Pérdida de relaciones espaciales y contextuales:** El promedio de color no preserva la geometría de una lata cilíndrica, las aristas de una botella o el texto impreso en una caja de cartón.
- **Techo de rendimiento:** La precisión global de los modelos basados exclusivamente en estas 9 características alcanza un máximo aproximado de 35.0%, haciendo indispensable complementar con técnicas de Transfer Learning para aplicaciones de alta exactitud en campo.

