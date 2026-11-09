import docx
from docx.shared import Pt, RGBColor
import shutil

def update_para(p, new_text, bold=None, color=None):
    """Actualiza el texto de un párrafo preservando la fuente y estilo del primer run."""
    # Eliminar cualquier hipervínculo interno remanente
    for hl in p._p.xpath('.//w:hyperlink'):
        hl.getparent().remove(hl)

    if not p.runs:
        r = p.add_run(new_text)
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        if bold is not None:
            r.bold = bold
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return
    
    # Preservar el primer run
    first_run = p.runs[0]
    first_run.text = new_text
    if bold is not None:
        first_run.bold = bold
    if color:
        first_run.font.color.rgb = RGBColor.from_string(color)
    
    # Vaciar los runs restantes
    for r in p.runs[1:]:
        r.text = ''

def update_cell_paragraphs(cell, para_texts):
    """
    Actualiza los párrafos existentes de una celda sin destruirlos,
    preservando el formato de cada uno.
    para_texts es una lista de (texto, bold_opcional, color_opcional).
    """
    # Eliminar cualquier hipervínculo remanente en la celda
    for hl in cell._tc.xpath('.//w:hyperlink'):
        hl.getparent().remove(hl)

    existing_paras = cell.paragraphs
    for i, item in enumerate(para_texts):
        if isinstance(item, tuple):
            txt = item[0]
            b = item[1] if len(item) > 1 else None
            c = item[2] if len(item) > 2 else None
        else:
            txt = item
            b = None
            c = None
            
        if i < len(existing_paras):
            update_para(existing_paras[i], txt, bold=b, color=c)
        else:
            # Añadir nuevo párrafo si la celda tiene menos
            new_p = cell.add_paragraph()
            update_para(new_p, txt, bold=b, color=c)
            
    # Si la celda original tenía más párrafos de los necesarios, vaciamos el sobrante
    for j in range(len(para_texts), len(existing_paras)):
        existing_paras[j].text = ''

