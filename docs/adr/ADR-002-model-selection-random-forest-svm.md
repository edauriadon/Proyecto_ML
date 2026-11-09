# ADR-002: Selección y Comparación de Modelos Supervisados Tabulares (Random Forest, SVM, Regresión Logística)

- **Estado:** Aceptado (Accepted)
- **Fecha:** 2026-11-09
- **Autor:** Edauris Adon Evangelista (MT-2026-02532)
- **Contexto:** Maestría en IA, Educación e Investigación | Proyecto Final de Machine Learning

---

## Contexto y Declaración del Problema
Habiendo estructurado el dataset tabular derivado del ETL visual con 9 características continuas y 8 clases objetivo (`battery`, `glass`, `metal`, `organic_waste`, `paper_cardboard`, `plastic`, `textiles`, `trash`), es necesario seleccionar algoritmos de clasificación supervisada que sirvan como línea base (*baseline*) e identifiquen patrones no lineales de separación entre residuos.

## Decisión
Se decidió implementar un marco multimodelo comparativo con tres algoritmos representativos de Scikit-Learn:
1. **Regresión Logística Multiclase (One-vs-Rest):** Como línea base probabilística e interpretable.
2. **Random Forest Classifier (100 árboles de decisión):** Para evaluar ensambles no lineales y obtener importancias de características.
3. **Support Vector Machine (SVM con Kernel RBF):** Para explorar separabilidad geométrica en espacios transformados de alta dimensión.

Se seleccionaron como métricas principales de decisión el **Macro F1-Score** y el **ROC-AUC multiclase (OvR)** para no sesgar el análisis hacia ninguna categoría en particular.

## Consecuencias

### Positivas:
- **Evaluación rigurosa:** Permite comparar un modelo lineal simple frente a ensambles (*bagging*) y máquinas de vectores de soporte.
- **Rendimiento demostrado:**
  - Regresión Logística: Accuracy 28.75%, Macro F1 0.2612, ROC-AUC 0.7221.
  - Random Forest: Accuracy 32.92%, Macro F1 0.3232, ROC-AUC 0.7190.
  - SVM (Kernel RBF): Accuracy 35.00%, Macro F1 0.3263, ROC-AUC 0.7303.
- SVM demostró ser el mejor modelo tabular general (35.0% de precisión y 0.7303 ROC-AUC), destacando en clases de alta reflectancia y contraste.
- Random Forest proporcionó interpretabilidad directa mostrando que `brightness` (18.4%), `contrast` (16.2%) y `mean_b` (14.7%) son las variables más influyentes.

### Negativas / Compensaciones:
- SVM requiere escalamiento estricto (`StandardScaler`), lo cual añade un paso indispensable en el pipeline de inferencia.
- El rendimiento general (~35%) demuestra que para ambientes fluviales complejos con sombras, agua y fango, los clasificadores sobre variables globales de color requieren ser complementados con redes neuronales convolucionales.

