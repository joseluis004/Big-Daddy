# 🚀 FinPlus Analytics Challenge: De Datos a Decisiones Accionables (Big-Daddy)

<p align="center">
  <img src="https://img.shields.io/badge/Tecnología-PySpark%2FDocker-blue" alt="PySpark Badge"/>
  <img src="https://img.shields.io/badge/Metodología-Layered%20Architecture-informational" alt="Layered Architecture Badge"/>
  <img src="https://img.shields.io/badge/Análisis-Churn%20Score%20%2F%20RFMI-success" alt="Analysis Badge"/>
  <img src="https://img.shields.io/badge/Status-Completado-brightgreen" alt="Status Badge"/>
</p>

---

## 1. 💡 Resumen y Objetivo Estratégico

[cite_start]Este repositorio contiene la solución completa *end-to-end* desarrollada por **Big-Daddy** para el "FinPlus Analytics Challenge"[cite: 5, 7]. [cite_start]El proyecto se enfoca en la implementación de una arquitectura de datos robusta usando Docker y PySpark para generar inteligencia de negocio avanzada[cite: 28, 79].

[cite_start]Nuestro objetivo es transformar los datos crudos de clientes (demográficos, digitales y transaccionales) en una **inteligencia de negocio predictiva y accionable**[cite: 67].

### Objetivos Clave de la Solución:

| # | Objetivo FinPlus | Resultado de la Solución |
| :-: | :--- | :--- |
| **1** | Comprender Clientes | **Segmentación Avanzada (Clustering)** para crear perfiles 360°. |
| **2** | Detectar Riesgos | [cite_start]**Modelo Predictivo de Abandono (Churn Score)** asignado a cada cliente[cite: 29]. |
| **3** | Oportunidades | [cite_start]**Features RFMI** y métricas de propensión para impulsar el *cross-selling*[cite: 52]. |
| **4** | Toma de Decisiones | [cite_start]**Dashboard Ejecutivo (Tableau)** con KPIs claros y narrativos[cite: 68]. |

---

## 2. ⚙️ Arquitectura y Diseño Técnico (Informe 2)

[cite_start]El diseño del proyecto utiliza un modelo de **Arquitectura por Capas (Layered Architecture)** [cite: 25] [cite_start]y se enfoca en el **Procesamiento por Lotes (Batch Processing)** [cite: 25][cite_start], priorizando la precisión para el análisis de comportamiento histórico (RFMI, Churn)[cite: 29].

### 2.1. Arquitectura de Datos y Motor



[Image of Layered Data Architecture]


* [cite_start]**Paradigma:** Arquitectura por Capas, enfoque en Batch Processing[cite: 25].
* [cite_start]**Motor Principal:** **Apache Spark / PySpark**[cite: 28]. [cite_start]Es esencial para manejar el Volumen y la Variedad de los datos transaccionales[cite: 28].
* [cite_start]**Almacenamiento Final:** **Master\_FINAL\_CONSOLIDADO.parquet** [cite: 59] [cite_start]en formato **Parquet**[cite: 62]. [cite_start]Este formato columnar optimiza la compresión y la velocidad de consulta en la capa de BI y Machine Learning[cite: 65].

### 2.2. Flujo ETL (Extracción, Transformación, Carga)

[cite_start]El flujo modular se implementa en PySpark dentro de la *Curated Layer*[cite: 32].



#### A. Extracción (E)
[cite_start]Se ingesta la información demográfica/contractual (`CLIENTS.csv`) y el comportamiento transaccional (`BEHAVIOURAL.parquet`) [cite: 34] [cite_start]usando DataFrames distribuidos de PySpark[cite: 35].

#### B. Transformación (T)
1.  **Limpieza y Normalización:**
    * [cite_start]**Imputación Estratégica:** Se rellenan variables de *scoring* o antigüedad (CAR AGE, JOB\_SENIORITY) con **-1** (valor sentinel)[cite: 41].
    * [cite_start]Las variables de historial de préstamo se rellenan con **0** (asumiendo "Sin Historial")[cite: 42].
    * [cite_start]Las variables categóricas (ej., EDUCATION) se rellenan con **'UNKNOWN'**[cite: 43].
    * [cite_start]**Normalización:** Las 10 variables categóricas se convierten a valores numéricos discretos mediante **Label Encoding (StringIndexer)**[cite: 44].
