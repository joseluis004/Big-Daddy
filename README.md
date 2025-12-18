# 🚀 FinPlus Analytics Challenge: De Datos a Decisiones Accionables (Big-Daddy)

---

## 1. 💡 Resumen y Objetivo Estratégico

Este repositorio contiene la solución completa única desarrollada por **Big-Daddy** para  "FinPlus Analytics Challenge". El proyecto se enfoca en la implementación de una arquitectura de datos robusta usando Docker y PySpark para generar inteligencia de negocio avanzada.

Nuestro objetivo es transformar los datos crudos de clientes (demográficos, digitales y transaccionales) en una inteligencia de negocio predictiva y accionable.

### Objetivos Clave de la Solución:

| # | Objetivo FinPlus | Resultado de la Solución |
| :-: | :--- | :--- |
| **1** | Comprender Clientes | **Segmentación Avanzada (Clustering)** para crear perfiles 360°. |
| **2** | Detectar Riesgos | **Modelo Predictivo de Incumplimineto de contratos** asignado a cada cliente. |
| **3** | Oportunidades | **Features RFMI** y métricas de propensión para impulsar el *cross-selling*. |
| **4** | Toma de Decisiones | **Dashboard Ejecutivo (Tableau)** con KPIs claros y narrativos. |
| **5** | Portal Interactivo | **Aplicación Streamlit** para predicciones en tiempo real. |

---

## 2. ⚙️ Arquitectura y Diseño Técnico (Informe 2)

El diseño del proyecto utiliza un modelo de **Arquitectura por Capas (Layered Architecture)** y se enfoca en el **Procesamiento por Lotes (Batch Processing)**, priorizando la precisión para el análisis de comportamiento histórico (RFMI, Churn).

### 2.1. Arquitectura de Datos y Motor

[Image of Layered Data Architecture]

* **Paradigma:** Arquitectura por Capas, enfoque en Batch Processing.
* **Motor Principal:** **Apache Spark / PySpark**. Es esencial para manejar el Volumen y la Variedad de los datos transaccionales.
* **Almacenamiento Final:** **Master_FINAL_CONSOLIDADO.parquet** en formato Parquet.

### 2.2. Flujo ETL (Extracción, Transformación, Carga)

Es el pipeline de procesamiento que permite Extraer(E), Tranformar(T) y Cargar(L) los datos inciales, opera bajo el motor de PySpark en un flujo modular dentro de la *Curated Layer*.

#### A. Extracción (E)
Se ingesta la información demográfica/contractual (`CLIENTS.csv`) y el comportamiento transaccional (`BEHAVIOURAL.parquet`) usando DataFrames distribuidos de PySpark.

#### B. Transformación (T)
1.  **Limpieza y Normalización:**
    * **Imputación Estratégica:** Se rellenan variables de *scoring* o antigüedad (CAR AGE, JOB_SENIORITY) con **-1** (valor sentinel).
    * Las variables de historial de préstamo se rellenan con **0** (asumiendo "Sin Historial").
    * Las variables categóricas (ej., EDUCATION) se rellenan con **'UNKNOWN'**.
    * **Normalización:** Las 10 variables categóricas se convierten a valores numéricos discretos mediante **Label Encoding (StringIndexer)**.
2.  **Feature Engineering:** Creación de las 7 dimensiones de valor del cliente:
    * **Métricas RFMI:** Recencia (`DAYS SINCE LAST_TXN`), Frecuencia (`FREQUENCY_COUNT`), e Intensidad (`INTENSITY_AVG_SPEND`).
    * **Riesgo Operativo:** Cálculo del `PAYMENT FIDELITY RATIO`.
    * **Targets ML:** Creación de variables binarias `Y` (`Y_RISK_CHURN`) y `T` (`TREATMENT_GROUP`) para modelado Causal (Uplift).

#### C. Carga (L)
Se realiza un **LEFT JOIN** de todos los DataFrames de métricas sobre el Master Base, resultando en la **Vista Consolidada** de 65 columnas (`Master_FINAL_CONSOLIDADO.parquet`).

---

## 3. 👥 Roles y Planificación Operativa

