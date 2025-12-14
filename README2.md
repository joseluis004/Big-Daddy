# 🚀 FinPlus Analytics Challenge: De Datos a Decisiones Accionables (Big-Daddy)

<p align="center">
  <img src="https://img.shields.io/badge/Tecnología-PySpark%2FDocker-blue" alt="PySpark Badge"/>
  <img src="https://img.shields.io/badge/Metodología-Layered%20Architecture-informational" alt="Layered Architecture Badge"/>
  <img src="https://img.shields.io/badge/Análisis-Churn%20Score%20%2F%20RFMI-success" alt="Analysis Badge"/>
  <img src="https://img.shields.io/badge/Status-Completado-brightgreen" alt="Status Badge"/>
</p>

---

## 1. 💡 Resumen y Objetivo Estratégico

Este repositorio contiene la solución completa *end-to-end* desarrollada por **Big-Daddy** para el "FinPlus Analytics Challenge". El proyecto se enfoca en la implementación de una arquitectura de datos robusta usando Docker y PySpark para generar inteligencia de negocio avanzada.

Nuestro objetivo es transformar los datos crudos de clientes (demográficos, digitales y transaccionales) en una **inteligencia de negocio predictiva y accionable**.

### Objetivos Clave de la Solución:

| # | Objetivo FinPlus | Resultado de la Solución |
| :-: | :--- | :--- |
| **1** | Comprender Clientes | **Segmentación Avanzada (Clustering)** para crear perfiles 360°. |
| **2** | Detectar Riesgos | **Modelo Predictivo de Abandono (Churn Score)** asignado a cada cliente. |
| **3** | Oportunidades | **Features RFMI** y métricas de propensión para impulsar el *cross-selling*. |
| **4** | Toma de Decisiones | **Dashboard Ejecutivo (Tableau)** con KPIs claros y narrativos. |

---

## 2. ⚙️ Arquitectura y Diseño Técnico (Informe 2)

El diseño del proyecto utiliza un modelo de **Arquitectura por Capas (Layered Architecture)** y se enfoca en el **Procesamiento por Lotes (Batch Processing)**, priorizando la precisión para el análisis de comportamiento histórico (RFMI, Churn).

### 2.1. Arquitectura de Datos y Motor



[Image of Layered Data Architecture]


* **Paradigma:** Arquitectura por Capas, enfoque en Batch Processing.
* **Motor Principal:** **Apache Spark / PySpark**. Es esencial para manejar el Volumen y la Variedad de los datos transaccionales.
* **Almacenamiento Final:** **Master\_FINAL\_CONSOLIDADO.parquet** en formato **Parquet**. Este formato columnar optimiza la compresión y la velocidad de consulta en la capa de BI y Machine Learning.

### 2.2. Flujo ETL (Extracción, Transformación, Carga)

El flujo modular se implementa en PySpark dentro de la *Curated Layer*.

#### A. Extracción (E)
Se ingesta la información demográfica/contractual (`CLIENTS.csv`) y el comportamiento transaccional (`BEHAVIOURAL.parquet`) usando DataFrames distribuidos de PySpark.

#### B. Transformación (T)
1.  **Limpieza y Normalización:**
    * **Imputación Estratégica:** Se rellenan variables de *scoring* o antigüedad (CAR AGE, JOB\_SENIORITY) con **-1** (valor sentinel).
    * Las variables de historial de préstamo se rellenan con **0** (asumiendo "Sin Historial").
    * Las variables categóricas (ej., EDUCATION) se rellenan con **'UNKNOWN'**.
    * **Normalización:** Las 10 variables categóricas se convierten a valores numéricos discretos mediante **Label Encoding (StringIndexer)**.
2.  **Feature Engineering:** Creación de las 7 dimensiones de valor del cliente:
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
| **Jose Luis Pérez** | **Project Lead & Data Architect** | Liderazgo estratégico, gobernanza (GitHub, Docker), y diseño final del Cuadro de Mando en Tableau. |
| **Claudia Torres** | **Data Engineer (Especialista ETL)** | Implementación del flujo ETL en PySpark, limpieza de datos, imputación estratégica y creación de la Curated Layer. |
| **Núria Mayoral** | **Data Analyst** | Desarrollo de la lógica de los 7 indicadores de comportamiento (RFMI, Riesgo, Anomalía, etc.) y la segmentación. |
| **Benjamín Carbonell** | **ML Specialist & Visualization Analyst** | Desarrollo y entrenamiento de los modelos predictivos. Implementación y construcción de *dashboards* en Tableau. |