2.  [cite_start]**Feature Engineering:** Creación de las 7 dimensiones de valor del cliente[cite: 51]:
    * [cite_start]**Métricas RFMI:** Recencia (`DAYS SINCE LAST_TXN`), Frecuencia (`FREQUENCY_COUNT`), e Intensidad (`INTENSITY_AVG_SPEND`)[cite: 52].
    * [cite_start]**Riesgo Operativo:** Cálculo del `PAYMENT FIDELITY RATIO`[cite: 53].
    * [cite_start]**Targets ML:** Creación de variables binarias `Y` (`Y_RISK_CHURN`) y `T` (`TREATMENT_GROUP`) para modelado Causal (Uplift)[cite: 55].

#### C. Carga (L)
[cite_start]Se realiza un **LEFT JOIN** de todos los DataFrames de métricas [cite: 58] [cite_start]sobre el Master Base, resultando en la **Vista Consolidada** de 65 columnas (`Master_FINAL_CONSOLIDADO.parquet`)[cite: 59, 60].

---

## 3. 👥 Roles y Planificación Operativa

### 3.1. Roles del Equipo y Responsabilidades Clave

| Miembro | Rol Principal Asignado | Funciones Clave y Tareas Ejecutadas |
| :--- | :--- | :--- |
| **Jose Luis Pérez** | **Project Lead & Data Architect** | [cite_start]Liderazgo estratégico, gobernanza (GitHub, Docker) [cite: 75][cite_start], y diseño final del Cuadro de Mando en Tableau[cite: 75]. |
| **Claudia Torres** | **Data Engineer (Especialista ETL)** | [cite_start]Implementación del flujo ETL en PySpark, limpieza de datos, imputación estratégica y creación de la Curated Layer[cite: 75]. |
| **Núria Mayoral** | **Data Analyst** | [cite_start]Desarrollo de la lógica de los 7 indicadores de comportamiento (RFMI, Riesgo, Anomalía, etc.) y la segmentación[cite: 75]. |
| **Benjamín Carbonell** | **ML Specialist & Visualization Analyst** | [cite_start]Desarrollo y entrenamiento de los modelos predictivos[cite: 75]. [cite_start]Implementación y construcción de *dashboards* en Tableau[cite: 75]. |

### 3.2. Planificación Operativa (Roadmap Semanal)

[cite_start]El proyecto se desarrolló con un enfoque ágil en 3 semanas[cite: 77]:

| Semana | Fases del Trabajo | Tareas Clave y Foco Principal | Responsable(s) Principal(es) |
| :--- | :--- | :--- | :--- |
| **Semana 1** | Fundación Técnica y ETL | Crear el entorno Docker, montar el repositorio en GitHub. [cite_start]Ingesta de datos, auditoría, imputación de nulos y ejecución del ETL de limpieza inicial[cite: 79]. | [cite_start]Jose Luis, Claudia [cite: 79] |
| **Semana 2** | Modelado y Análisis Avanzado | Calcular los 7 indicadores de comportamiento. [cite_start]Crear variables $Y/T$ y entrenar los modelos predictivos[cite: 79]. | [cite_start]Núria, Benjamín, Jose Luis [cite: 79] |
| **Semana 3** | Visualización y Documentación | Construir los 7 Cuadros de Mando en Tableau. [cite_start]Redacción final de la documentación[cite: 79]. | [cite_start]Benjamín, Jose Luis, Claudia, Núria [cite: 79] |

#### Puntos de Control Clave (Milestones)

| Milestone | Resultado Obtenido |
| :--- | :--- |
| **M1: Entorno Operativo** | [cite_start]Entorno técnico configurado[cite: 87]. |
| **M2: Master View Lista** | [cite_start]Capa Curada creada y validada[cite: 87]. |
| **M3: Inteligencia Analítica** | [cite_start]Todos los 7 indicadores calculados y Modelos Predictivos entrenados[cite: 87]. |
| **M4: Solución Completa** | [cite_start]Documentación y 7 Dashboards de Tableau finalizados[cite: 87]. |

---

## 4. 🛠️ Guía de Instalación y Ejecución del Pipeline

### Control de Versiones
[cite_start]Utilizamos **GitHub** para el control de versiones, asegurando que el código sea reproducible, documentado, y que cada cambio sea trazable, cumpliendo con la Verificabilidad[cite: 89, 90].

### Requisitos Previos

1.  **Git** (para clonar el repositorio).
2.  **Docker Desktop** (para el entorno reproducible).

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
| **Visualización/Servicio** | [cite_start]Aplicación o Dashboard Ejecutivo (Implementado en Tableau)[cite: 68]. | `portal_app/` y [**LINK AL DASHBOARD** (Tableau/PowerBI)] |

**¡Gracias por su tiempo! Esperamos convertirnos en su socio analítico 2025.**