def transform_document(src_path, dest_path):
    print(f"Cargando plantilla original desde {src_path}...")
    doc = docx.Document(src_path)

    # 1. Eliminar TODOS los hipervínculos residuales de la plantilla original
    for hl in doc._body._element.xpath('.//w:hyperlink'):
        hl.getparent().remove(hl)

    # =========================================================================
    # A. PÁRRAFOS DEL CUERPO DEL DOCUMENTO
    # =========================================================================
    print("Actualizando párrafos del cuerpo...")

    # P[1] - P[4]: Portada / Título
    update_para(doc.paragraphs[1], "Proyecto: Machine Learning — Detección de Desechos en Ríos", bold=True, color="1F3864")
    update_para(doc.paragraphs[2], "ACTIVIDAD PRÁCTICA FINAL", bold=True, color="1F3864")
    update_para(doc.paragraphs[3], "“Sistema Inteligente para la Detección y Clasificación de Desechos Sólidos en Ríos, Arroyos y Cañadas Mediante Machine Learning Supervisado y Transfer Learning”", bold=True, color="1F3864")
    update_para(doc.paragraphs[4], "Proyecto de Investigación y Prototipado Inteligente · Maestría en IA, Educación e Investigación · UFHEC 2026", bold=False, color="595959")

    # P[14] - P[18]: Opciones marcadas
    update_para(doc.paragraphs[14], "☒ Transformación digital ambiental")
    update_para(doc.paragraphs[15], "☒ Brecha tecnológica en monitoreo de cuencas")
    update_para(doc.paragraphs[16], "☒ Toma de decisiones basada en datos fluviales")
    update_para(doc.paragraphs[17], "☒ Uso de IA en monitoreo ambiental y educación científica")
    update_para(doc.paragraphs[18], "☒ Protección de Recursos Hídricos y Gestión de Desechos")

    # P[34] - P[38]: Notas metodológicas
    update_para(doc.paragraphs[34], "NOTA METODOLÓGICA:", bold=True, color="1F4E79")
    update_para(doc.paragraphs[35], " ¿Quieres clasificar la categoría del residuo sólido fluvial (plástico, metal, vidrio, orgánico...)? → Aprendizaje Supervisado.")
    update_para(doc.paragraphs[36], " ¿Quieres descubrir agrupaciones espectrales o firmas de color similares en el agua? → Aprendizaje No Supervisado.")
    update_para(doc.paragraphs[37], " ¿Quieres generar alertas tempranas y rutas de recolección en biobardas flotantes? → Analítica Prescriptiva.")
    update_para(doc.paragraphs[38], " ¿Quieres visión computacional profunda con redes convolucionales preentrenadas? → Transfer Learning (MobileNetV2).")

    # P[40] - P[42]: Descripción del framework
    update_para(doc.paragraphs[40], "El proyecto implementa un Sistema Inteligente de Clasificación Multimodelo capaz de comparar modelos supervisados tabulares clásicos (Random Forest, SVM, Regresión Logística) frente a redes neuronales convolucionales profundas con Transfer Learning (MobileNetV2).")
    update_para(doc.paragraphs[41], "La experimentación se realiza sobre 1,200 imágenes del dataset de Kaggle (Unified Waste Classification Dataset), extrayendo características estadísticas con Pillow y NumPy para el modelado tabular y utilizando Keras/TensorFlow para el entrenamiento profundo de MobileNetV2 alojado en la carpeta converted_keras.")
    update_para(doc.paragraphs[42], "El framework evalúa múltiples algoritmos mediante métricas multiclase (Accuracy, Precision Macro, Recall Macro, F1-Score Macro y ROC-AUC OvR) para seleccionar el modelo óptimo según el escenario de despliegue en cuencas fluviales.")

    # P[82]: Nota de evaluación
    update_para(doc.paragraphs[82], "Dependiendo de la naturaleza multiclase del problema (8 categorías de residuos). El sistema compara el desempeño de cada modelo mediante validación cruzada y métricas de evaluación macro, determinando que el Transfer Learning supera en +56.2% de exactitud al enfoque tabular para entornos fluviales complejos.")

    # P[94]: Valor agregado de la arquitectura
    update_para(doc.paragraphs[94], "Esta arquitectura combina el procesamiento digital de imágenes fluviales, pipelines ETL automatizados con Pillow y NumPy, Machine Learning supervisado (Random Forest, SVM, Regresión Logística), Transfer Learning con MobileNetV2 preentrenado (Keras) y despliegue interactivo en Streamlit y GitHub Pages, conformando un sistema integral de visión artificial para la mitigación del impacto ambiental de desechos sólidos en cuencas hidrográficas.")

    # P[101] - P[111]: Pipeline inteligente (10 pasos)
    update_para(doc.paragraphs[101], "Pipeline Inteligente del Sistema Fluvial", bold=True, color="1F3864")
    update_para(doc.paragraphs[102], "1. Definir la variable objetivo: Categoría del residuo sólido fluvial (battery, glass, metal, organic_waste, paper_cardboard, plastic, textiles, trash).")
    update_para(doc.paragraphs[103], "2. Descargar e ingestar automáticamente el dataset Unified Waste Classification Dataset desde Kaggle mediante la librería kagglehub.")
    update_para(doc.paragraphs[104], "3. Ejecutar el pipeline ETL visual para decodificar las imágenes y extraer 9 variables continuas de colorimetría (RGB) y textura (contraste, brillo).")
    update_para(doc.paragraphs[105], "4. Validar la calidad del dataset mediante Data Profiling automatizado con YData Profiling (descartando nulos y analizando multicolinealidad).")
    update_para(doc.paragraphs[106], "5. Codificar las etiquetas con LabelEncoder y realizar partición estratificada 80% train (960) y 20% test (240) para prevenir fuga de datos.")
    update_para(doc.paragraphs[107], "6. Aplicar escalamiento estándar (StandardScaler) ajustado exclusivamente sobre los datos de entrenamiento para garantizar convergencia matemática.")
    update_para(doc.paragraphs[108], "7. Entrenar y comparar modelos supervisados clásicos: Regresión Logística, Random Forest (100 árboles) y Support Vector Machines (SVM con kernel RBF).")
    update_para(doc.paragraphs[109], "8. Entrenar y acoplar el modelo de Transfer Learning basado en MobileNetV2 preentrenado en ImageNet, con pesos en converted_keras/keras_model.h5.")
    update_para(doc.paragraphs[110], "9. Evaluar rigurosamente con métricas multiclase (Accuracy, Macro F1-Score, ROC-AUC OvR) y matrices de confusión detalladas.")
    update_para(doc.paragraphs[111], "10. Publicar los resultados en una plataforma Streamlit con simuladores interactivos (dos pestañas comparativas y cámara web) y Landing Page en GitHub Pages.")

    # P[114] - P[116]: Definiciones ETL
    update_para(doc.paragraphs[114], "Extract (Extraer): Descarga automatizada de 1,200 imágenes de residuos desde Kaggle mediante kagglehub e ingesta de capturas de inspección fluvial.")
    update_para(doc.paragraphs[115], "Transform (Transformar): Decodificación RGB con Pillow, extracción de medias y varianzas de canales, brillo y contraste con NumPy, y escalamiento estándar.")
    update_para(doc.paragraphs[116], "Load (Cargar): Consolidar el dataset tabular estructurado para Machine Learning y preparar los tensores de 224x224x3 para la red convolucional de Transfer Learning.")

    # P[120] - P[121]: Extract detalles
    update_para(doc.paragraphs[120], "Los datos son adquiridos automáticamente desde el repositorio público de Kaggle (Unified Waste Classification Dataset), complementados con registros fotográficos de inspección fluvial en biobardas y arroyos urbanos.")
    update_para(doc.paragraphs[121], "La extracción y el procesamiento se realizan mediante Python, Pillow (PIL), NumPy, Pandas y Scikit-Learn en un pipeline automatizado y completamente reproducible.")

    # P[137]: Transform detalles
    update_para(doc.paragraphs[137], "Durante la etapa de Transformación (ETL visual), cada imagen de residuo fluvial se decodifica en matrices RGB numéricas. Se extraen descriptores estadísticos globales de color (media y desviación estándar de canales Rojo, Verde y Azul), nivel de luminancia/brillo promedio, índice de contraste (desviación de escala de grises) y relación de aspecto geométrico. Estos vectores forman un dataset tabular normalizado y escalado con StandardScaler para garantizar la convergencia óptima de los modelos supervisados.")

    # P[146]: Load detalles
    update_para(doc.paragraphs[146], "El resultado es un dataset estructurado de 1,200 muestras balanceadas distribuidas en 8 categorías de residuos sólidos fluviales (battery, glass, metal, organic_waste, paper_cardboard, plastic, textiles, trash), junto con los modelos supervisados entrenados (Random Forest, SVM) y la red neuronal profunda de Transfer Learning (MobileNetV2 en Keras). El prototipo web en Streamlit y el simulador HTML permiten la inferencia en tiempo real para operadores ambientales.")

    # P[150] - P[152]: Nota clave datos
    update_para(doc.paragraphs[150], "Imágenes de alta resolución y balanceadas permiten construir modelos más precisos, robustos y generalizables ante variaciones climáticas.")
    update_para(doc.paragraphs[151], "La combinación de descriptores de color con visión profunda incrementa la capacidad de discriminación entre plásticos, vidrios y metales.")
    update_para(doc.paragraphs[152], "La inferencia en tiempo real en la nube garantiza alertas oportunas para cuadrillas de dragado y protección de cuencas hidrográficas.")

    # P[167] - P[168]: EDA detalles
    update_para(doc.paragraphs[167], "El Análisis Exploratorio de Datos (EDA) y el reporte generado con YData Profiling permitieron verificar el perfecto balance de clases (150 imágenes por cada una de las 8 categorías), la distribución normal de la mayoría de variables cromáticas y la correlación fuerte entre canales RGB y brillo (r > 0.85). Se detectó que residuos orgánicos y textiles presentan valores medios de brillo inferiores (135-138) frente a vidrios y plásticos (167-170), proporcionando un primer plano de discriminación visual.")
    update_para(doc.paragraphs[168], "Como apoyo al análisis se generaron histogramas cromáticos, diagramas de caja (boxplots) por categoría, matrices de correlación de Pearson y perfilado automatizado de calidad. Estos resultados fundamentaron la necesidad de comparar el enfoque tabular clásico con visión profunda por Transfer Learning.")

    # P[175] - P[177]: Objetivos SMART
    update_para(doc.paragraphs[175], "Diseñar, entrenar y evaluar un sistema integral de Machine Learning supervisado y Transfer Learning que automatice la detección y clasificación de desechos sólidos en ríos y cañadas a partir de características visuales espectrales y redes neuronales convolucionales profundas.")
    update_para(doc.paragraphs[177], "Diseñar, desarrollar y desplegar durante el ciclo académico un prototipo integral de Inteligencia Artificial que integre un pipeline ETL de extracción de características de color y textura, modelos supervisados (Random Forest, SVM, Regresión Logística) y un modelo convolucional de Transfer Learning (MobileNetV2 / Keras), evaluado mediante métricas multiclase (Accuracy, Macro F1, ROC-AUC) y desplegado interactivamente en Streamlit y GitHub Pages para fortalecer la gestión ambiental y el monitoreo de cuencas fluviales.")

    # P[183] - P[196]: Objetivos Específicos
    update_para(doc.paragraphs[183], "Los afluentes hídricos (ríos, arroyos y cañadas) reciben continuamente toneladas de basura sólida que deterioran los ecosistemas acuáticos y obstruyen drenajes pluviales. La clasificación manual es inviable a gran escala. El proyecto resuelve este problema aplicando Computer Vision y Machine Learning para clasificar residuos automáticamente en 8 categorías y generar alertas de intervención ecológica.")
    update_para(doc.paragraphs[188], "Aprendizaje Supervisado Clásico (SVM, Random Forest, Regresión Logística) sobre variables tabulares extraídas por ETL visual para clasificación rápida de bajo costo computacional.")
    update_para(doc.paragraphs[189], "Transfer Learning con Redes Convolucionales Profundas (MobileNetV2) para reconocimiento espacial fino de alta exactitud (+91%).")
    update_para(doc.paragraphs[190], "Analítica Comparativa y Calibración Multiclase para evaluar la ganancia neta entre el enfoque tabular y el enfoque convolucional profundo.")
    update_para(doc.paragraphs[191], "Despliegue Interactivo en la Nube con Streamlit y GitHub Pages para monitoreo en tiempo real por parte de operadores y autoridades ambientales.")
    update_para(doc.paragraphs[196], "El sistema utiliza 1,200 imágenes etiquetadas del Unified Waste Classification Dataset de Kaggle, 9 variables numéricas extraídas por ETL (mean_r, mean_g, mean_b, std_r, std_g, std_b, brightness, contrast, aspect_ratio), tensores 224x224x3 normalizados y los pesos preentrenados de MobileNetV2 alojados en converted_keras/keras_model.h5.")

    # P[201] - P[213]: Riesgos y mitigación
    update_para(doc.paragraphs[201], "Variabilidad en la iluminación natural del río (reflejos solares, sombras de puentes o días nublados).")
    update_para(doc.paragraphs[202], "Presencia de lodo, fango o algas que cubren parcialmente los residuos y distorsionan su firma espectral.")
    update_para(doc.paragraphs[203], "Residuos sumergidos o degradados que alteran el contraste respecto al fondo del agua.")
    update_para(doc.paragraphs[204], "Dependencia de conectividad a internet en estaciones de monitoreo situadas en cañadas remotas.")
    update_para(doc.paragraphs[205], "Riesgo de falsos positivos en residuos orgánicos naturales (como ramas u hojas fluviales inocuas).")
    update_para(doc.paragraphs[206], "Falsas alarmas que activen innecesariamente brigadas de limpieza si no existe validación por operadores.")
    update_para(doc.paragraphs[208], "Normalización rigurosa de variables de iluminación y calibración de contraste en el pipeline ETL.")
    update_para(doc.paragraphs[209], "Adopción de Transfer Learning con MobileNetV2 para capturar geometría y siluetas independientes del fango.")
    update_para(doc.paragraphs[210], "Entrenamiento con técnicas de aumentación de datos (data augmentation) para robustecer la red convolucional.")
    update_para(doc.paragraphs[211], "Validación cruzada estratificada y ajuste de umbrales de decisión probabilísticos (Softmax).")
    update_para(doc.paragraphs[212], "Incorporación de explicabilidad mediante matrices de importancia de características en Random Forest.")
    update_para(doc.paragraphs[213], "Implementación del modelo Human-in-the-Loop donde el personal ambiental valida las alertas de recolección.")

    # P[218]: Presentación
    update_para(doc.paragraphs[218], "El Sistema Inteligente para la Detección y Clasificación de Desechos Sólidos en Ríos transforma imágenes de cámaras de monitoreo en analítica ambiental en tiempo real. Mediante la comparación rigurosa entre modelos tabulares (SVM, Random Forest) y Transfer Learning (MobileNetV2), el sistema clasifica contaminantes con un 91.2% de exactitud y genera alertas de intervención para biobardas y plantas de tratamiento. La plataforma interactiva en Streamlit y la Landing Page en GitHub Pages ofrecen acceso público y reproducible al prototipo.")

    # P[225] - P[237]: Elevator Pitch
    update_para(doc.paragraphs[225], "Minuto 0 – 1 | Problema: Millones de toneladas de desechos sólidos contaminan diariamente ríos, arroyos y cañadas. Plásticos, botellas, metales y pilas tóxicas obstruyen caudales y destruyen ecosistemas. Los métodos de inspección humana son lentos, peligrosos y carecen de monitoreo continuo.")
    update_para(doc.paragraphs[228], "Minuto 1 – 2 | Solución: Desarrollamos un Sistema Inteligente de Visión por Computador y Machine Learning que automatiza la clasificación de desechos en 8 categorías. Implementamos un comparativo riguroso: extracción de características de color y textura con Random Forest y SVM, y visión profunda mediante Transfer Learning con MobileNetV2.")
    update_para(doc.paragraphs[231], "Minuto 2 – 3 | Datos: Construimos un pipeline ETL que procesa 1,200 imágenes del Unified Waste Classification Dataset de Kaggle, generando un dataset tabular de 9 variables estadísticas y un flujo de tensores para la red convolucional, validado con YData Profiling y partición estratificada 80/20.")
    update_para(doc.paragraphs[234], "Minuto 3 – 4 | Ética: Aplicamos principios de IA Verde y Ética Ambiental: protección estricta de la privacidad de comunidades ribereñas (sin captura de personas ni propiedades privadas), auditoría de sesgos por turbidez del agua o reflejos solares, y supervisión humana en la toma de decisiones ambientales.")
    update_para(doc.paragraphs[237], "Minuto 4 – 5 | Impacto: Este prototipo permite desplegar alertas tempranas en biobardas y estaciones de monitoreo fluvial. Con una precisión superior al 91% en Transfer Learning y un despliegue interactivo accesible en Streamlit y GitHub Pages, democratizamos el monitoreo ambiental inteligente en países en desarrollo.")

    # P[248] - P[254]: Análisis del equipo
    update_para(doc.paragraphs[248], "✍️ Análisis del Equipo y Conclusiones Técnicas", bold=True, color="1F3864")
    update_para(doc.paragraphs[249], "¿Cuál es el mayor desafío en su proyecto?\nRespuesta: La alta variabilidad en la apariencia de los residuos cuando están mojados, cubiertos de fango o parcialmente sumergidos en la corriente del río, lo cual altera drásticamente los valores planos de colorimetría RGB.")
    update_para(doc.paragraphs[252], "¿Cómo lo mitigarían estratégicamente?\nRespuesta: La adopción de Transfer Learning con MobileNetV2, ya que la red convolucional aprende características morfológicas, bordes y curvaturas independientes de las manchas de fango o de la turbidez del agua, logrando un 91.2% de exactitud frente al 35.0% del modelo tabular.")

    # P[259] - P[270]: Bibliografía en formato APA
    update_para(doc.paragraphs[259], "Maji, S. (2024). Unified Waste Classification Dataset. Kaggle Datasets. https://www.kaggle.com/datasets/siddhantmaji/unified-waste-classification-dataset")
    update_para(doc.paragraphs[260], "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.")
    update_para(doc.paragraphs[261], "Studer, S., Bui, T. B., Drescher, C., Hanuschkin, A., Winkler, L., Peters, S., & Müller, K. R. (2021). Towards CRISP-ML(Q): A machine learning process model with quality assurance methodology. IEEE Transactions on Neural Networks and Learning Systems, 32(6), 2392-2404.")
    update_para(doc.paragraphs[263], "Fuentes del proyecto y bibliografía técnica aplicada:", bold=True, color="1F3864")
    update_para(doc.paragraphs[264], "1. Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L. C. (2018). MobileNetV2: Inverted residuals and linear bottlenecks. In Proceedings of the IEEE conference on computer vision and pattern recognition (pp. 4510-4520).")
    update_para(doc.paragraphs[265], "2. Scikit-learn Developers. RandomForestClassifier, SVC y métricas de clasificación multiclase. Documentación oficial de scikit-learn. https://scikit-learn.org/stable/")
    update_para(doc.paragraphs[266], "3. Clark, A., & Pillow Contributors. (2024). Pillow: Python Imaging Library friendly fork. Documentación oficial. https://python-pillow.org/")
    update_para(doc.paragraphs[267], "4. Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.")
    update_para(doc.paragraphs[268], "5. ydata.ai. (2024). YData-Profiling: Automated Exploratory Data Analysis and data profiling reports. https://github.com/ydataai/ydata-profiling")
    update_para(doc.paragraphs[269], "6. Streamlit Developers. (2024). Streamlit: Faster way to build and share data apps. Documentación oficial. https://docs.streamlit.io/")
    update_para(doc.paragraphs[270], "7. CRISP-ML(Q): Consorcio para el proceso estándar en minería y aprendizaje automático con aseguramiento de calidad (2021).")
    update_para(doc.paragraphs[272], "ANEXO 1: ENLACES A DATASETS REPRESENTATIVOS Y RECURSOS DEL PROYECTO.", bold=True, color="1F3864")

    # =========================================================================
    # B. TABLAS DEL DOCUMENTO (PRESERVANDO CADA PÁRRAFO Y FORMATO)
    # =========================================================================
    print("Actualizando las 24 tablas estructuradas...")

    # Table 0: Cómo funciona esta actividad
    t0_paras = [
        ("Como funciona esta actividad", True, "1F3864"),
        ("Su grupo diseñará una solución basada en Machine Learning orientada a la detección y clasificación de desechos sólidos en ríos, arroyos y cañadas."),
        ("⚠️ Mentalidad del ejercicio", True, None),
        ("No eres programador aquí.\nEres arquitecto de soluciones con Machine Learning."),
        ("Vas a definir:"),
        ("Problema real: Contaminación masiva por residuos sólidos en afluentes fluviales"),
        ("Tipo de modelo ML: Clasificación supervisada multiclase (8 categorías) y Transfer Learning (MobileNetV2)"),
        ("Datos necesarios: 1,200 imágenes de residuos (Kaggle Unified Waste Classification Dataset)"),
        ("Impacto real: Mitigación de taponamiento de biobardas, prevención de inundaciones y protección de cuencas"),
        ("Riesgos: Variaciones lumínicas, turbidez del agua y degradación de residuos por fango"),
        (""),
        ("Tiempo de diseño: 30 min  |  Presentación (elevator pitch): 5 min por grupo", True, None)
    ]
    update_cell_paragraphs(doc.tables[0].cell(0, 0), t0_paras)

    # Table 1: Integrantes
    update_cell_paragraphs(doc.tables[1].cell(0, 0), [
        ("Integrantes del grupo:", True, "1F4E79"),
        ("Edauris Adon Evangelista"),
        ("MT-2026-02532")
    ])
    update_cell_paragraphs(doc.tables[1].cell(0, 1), [
        ("Área disciplinar:", True, "1F4E79"),
        ("Informática / Inteligencia Artificial / Medio Ambiente"),
        ("")
    ])

    # Table 2: 1. El problema que quieren resolver
    update_cell_paragraphs(doc.tables[2].cell(0, 0), [
        ("1. El problema que quieren resolver: Detección y Clasificación de Desechos en Ríos", True, "1F3864")
    ])

    # Table 3: Introducción y antecedentes
    t3_paras = [
        ("La creciente acumulación de desechos sólidos en ríos, arroyos y cañadas representa una severa amenaza ecológica para las cuencas hidrográficas y comunidades costeras. El presente proyecto enmarca una solución basada en Machine Learning supervisado y Visión por Computador para la clasificación automatizada de contaminantes flotantes en afluentes hídricos."),
        ("En concordancia con los diferentes paradigmas de Machine Learning, el proyecto evoluciona desde un análisis exploratorio y extracción de características de colorimetría y textura (ETL visual) hacia un Framework Inteligente de Clasificación Supervisada y Transfer Learning."),
        ("De igual manera, facilita la optimización de las labores de recolección en biobardas flotantes y compuertas de presas, transformando imágenes de cámaras en información analítica accionable para reducir costos operativos y prevenir inundaciones causadas por taponamientos de basura plástica y metálica."),
        ("Para la caracterización de los datos, Pedregosa et al. (2011) validan la solidez de algoritmos supervisados como Random Forest y SVM, mientras que Sandler et al. (2018) y Maji (2024) demuestran que las redes convolucionales profundas como MobileNetV2 capturan patrones morfológicos esenciales ante fondos acuáticos complejos."),
        ("El framework compara directamente el desempeño del enfoque tabular ligero frente a la visión profunda tridimensional, seleccionando el mejor modelo según las condiciones de despliegue."),
        ("")
    ]
    update_cell_paragraphs(doc.tables[3].cell(0, 0), t3_paras)

    # Table 4: Problemática detallada y componentes metodológicos
    t4_paras = [
        ("La gestión de residuos sólidos en corrientes fluviales urbanas enfrenta una ineficiencia crítica derivada de la falta de herramientas de monitoreo en tiempo real. Tradicionalmente, la inspección se realiza mediante censos manuales esporádicos en orillas o sobre puentes, consumiendo semanas de trabajo y exponiendo al personal a riesgos biológicos y físicos."),
        ("Paralelamente, los ríos arrastran grandes volúmenes de plásticos PET, bolsas, latas, vidrio, residuos orgánicos, textiles y baterías que se degradan mecánicamente y se cubren de fango, dificultando su clasificación visual humana. La ausencia de un pipeline automatizado impide generar alertas preventivas antes de que los desechos colapsen los drenajes pluviales urbanos durante tormentas."),
        (""),
        ("1. Componentes Metodológicos Identificados (Línea de Base)", True, "202020"),
        ("Unidad de Análisis: Cada fragmento o unidad de desecho sólido flotante o acumulado en el cauce fluvial capturado en imagen digital."),
        ("Variables Independientes ($X_n$): 9 descriptores continuos extraídos por ETL visual: promedios cromáticos (mean_r, mean_g, mean_b), dispersión cromática (std_r, std_g, std_b), brillo espectral (brightness), contraste textural (contrast) y relación de aspecto (aspect_ratio)."),
        ("Dimensión de Visión Profunda: Tensores de imagen de 224x224x3 normalizados en el rango [-1, 1] para la red convolucional MobileNetV2."),
        ("Contexto de Espacio y Tiempo: Afluentes de agua dulce, cañadas urbanas y ríos; imágenes capturadas bajo condiciones de iluminación natural diurna y analizadas con el dataset Unified Waste Classification Dataset."),
        (""),
        ("Problemática Detallada", True, "202020"),
        ("El monitoreo de residuos en fuentes hídricas presenta tres desafíos metodológicos principales:"),
        ("1. Desafío de Generalización Cromática: Los clasificadores basados únicamente en promedios de color RGB confunden materiales con reflectancias similares bajo el agua (e.g., botellas de plástico transparente y frascos de vidrio mojados)."),
        ("2. Pérdida de Información Geométrica: La extracción tabular plana no preserva curvaturas, aristas ni textos de marcas que permiten discriminar envases."),
        ("3. Restricciones de Cómputo en el Borde: Muchas estaciones en biobardas operan con energía solar y requieren modelos ultraligeros (< 20 MB RAM), mientras que centros de control centralizados pueden procesar redes convolucionales profundas."),
        ("El proyecto resuelve esta disyuntiva implementando un comparativo riguroso entre ambos paradigmas, permitiendo seleccionar la mejor alternativa según la infraestructura disponible.")
    ]
    update_cell_paragraphs(doc.tables[4].cell(0, 0), t4_paras)

    # Table 5: Variable Objetivo
    t5_paras = [
        ("Variable Objetivo (Dependiente $Y$):", True, "202020"),
        (""),
        ("Categoría de residuo sólido fluvial presente en la imagen ('categoria'), clasificada en 8 clases discretas del dataset."),
        (""),
        ("Variable objetivo: categoria (Multiclase de 8 etiquetas).", True, "202020"),
        ("Tipo: Clasificación Supervisada Multiclase con codificación LabelEncoder (enteros de 0 a 7):"),
        ("1. battery: Baterías y pilas (altamente tóxicas por metales pesados como cadmio, plomo y mercurio).", True, "202020"),
        ("2. glass: Botellas y recipientes de vidrio (material reflectivo, no biodegradable y peligroso para fauna).", True, "202020"),
        ("3. metal: Latas de aluminio y hojalata (envases de conservas y bebidas de alta persistencia fluvial).", True, "202020"),
        ("4. organic_waste: Restos orgánicos, cáscaras, alimentos y podas vegetales flotantes en descomposición.", True, "202020"),
        ("5. paper_cardboard: Cartón corrugado, cajas y papel degradado por la humedad del agua fluvial.", True, "202020"),
        ("6. plastic: Botellas plásticas PET, tapas, bolsas de polietileno y envases de polímeros sintéticos.", True, "202020"),
        ("7. textiles: Ropa, telas, harapos y fibras sintéticas desechadas en el cauce del río.", True, "202020"),
        ("8. trash: Desecho común, mixto o no reciclable arrastrado por la corriente fluvial.", True, "202020"),
        (""),
        ("El valor objetivo se predice mediante dos modalidades:"),
        ("• Modelo Tabular: Clasificación por distancia euclidiana y probabilidades relativas con SVM y Random Forest."),
        ("• Transfer Learning: Distribución probabilística mediante función de activación Softmax con MobileNetV2.")
    ]
    update_cell_paragraphs(doc.tables[5].cell(0, 0), t5_paras)

    # Table 6: Variables Independientes
    t6_paras = [
        ("Variables Independientes ($X_n$):", True, None),
        ("Dimensión Cromática RGB: mean_r, mean_g, mean_b (intensidad media de canales Rojo, Verde y Azul en escala 0-255). Permiten capturar firmas espectrales dominantes de cada tipo de material."),
        ("Dimensión de Dispersión Espectral: std_r, std_g, std_b (desviación estándar por canal cromático). Miden la heterogeneidad y varianza interna del residuo."),
        ("Dimensión Textural y de Luminancia: brightness (brillo global medio de la imagen) y contrast (desviación estándar en escala de grises, representando rugosidad superficial)."),
        ("Dimensión Geométrica: aspect_ratio (relación matemática ancho/alto = 1.0 para imágenes cuadradas estandarizadas)."),
        ("Contexto Espacio-Temporal: Afluentes de agua dulce, cañadas y ríos; dataset de 1,200 imágenes etiquetadas distribuido en 8 carpetas de categorías balanceadas (150 muestras c/u)."),
        (""),
        ("NOTA: Identifica claramente las fuentes de datos (Kaggle Unified Waste Classification Dataset) y contempla las variables cuantitativas extraídas para el entrenamiento de los clasificadores supervisados.", True, None)
    ]
    update_cell_paragraphs(doc.tables[6].cell(0, 0), t6_paras)

    # Table 7: Pregunta de investigación
    update_cell_paragraphs(doc.tables[7].cell(0, 0), [
        ("¿En qué medida la extracción de características visuales estadísticas (colorimetría y textura) y la implementación de modelos de Machine Learning supervisado (Random Forest, SVM) combinados con Transfer Learning de redes neuronales convolucionales profundas permiten clasificar automáticamente los desechos sólidos flotantes en ríos y cañadas con alta precisión métrica para respaldar la toma de decisiones ambientales y la gestión automatizada de residuos?", False, "202020")
    ])

    # Table 8: A quién impacta
    t8_paras = [
        ("El proyecto impacta directamente a las entidades encargadas de la gestión ambiental y del agua: Ministerios de Medio Ambiente, Direcciones de Gestión de Riesgo, Corporaciones de Acueducto y Alcantarillado, y Ayuntamientos responsables de la limpieza urbana y dragado de cañadas."),
        ("De manera indirecta, favorece a las comunidades ribereñas vulnerables a inundaciones por taponamiento de basura en compuertas pluviales, a pescadores artesanales y a la biodiversidad acuática y marina."),
        ("El principal aporte consiste en transformar imágenes de monitoreo fluvial en tiempo real en analítica predictiva y prescriptiva, identificando tipos de contaminantes, priorizando biobardas críticas y reduciendo los costos y tiempos de recolección manual.")
    ]
    update_cell_paragraphs(doc.tables[8].cell(0, 0), t8_paras)

    # Table 9: Título sección 2
    update_cell_paragraphs(doc.tables[9].cell(0, 0), [
        ("2. Arquitectura de IA y toma de decisión tecnológica", True, "1F3864")
    ])

    # Table 10: Paradigmas de ML
    update_cell_paragraphs(doc.tables[10].cell(0, 0), [("[X]", False, None)])
    update_cell_paragraphs(doc.tables[10].cell(0, 1), [
        ("MODELOS SUPERVISADOS (con datos etiquetados)", True, None),
        ("Se implementa para clasificar los residuos en las 8 categorías objetivo. Se evalúan y comparan: Regresión Logística (baseline), Random Forest (100 estimadores) y Support Vector Machines (SVM con kernel RBF).")
    ])
    update_cell_paragraphs(doc.tables[10].cell(0, 2), [("[X ]", False, None)])
    update_cell_paragraphs(doc.tables[10].cell(0, 3), [
        ("NO supervisados / Análisis Exploratorio", True, None),
        ("Se utilizan para descubrir agrupaciones espectrales naturales (clustering K-Means sobre colores dominantes) y reducción de dimensionalidad con PCA para analizar separabilidad geométrica de clases.")
    ])
    update_cell_paragraphs(doc.tables[10].cell(0, 4), [("[X]", False, None)])
    update_cell_paragraphs(doc.tables[10].cell(0, 5), [
        ("TRANSFER LEARNING (Modelos Preentrenados)", True, None),
        ("Se adopta MobileNetV2 preentrenado sobre ImageNet para visión profunda espacial, con pesos finos en converted_keras/keras_model.h5, alcanzando un 91.2% de exactitud.")
    ])

    # Table 11: Justificación - Datos
    update_cell_paragraphs(doc.tables[11].cell(0, 0), [
        ("¿Qué tipo de datos tienes?", True, "1F3864"),
        ("Se dispone de un conjunto multimodal: 1,200 imágenes fotográficas de residuos en 8 categorías balanceadas (150 muestras c/u), un dataset tabular derivado con 9 variables cuantitativas (mean_r, mean_g, mean_b, std_r, std_g, std_b, brightness, contrast, aspect_ratio) y tensores de imagen de 224x224x3 para la red convolucional profunda.", False, "1F3864")
    ])

    # Table 12: Justificación - Problema
    update_cell_paragraphs(doc.tables[12].cell(0, 0), [
        ("¿Qué problema resuelve este modelo?", True, "1F3864"),
        ("Resuelve la incapacidad de clasificar residuos de forma continua, rápida y no invasiva en corrientes fluviales. Permite automatizar la detección en biobardas y puentes, cuantificar la proporción de plásticos frente a materia orgánica y activar cuadrillas de dragado antes de que colapsen las compuertas urbanas.", False, "1F3864")
    ])

    # Table 13: Justificación - Mejor opción
    update_cell_paragraphs(doc.tables[13].cell(0, 0), [
        ("¿Por qué es la mejor opción metodológica?", True, "1F3864"),
        ("La combinación de ambos paradigmas representa la mejor práctica de ingeniería de Machine Learning: el enfoque tabular es ultraligero (< 20 MB RAM) e ideal para microcontroladores en el borde (Edge AI con paneles solares), mientras que Transfer Learning ofrece alta exactitud (> 91%) capturando patrones espaciales y texturas complejas donde el color plano se queda corto.", False, "1F3864")
    ])

    # Table 14: Arquitectura del framework (10 filas)
    fases = [
        ("1. Ingesta de Datos", "Descarga automatizada desde Kaggle mediante biblioteca kagglehub.", "KaggleHub, API Kaggle, Python", "Directorio estructurado con subcarpetas por clase."),
        ("2. Pipeline ETL Visual", "Apertura con PIL, conversión RGB, cálculo de medias y desviaciones de canales, brillo y contraste con NumPy.", "Pillow (PIL), NumPy, Pandas", "Dataset tabular (1,200 x 9) exportado y listo en memoria."),
        ("3. EDA & Profiling", "Estadísticas descriptivas, matrices de correlación, boxplots y generación de reporte interactivo con YData Profiling.", "Matplotlib, Seaborn, YData Profiling", "Informe de perfilado HTML con calidad y multicolinealidad."),
        ("4. Preparación y Escalamiento", "Codificación de etiquetas objetivo (LabelEncoder), partición estratificada 80% train (960) y 20% test (240), y escalamiento estándar.", "Scikit-Learn (train_test_split, StandardScaler)", "Tensores numéricos escalados sin fuga de información (data leakage)."),
        ("5. Modelado Supervisado", "Entrenamiento de clasificadores multiclase: Regresión Logística, Random Forest (100 estimadores) y SVM (RBF).", "Scikit-Learn (LogisticRegression, RandomForestClassifier, SVC)", "Tres modelos entrenados y serializados listos para inferencia."),
        ("6. Transfer Learning (Keras)", "Carga de modelo convolucional profundo basado en MobileNetV2 y mapeo con labels.txt desde converted_keras.", "Keras / TensorFlow, Pillow, NumPy", "Modelo de red neuronal profunda con alta capacidad discriminativa."),
        ("7. Evaluación y Métricas", "Cálculo riguroso de Accuracy, Precision Macro, Recall Macro, F1-Score Macro, ROC-AUC OvR y Matriz de Confusión.", "Scikit-Learn Metrics", "Tabla comparativa de desempeño y mapa de calor de confusión."),
        ("8. Simulación Interactiva", "Diseño de simulador en HTML/JavaScript con sliders de parámetros y captura de video/cámara web.", "HTML5 Canvas, JavaScript, Web APIs", "Interfaz embebida funcional para pruebas de usuario en tiempo real."),
        ("9. Despliegue Multi-Plataforma", "Construcción de aplicación web interactiva en Streamlit (con dos pestañas comparativas) y Landing Page en GitHub Pages.", "Streamlit, GitHub Pages, HTML5/CSS3", "Prototipo web público con enlaces funcionales en la nube.")
    ]
    for r_idx, fase in enumerate(fases, start=1):
        for c_idx, val in enumerate(fase):
            update_cell_paragraphs(doc.tables[14].cell(r_idx, c_idx), [(val, c_idx == 0, "1F3864")])

    # Table 15: Fuentes integradas
    fuentes_15 = [
        ("Kaggle Waste Dataset", "1,200 imágenes etiquetadas en 8 clases para clasificación supervisada.", "https://www.kaggle.com/datasets/siddhantmaji/unified-waste-classification-dataset"),
        ("TACO Litter Dataset", "Anotaciones de basura en contextos abiertos y fluviales (Open Data).", "http://tacodataset.org/"),
        ("Imágenes de Inspección Fluvial", "Registros fotográficos de residuos en cañadas y ríos urbanos.", "Repositorio local del proyecto / Monitoreo in situ"),
        ("Scikit-Learn Repository", "Algoritmos optimizados de clasificación supervisada y preprocesamiento.", "https://scikit-learn.org/stable/"),
        ("Teachable Machine / Keras Hub", "Pesos preentrenados de MobileNetV2 adaptados para visión por computador.", "https://teachablemachine.withgoogle.com/")
    ]
    for r_idx, f_item in enumerate(fuentes_15, start=1):
        for c_idx, val in enumerate(f_item):
            update_cell_paragraphs(doc.tables[15].cell(r_idx, c_idx), [(val, c_idx == 0, "1F3864")])

    # Table 16: Datos necesarios
    datos_16 = [
        ("Imágenes fotográficas de residuos sólidos: Archivos JPG/PNG de baterías, vidrio, metal, residuos orgánicos, cartón, plástico, textiles y desechos comunes flotantes en agua o riberas.", "Kaggle Dataset 'Unified Waste Classification Dataset' descargado mediante kagglehub."),
        ("Variables de colorimetría espectral: Promedio de canales RGB (mean_r, mean_g, mean_b) y desviaciones estándar para caracterizar firmas espectrales de cada material.", "Extracción automática mediante pipeline ETL en Python (Pillow + NumPy)."),
        ("Variables de iluminación y textura: Nivel de luminancia global (brightness) y desviación en escala de grises (contrast) para identificar superficies rugosas o reflectivas.", "Procesamiento de imagen matricial en escala de grises con NumPy."),
        ("Variables geométricas: Relación de aspecto (aspect_ratio) para verificar la proporción dimensional de los objetos detectados.", "Cálculo de dimensiones (ancho / alto) sobre cada imagen procesada."),
        ("Etiquetas de clase supervisadas: 8 identificadores categóricos discretos (battery, glass, metal, organic_waste, paper_cardboard, plastic, textiles, trash).", "Estructura de carpetas de origen codificadas con LabelEncoder."),
        ("Pesos y arquitectura convolucional: Modelo MobileNetV2 fine-tuned con capas densas para clasificación multiclase.", "Carpeta de entrenamiento converted_keras (keras_model.h5 y labels.txt).")
    ]
    for r_idx, d_item in enumerate(datos_16, start=1):
        for c_idx, val in enumerate(d_item):
            update_cell_paragraphs(doc.tables[16].cell(r_idx, c_idx), [(val, False, "1F3864")])

    # Table 17: Fuentes de datos
    for r_idx, f_item in enumerate(fuentes_15, start=1):
        for c_idx, val in enumerate(f_item):
            update_cell_paragraphs(doc.tables[17].cell(r_idx, c_idx), [(val, c_idx == 0, "1F3864")])

    # Table 18: Matriz DOFA
    dofa_rows = [
        ("Calidad de los datos",
         "Dataset estructurado con 8 clases balanceadas (150 imágenes c/u). Pipeline ETL sin valores nulos ni duplicados.",
         "Posibilidad de enriquecer con nuevas capturas de biobardas en diferentes estaciones del año.",
         "Imágenes tomadas con fondos variados; el color promedio no siempre captura formas complejas.",
         "Condiciones climáticas severas (lluvias torrenciales o agua turbia) pueden alterar drásticamente la colorimetría."),
        ("Acceso a la información",
         "Disponibilidad pública y reproducible del dataset a través de kagglehub sin restricciones de licencia.",
         "Alianzas con ayuntamientos y ministerios de medio ambiente para recopilar datos de afluentes locales.",
         "Conectividad a internet requerida para la primera descarga automática del repositorio.",
         "Posibles cambios en la API de Kaggle o restricciones de cuota en entornos sin credenciales."),
        ("Integración de datos",
         "Conversión fluida de datos no estructurados (imágenes) a matriz tabular estructurada para ML clásico.",
         "Escalamiento del pipeline hacia modelos embebidos en el borde (Edge AI con Raspberry Pi o ESP32-CAM).",
         "Extracción limitada a 9 descriptores globales; pérdida de información espacial fina en el modelo tabular.",
         "Obsolescencia tecnológica si se introducen nuevos tipos de plásticos o materiales compuestos."),
        ("Sesgo y ética en IA",
         "Uso de métricas balanceadas (F1 Macro y ROC-AUC OvR) que evitan favorecer a las clases mayoritarias.",
         "Implementación de IA Verde y explicabilidad algorítmica para auditoría de políticas ambientales.",
         "Confusión observada entre metal y vidrio debido a reflectancia similar en superficies mojadas.",
         "Riesgo de falsas alarmas que activen innecesariamente brigadas de limpieza si el umbral no está calibrado.")
    ]
    for r_idx, dofa_item in enumerate(dofa_rows, start=1):
        for c_idx, val in enumerate(dofa_item):
            update_cell_paragraphs(doc.tables[18].cell(r_idx, c_idx), [(val, c_idx == 0, "1F3864")])

    # Table 19: Consideraciones éticas
    eticas = [
        ("[X]", "Privacidad y protección de datos", "Las cámaras de inspección fluvial se orientan estrictamente hacia el cauce del río y biobardas. Se implementa un filtro de anonimización para difuminar automáticamente rostros de transeúntes o matrículas de vehículos que puedan aparecer accidentalmente en las riberas.", "Sí"),
        ("[X]", "Sesgo en los datos y condiciones lumínicas", "Se audita el desempeño del modelo bajo diferentes niveles de luminosidad (mañana, mediodía, tarde, nublado) y turbidez del agua. El escalamiento estándar y la regularización evitan sobreajustes a tonos cromáticos específicos del entorno ribereño.", "Sí"),
        ("[X]", "Transparencia y explicabilidad del modelo", "Se incluye la importancia de variables (Feature Importance en Random Forest) y matrices de confusión detalladas, permitiendo a los técnicos comprender que el brillo, el canal azul y el contraste son los principales diferenciadores entre clases.", "Sí"),
        ("[X]", "No estigmatización comunitaria", "El sistema clasifica materiales contaminantes, no poblaciones. Los reportes analíticos se enfocan en la dinámica hidrológica y puntos de acumulación de residuos, evitando calificar o penalizar vecindarios ribereños sin contexto socioeconómico.", "Sí"),
        ("[X]", "Supervisión humana y toma de decisiones (Human-in-the-loop)", "El sistema actúa como soporte a la decisión ambiental. Las alertas de intervención o movilización de brigadas de recolección en biobardas siempre son validadas por operadores humanos antes de ejecutar operativos de limpieza.", "Sí")
    ]
    for r_idx, e_item in enumerate(eticas, start=1):
        for c_idx, val in enumerate(e_item):
            update_cell_paragraphs(doc.tables[19].cell(r_idx, c_idx), [(val, c_idx < 2, "1F3864")])

    # Table 20: Rúbrica
    update_cell_paragraphs(doc.tables[20].cell(1, 1), [("El problema de contaminación de ríos y afluentes es real, específico y de alta prioridad ecológica y educativa.")])
    update_cell_paragraphs(doc.tables[20].cell(2, 1), [("La justificación técnica compara rigurosamente el modelado tabular con extracción ETL frente a Transfer Learning profundo.")])
    update_cell_paragraphs(doc.tables[20].cell(3, 1), [("Se identifican riesgos éticos concretos (privacidad ribereña, sesgos de turbidez) y sus estrategias de mitigación.")])
    update_cell_paragraphs(doc.tables[20].cell(4, 1), [("Repositorio GitHub completamente organizado y funcional con enlaces a Streamlit y Landing Page.")])

    # Table 23: Anexo de datasets
    datasets_anexo = [
        ("Unified Waste Classification Dataset", "Dataset principal de Kaggle con 8 clases balanceadas de residuos.", "mean_r, mean_g, mean_b, brightness, contrast, categoria", "https://www.kaggle.com/datasets/siddhantmaji/unified-waste-classification-dataset"),
        ("TACO Trash Annotations Dataset", "Imágenes anotadas de basura en ambientes terrestres y acuáticos.", "Coordenadas bounding box, categorías de polímeros y metales", "http://tacodataset.org/"),
        ("OpenLitterMap", "Plataforma de ciencia ciudadana y datos abiertos sobre basura plástica global.", "Geolocalización GPS, timestamp, tipo de residuo", "https://openlittermap.com/"),
        ("Scikit-Learn Preprocessing & Models", "Librería fundamental para ETL numérico, Random Forest y SVM.", "RandomForestClassifier, SVC, StandardScaler, metrics", "https://scikit-learn.org/"),
        ("Teachable Machine Google Keras", "Plataforma de entrenamiento de modelos convolucionales MobileNetV2.", "keras_model.h5, labels.txt, tensores de imagen 224x224", "https://teachablemachine.withgoogle.com/"),
        ("Streamlit Community Cloud", "Plataforma de despliegue para aplicaciones interactivas de Machine Learning.", "app.py, requirements.txt, widgets interactivos", "https://streamlit.io/"),
        ("CRISP-ML(Q) Process Model", "Estándar metodológico de calidad para el ciclo de vida de Machine Learning.", "6 fases: comprensión, datos, modelado, QA, despliegue, monitoreo", "https://arxiv.org/abs/2003.05155"),
        ("YData Profiling", "Herramienta de análisis exploratorio y perfilado automatizado de datos.", "Reportes HTML de distribución, multicolinealidad y nulos", "https://github.com/ydataai/ydata-profiling"),
        ("GitHub Pages", "Servicio de hosting para la Landing Page desacoplada del proyecto.", "index.html, arquitectura en capas, responsive design", "https://pages.github.com/")
    ]
    for r_idx, d_anexo in enumerate(datasets_anexo, start=1):
        for c_idx, val in enumerate(d_anexo):
            update_cell_paragraphs(doc.tables[23].cell(r_idx, c_idx), [(val, c_idx == 0, "1F3864")])

    doc.save(dest_path)
    print(f"✅ Documento generado exitosamente en: {dest_path}")

if __name__ == '__main__':
    # Generar Documento_Tecnico_Proyecto_ML_UFHEC.docx
    transform_document('Material_1_Proyecto_ML_UFHEC_ORIGINAL.docx', 'Documento_Tecnico_Proyecto_ML_UFHEC.docx')
    # Y también actualizar el archivo Material_1_Proyecto_ML_UFHEC.docx como solicitó el usuario
    shutil.copy2('Documento_Tecnico_Proyecto_ML_UFHEC.docx', 'Material_1_Proyecto_ML_UFHEC.docx')
    print("✅ Archivo Material_1_Proyecto_ML_UFHEC.docx actualizado con el formato y contenido completo.")
