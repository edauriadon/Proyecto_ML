# 🎬 Guión de Sustentación y Video de Presentación del Proyecto
## Sistema Inteligente para la Detección y Clasificación de Desechos Sólidos en Ríos

**Maestría en IA, Educación e Investigación | Curso: Machine Learning**  
**Universidad Federico Henríquez y Carvajal (UFHEC)**  
**Estudiante:** Edauris Adon Evangelista · **Matrícula:** MT-2026-02532  
**Formato:** Video de Presentación e Interactividad (Skill `latent-spaces/brag`)  
**Duración Total:** 5 Minutos (Elevator Pitch Académico)  

---

### ⏱️ Minuto 0:00 – 1:00 | Diagnóstico de la Problemática Fluvial
- **Locución (Español):**  
  *"¡Saludos cordiales a los docentes, evaluadores y compañeros! Mi nombre es Edauris Adon Evangelista, y hoy les presento el Proyecto Final del curso de Machine Learning en la Maestría en IA, Educación e Investigación: el **Sistema Inteligente para la Detección y Clasificación de Desechos Sólidos en Ríos, Arroyos y Cañadas**.*  
  *La acumulación descontrolada de residuos sólidos en nuestras fuentes hídricas urbanas representa una de las mayores emergencias ambientales de nuestra época. Plásticos de un solo uso, botellas de vidrio, latas metálicas, telas y baterías con metales pesados altamente tóxicos son arrastrados por las corrientes fluviales hacia las costas y océanos. Esto no solo envenena la biodiversidad acuática, sino que tapona compuertas pluviales y biobardas, causando inundaciones devastadoras durante crecidas fluviales.*  
  *Los censos manuales tradicionales son peligrosos, lentos y de cobertura limitada. Nuestra propuesta responde a una pregunta clave: ¿Cómo podemos transformar cámaras y visión artificial en una herramienta automática de alerta y clasificación para la gestión ambiental?"*
- **Recurso Visual:** Diapositiva 1 con tomas de ríos contaminados, estadísticas globales de plásticos flotantes y formulación de la pregunta de investigación.

---

### ⏱️ Minuto 1:00 – 2:00 | Solución Tecnológica y Metodología CRISP-ML(Q)
- **Locución (Español):**  
  *"Para responder a este desafío, adoptamos el estándar metodológico **CRISP-ML(Q)**, garantizando rigor analítico, reproducibilidad y gobernanza en cada fase.*  
  *El corazón de nuestra propuesta radica en un diseño comparativo de dos paradigmas de Machine Learning:*  
  *Primero: un pipeline liviano de **Extracción de Características (ETL Visual)** que convierte imágenes en 9 variables tabulares de color y textura, evaluando clasificadores supervisados como Random Forest y Support Vector Machines.*  
  *Segundo: un modelo de **Transfer Learning** basado en la red convolucional profunda **MobileNetV2** preentrenada en ImageNet, ajustada para discriminar 8 categorías de residuos sólidos fluviales.*  
  *Esta dualidad nos permite comparar directamente la computación liviana frente a la visión profunda tridimensional."*
- **Recurso Visual:** Diagrama interactivo de las 6 fases de CRISP-ML(Q) y comparación de arquitectura de modelos.

---

### ⏱️ Minuto 2:00 – 3:00 | Datos, Pipeline ETL y Análisis Exploratorio
- **Locución (Español):**  
  *"Utilizamos el dataset de Kaggle **Unified Waste Classification Dataset**, integrando 1,200 imágenes balanceadas en 8 categorías:*  
  *`battery`, `glass`, `metal`, `organic_waste`, `paper_cardboard`, `plastic`, `textiles` y `trash`.*  
  *Nuestro pipeline ETL extrae matemáticamente promedios y desviaciones de canales rojo, verde y azul, brillo y contraste textural. Validamos la calidad del dataset con **YData Profiling**, confirmando la ausencia de nulos y evitando cualquier fuga de datos mediante partición estratificada 80/20 y escalamiento con StandardScaler ajustado únicamente sobre el conjunto de entrenamiento.*  
  *Esto nos entrega un dataset estructurado, limpio y matemáticamente representativo."*
- **Recurso Visual:** Gráficos de barras de distribución de clases, mapa de correlación de variables y captura del reporte de YData Profiling.

---

### ⏱️ Minuto 3:00 – 4:00 | Resultados, Métricas y Salto de Calidad
- **Locución (Español):**  
  *"Los resultados experimentales revelan un hallazgo crucial:*  
  *En el enfoque tabular, la **Support Vector Machine (SVM)** lideró con un **35.0% de exactitud**, superando a Random Forest (32.9%) y Regresión Logística (28.8%), con un ROC-AUC de 0.7303. Sin embargo, las variables de color tienen un techo evidente: no distinguen fácilmente una lata de metal de una botella de vidrio mojada.*  
  *Es aquí donde el **Transfer Learning con MobileNetV2** demostró su poder transformador, alcanzando un **91.2% de exactitud global**, un **F1-Score Macro de 0.9030** y un **ROC-AUC multiclase de 0.9820**.*  
  *Un incremento neto de más de 56 puntos porcentuales al analizar bordes, formas y texturas espaciales."*
- **Recurso Visual:** Gráfico comparativo interactivo de barras de métricas (Tabular 35% vs Transfer Learning 91.2%) y matriz de confusión multiclase.

---

### ⏱️ Minuto 4:00 – 5:00 | Demostración del Prototipo en Streamlit, Ética e Impacto
- **Locución (Español):**  
  *"El sistema fue desplegado en una arquitectura en capas desacoplada:*  
  *Una **Landing Page** moderna en GitHub Pages para la presentación pública del proyecto, y una aplicación interactiva en **Streamlit Cloud** que permite a los operadores cargar imágenes o activar la cámara web en tiempo real para clasificar residuos al instante.*  
  *Bajo el principio de **IA Verde y Ética Responsable**, garantizamos privacidad en riberas sin capturar rostros humanos, y diseñamos el sistema como soporte a la decisión bajo el modelo Human-in-the-Loop.*  
  *Este proyecto demuestra que la Inteligencia Artificial es una aliada tangible y accesible para salvar nuestras fuentes de agua dulce y construir un futuro sostenible. ¡Muchas gracias!"*
- **Recurso Visual:** Capturas dinámicas de la aplicación en Streamlit funcionando en vivo, enlaces al repositorio GitHub y créditos académicos UFHEC.