### 3.1. Roles del Equipo y Responsabilidades Clave

| Miembro | Rol Principal Asignado | Funciones Clave y Tareas Ejecutadas |
| :--- | :--- | :--- |
| **Jose Luis Pérez** | **Project Lead & Data Architect** | Liderazgo estratégico, gobernanza (GitHub, Docker), documentación inicial(README.md) y Modelado predictivo y Diseño final del Cuadro de Mando enT ableau. |
| **Claudia Torres** | **Data Engineer (Especialista ETL)** | Implementación del flujo ETL en PySpark, limpieza de datos, imputación estratégica y creación de la Curated Layer. |
| **Núria Mayoral** | **Data Analyst** | Desarrollo de la lógica de los 7 indicadores de comportamiento (RFMI, Riesgo, Anomalía, etc.) y la segmentación. |
| **Benjamín Carbonell** | **ML Specialist & Visualization Analyst** | Desarrollo y entrenamiento de los modelos predictivos. Implementación y construcción de *dashboards* en Tableau. |

### 3.2. Planificación Operativa (Roadmap Semanal)

El proyecto se desarrolló con un enfoque ágil en 3 semanas:

| Semana | Fases del Trabajo | Tareas Clave y Foco Principal | Responsable(s) Principal(es) |
| :--- | :--- | :--- | :--- |
| **Semana 1** | Fundación Técnica y ETL | Crear el entorno Docker, montar el repositorio en GitHub. Ingesta de datos, auditoría, imputación de nulos y ejecución del ETL de limpieza inicial. | Jose Luis, Claudia |
| **Semana 2** | Modelado y Análisis Avanzado | Calcular los 7 indicadores de comportamiento. Crear variables $Y/T$ y entrenar los modelos predictivos. | Núria, Benjamín, Jose Luis |
| **Semana 3** | Visualización y Documentación | Construir los 7 Cuadros de Mando en Tableau. Desarrollo del portal interactivo Streamlit. Redacción final de la documentación. | Benjamín, Jose Luis, Claudia, Núria |

#### Puntos de Control Clave (Milestones)

| Milestone | Resultado Obtenido |
| :--- | :--- |
| **M1: Entorno Operativo** | Entorno técnico configurado. |
| **M2: Master View Lista** | Capa Curada creada y validada. |
| **M3: Inteligencia Analítica** | Todos los 7 indicadores calculados y Modelos Predictivos entrenados. |
| **M4: Portal Interactivo** | Aplicación Streamlit desplegada y operativa. |
| **M5: Solución Completa** | Documentación y 6 Dashboards de Tableau finalizados. |

---

## 4. 🛠️ Guía de Instalación y Ejecución del Pipeline

### Control de Versiones
Utilizamos **GitHub** para el control de versiones, asegurando que el código sea reproducible, documentado, y que cada cambio sea trazable, cumpliendo con la Verificabilidad.

### Requisitos Previos

1.  **Git** (para clonar el repositorio).
2.  **Docker Desktop** (para el entorno reproducible).

### 4.1. Puesta en Marcha del Entorno

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/joseluis004/Big-Daddy.git
    cd Big-Daddy/
    ```

2.  **Navegar a la Carpeta de Configuración Docker:**
    ```bash
    cd docker_big_daddy/
    ```

3.  **Construir el Entorno (Instala PySpark, Python, librerías):**
    ```bash
    docker-compose build
    ```

4.  **Ejecutar el Contenedor (Inicia JupyterLab):**
    ```bash
    docker-compose up
    ```
    *Una vez iniciado, acceda al enlace `http://localhost:8888` (o el que se muestre en la terminal) en su navegador para entrar a JupyterLab.*

### 4.2. Ejecución del Pipeline Analítico

El proceso de ETL, Feature Engineering y Modelado se realiza mediante la ejecución secuencial de los Notebooks dentro del contenedor de JupyterLab.