### 3.2. Planificación Operativa (Roadmap Semanal)

El proyecto se desarrolló con un enfoque ágil en 3 semanas:

| Semana | Fases del Trabajo | Tareas Clave y Foco Principal | Responsable(s) Principal(es) |
| :--- | :--- | :--- | :--- |
| **Semana 1** | Fundación Técnica y ETL | Crear el entorno Docker, montar el repositorio en GitHub. Ingesta de datos, auditoría, imputación de nulos y ejecución del ETL de limpieza inicial. | Jose Luis, Claudia |
| **Semana 2** | Modelado y Análisis Avanzado | Calcular los 7 indicadores de comportamiento. Crear variables $Y/T$ y entrenar los modelos predictivos. | Núria, Benjamín, Jose Luis |
| **Semana 3** | Visualización y Documentación | Construir los 7 Cuadros de Mando en Tableau. Redacción final de la documentación. | Benjamín, Jose Luis, Claudia, Núria |

#### Puntos de Control Clave (Milestones)

| Milestone | Resultado Obtenido |
| :--- | :--- |
| **M1: Entorno Operativo** | Entorno técnico configurado. |
| **M2: Master View Lista** | Capa Curada creada y validada. |
| **M3: Inteligencia Analítica** | Todos los 7 indicadores calculados y Modelos Predictivos entrenados. |
| **M4: Solución Completa** | Documentación y 7 Dashboards de Tableau finalizados. |

---

## 4. 🛠️ Guía de Instalación y Ejecución del Pipeline

### Control de Versiones
Utilizamos **GitHub** para el control de versiones, asegurando que el código sea reproducible, documentado, y que cada cambio sea trazable, cumpliendo con la Verificabilidad.

### Requisitos Previos

1.  **Git** (para clonar el repositorio).
2.  **Docker Desktop** (para el entorno reproducible).

### 4.1. Puesta en Marcha del Entorno

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/joseluis004/Big-Daddy.git](https://github.com/joseluis004/Big-Daddy.git)
    cd Big-Daddy/
    ```

2.  **Navegar a la Carpeta de Configuración Docker:**
    ```bash
    cd docker_big_daddy/
    ```

3.  **Construir el Entorno (Instala PySpark, Python, librerías):**
    ```bash
    docker-compose build
    ```

4.  **Ejecutar el Contenedor (Inicia JupyterLab):**
    ```bash
    docker-compose up
    ```
    *Una vez iniciado, acceda al enlace `http://localhost:8888` (o el que se muestre en la terminal) en su navegador para entrar a JupyterLab.*

### 4.2. Ejecución del Pipeline Analítico

El proceso de ETL, Feature Engineering y Modelado se realiza mediante la ejecución secuencial de los Notebooks dentro del contenedor de JupyterLab.

1.  En la interfaz de JupyterLab, navegue a la carpeta **`notebooks/`**.

2.  **Paso 1: TRATAMIENTO DE DATOS**
    * Abrir y ejecutar completamente el notebook **`TRATAMIENTO DE DATOS.ipynb`**.
    * *Resultado:* Carga los datos, realiza la limpieza, ingeniería de features y guarda los resultados en la Capa Silver/Gold.

3.  **Paso 2: MODELOS PREDICTIVOS**
    * Abrir y ejecutar completamente el notebook **`MODELOS PREDICTIVOS.ipynb`**.
    * *Resultado:* Utiliza los datos procesados para entrenar y evaluar los modelos (Clustering y Churn Score).

---

## 5. 🔗 Entregables y Resultados

| Entregable | Contenido | Ubicación |
| :--- | :--- | :--- |
| **Documentación** | Propuesta Inicial, Fundamentos y Diagrama de Arquitectura. | `docs/` |
| **Código Fuente** | Repositorio completo (commits y PRs). | [GitHub: Big-Daddy](https://github.com/joseluis004/Big-Daddy) |
| **Código ETL** | Limpieza y Feature Engineering con PySpark. | `notebooks/TRATAMIENTO DE DATOS.ipynb` |
| **Código Modelado** | Clustering, Churn Score. | `notebooks/MODELOS PREDICTIVOS.ipynb` |
| **Visualización/Servicio** | Aplicación o Dashboard Ejecutivo (Implementado en Tableau). | `portal_app/` y [**LINK AL DASHBOARD** (Tableau/PowerBI)] |

**¡Gracias por su tiempo! Esperamos convertirnos en su socio analítico 2025.**