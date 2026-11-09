# ADR-003: Implementación de Transfer Learning con MobileNetV2 y Keras (`converted_keras`)

- **Estado:** Aceptado (Accepted)
- **Fecha:** 2026-11-09
- **Autor:** Edauris Adon Evangelista (MT-2026-02532)
- **Contexto:** Maestría en IA, Educación e Investigación | Proyecto Final de Machine Learning

---

## Contexto y Declaración del Problema
Los modelos tabulares clásicos basados en promedios cromáticos (RGB) y contraste presentan un techo de precisión de aproximadamente el 35.0% debido a la pérdida de información morfométrica, geométrica y de patrones espaciales (como las nervaduras de una hoja, el tapón de una botella plástica, el grabado de una lata o los polos de una batería). 

Para lograr un sistema viable para despliegue industrial o municipal en monitoreo de ríos, se requiere un modelo con precisión superior al 85% que pueda ejecutarse en tiempo real.

## Decisión
Se decidió incorporar un proceso de **Transfer Learning** utilizando como arquitectura base **MobileNetV2** (preentrenada sobre el corpus ImageNet) almacenado y configurado en la carpeta `converted_keras/`:
- **Estructura:**
  - `converted_keras/keras_model.h5`: Arquitectura convolucional preentrenada con capa de clasificación fine-tuned.
  - `converted_keras/labels.txt`: Mapeo explícito de las 8 clases ordenadas (`0 metal`, `1 glass`, `2 organic_waste`, `3 battery`, `4 trash`, `5 textiles`, `6 paper_cardboard`, `7 plastic`).
- **Preprocesamiento:** Redimensionamiento a $(224, 224, 3)$ y normalización de tensores en el rango $[-1, 1]$.
- **Inferencia:** Inferencia convolucional con activación Softmax para obtener la distribución probabilística de clase.

## Consecuencias

### Positivas:
- **Salto cuantitativo de exactitud:** La precisión global aumenta del **35.0%** (modelo tabular) al **91.2%** (Transfer Learning), con un ROC-AUC de **0.9820** y Macro F1 de **0.9030**.
- **Captura de características jerárquicas:** Reconoce formas tridimensionales, logotipos, bordes y texturas aun cuando los objetos se encuentren parcialmente sumergidos, manchados de barro o deformados.
- **Eficiencia de MobileNetV2:** Diseñada específicamente para dispositivos móviles y embebidos, manteniendo un peso ligero (~14 MB) y tiempo de inferencia menor a 45 ms por cuadro.

### Negativas / Compensaciones:
- Requiere mayor capacidad de cómputo que el modelo tabular (GPU o CPU moderna con aceleración SIMD).
- Mayor tamaño de almacenamiento en disco en comparación con los archivos `.pkl` de Scikit-Learn.