1.  En la interfaz de JupyterLab, navegue a la carpeta **`notebooks/`**.
2.  **Paso 1: TRATAMIENTO DE DATOS**
    * Abrir y ejecutar completamente el notebook **`TRATAMIENTO DE DATOS.ipynb`**.
    * *Resultado:* Carga los datos, realiza la limpieza, ingeniería de features y genera múltiples archivos Parquet de resultados. Los modelos predictivos posteriormente ejecutarán el archivo **`Master_Model_FinPlus.parquet`** que se encuentra en `data/curated/`.
3.  **Paso 2: MODELOS PREDICTIVOS**
    * Abrir y ejecutar completamente el notebook **`MODELOS PREDICTIVOS.ipynb`**.
    * *Resultado:* Utiliza los datos procesados para entrenar y evaluar los modelos. **Importante:** Se entrenaron y evaluaron dos modelos para la predicción de churn: **XGBoost** y una **Red Neuronal**. Dado que el modelo XGBoost demostró un mejor desempeño en términos de precisión, fue seleccionado como el modelo final para la implementación en producción. Sin embargo, ambos modelos están disponibles en el repositorio.
### 4.3. Portal Interactivo FinPlus

Hemos desarrollado un portal interactivo utilizando **Streamlit** que permite cargar nuevos datos en formato CSV y obtener predicciones del modelo XGBoost en tiempo real.

**🔗 Acceso al Portal:**
- **URL:** [big-daddy-episjsskxsskkkuyuaq7iv.streamlit.app](https://big-daddy-episjsskxsskkkuyuaq7iv.streamlit.app)

**Funcionalidades del Portal:**
- **Carga de Datos:** Interfaz intuitiva para subir archivos CSV con datos de clientes.
- **Predicción en Tiempo Real:** El modelo XGBoost entrenado realiza predicciones de churn score inmediatamente.
- **Visualización de Resultados:** Muestra las probabilidades de abandono para cada cliente.
- **Descarga de Resultados:** Permite exportar las predicciones para su uso posterior.

---

## 5. 🔗 Entregables y Resultados

| Entregable | Contenido | Ubicación |
| :--- | :--- | :--- |
| **Documentación** | Propuesta Inicial, Fundamentos y Diagrama de Arquitectura. | `docs/` |
| **Código Fuente** | Repositorio completo (commits y PRs). | [GitHub: Big-Daddy](https://github.com/joseluis004/Big-Daddy) |
| **Código ETL** | Limpieza y Feature Engineering con PySpark. | `notebooks/TRATAMIENTO DE DATOS.ipynb` |
| **Código Modelado** | Xgboost, Red neuronal. | `notebooks/MODELOS PREDICTIVOS.ipynb` |
| **Portal Interactivo** | Aplicación Streamlit para predicciones en tiempo real. | [Portal FinPlus](https://big-daddy-episjsskxsskkkuyuaq7iv.streamlit.app) |
| **Visualización/Servicio** | 6 Dashboards Ejecutivos implementados en Tableau Public. | [Dashboard 1: Anomaly Class](https://public.tableau.com/app/profile/jose.luis.perez3391/viz/Big_Daddy_dashboards_1/DashboardANOMALYCLASS)<br>[Dashboard 2: Riesgo Abandono](https://public.tableau.com/app/profile/jose.luis.perez3391/viz/Big_Daddy_dashboards_2/DashboardRIESGOABANDONO)<br>[Dashboard 3: Barras de Actividad](https://public.tableau.com/app/profile/jose.luis.perez3391/viz/Big_Daddy_dashboards_3/DashboardBARRASDEACTIVIDAD)<br>[Dashboard 4: Barras Apiladas de Valor](https://public.tableau.com/app/profile/jose.luis.perez3391/viz/Big_Daddy_dashboards_4/DashboardBARRASAPILADASDEVALOR)<br>[Dashboard 5: Barras Agrupadas de Interacción](https://public.tableau.com/app/profile/jose.luis.perez3391/viz/Big_Daddy_dashboards_5/DashboardBARRASAGRUPADASDEINTERACCIN)<br>[Dashboard 6: Dispersión de Riesgo](https://public.tableau.com/app/profile/jose.luis.perez3391/viz/Big_Daddy_dashboards_6/DashboardDISPERSINDERIESGO) |

**¡Gracias por su tiempo! Esperamos convertirnos en su socio analítico 2025.**
