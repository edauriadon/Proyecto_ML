# ADR-004: Arquitectura Desacoplada de Despliegue (Landing Page en GitHub Pages + App en Streamlit Cloud)

- **Estado:** Aceptado (Accepted)
- **Fecha:** 2026-11-09
- **Autor:** Edauris Adon Evangelista (MT-2026-02532)
- **Contexto:** Maestría en IA, Educación e Investigación | Proyecto Final de Machine Learning

---

## Contexto y Declaración del Problema
El proyecto requiere ser presentado tanto a evaluadores académicos y comunidades ambientales interesadas en el contexto investigativo, como a técnicos y desarrolladores que necesitan interactuar con los modelos predictivos en tiempo real.

Alojar todo en un único servidor monolítico o depender de una sola plataforma compromete la velocidad de carga institucional y la disponibilidad continua del proyecto.

## Decisión
Se decidió implementar una **arquitectura desacoplada en capas**:
1. **Landing Page en GitHub Pages (`index.html` en el directorio raíz):**
   - Servida mediante CDN global estático de GitHub Pages.
   - Presentación institucional con diseño responsivo, infografías del ciclo CRISP-ML, métricas clave, simulador HTML5 y video interactivo embebido.
   - Enlace directo al repositorio: `https://github.com/edauriadon/Proyecto-ML.git`
   - Enlace directo a la app en Streamlit: `https://Proyecto_ML.streamlit.app`
2. **Aplicación Web Interactiva en Streamlit Cloud (`app.py`, `requirements.txt`):**
   - Aloja el motor de inferencia de Machine Learning con dos pestañas interactivas comparativas (Pestaña 1: Modelo Tabular / Notebook; Pestaña 2: Transfer Learning con `converted_keras`).
   - Permite carga de archivos (imágenes locales) y captura de cámara web para predicciones en vivo.

## Consecuencias

### Positivas:
- **Disponibilidad 24/7:** La landing page en GitHub Pages nunca experimenta tiempos de espera por reposo del servidor (*cold starts*).
- **Separación de responsabilidades:** La landing page educa, comunica y orienta; la aplicación de Streamlit computa y predice.
- **Experiencia de usuario optimizada:** Los evaluadores pueden revisar la documentación técnica y el video interactivo de inmediato sin necesidad de esperar la inicialización del entorno Python.

### Negativas / Compensaciones:
- Requiere mantener dos interfaces sincronizadas en cuanto a versiones de enlaces y descripciones técnicas.

