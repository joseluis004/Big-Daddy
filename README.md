# 🚀 FinPlus Analytics Challenge: De Datos a Decisiones Accionables

<p align="center">
  <img src="https://img.shields.io/badge/Tecnología-PySpark%2FDocker-blue" alt="PySpark Badge"/>
  <img src="https://img.shields.io/badge/Metodología-Medallion%20Architecture-informational" alt="Medallion Badge"/>
  <img src="https://img.shields.io/badge/Análisis-Churn%20Score%20%2F%20RFM-success" alt="Analysis Badge"/>
  <img src="https://img.shields.io/badge/Status-Completado-brightgreen" alt="Status Badge"/>
</p>

---

## 1. 💡 Resumen y Objetivo Estratégico

Este repositorio contiene la solución completa *end-to-end* desarrollada por **[NOMBRE DE SU EQUIPO / CONSULTORA]** para el "FinPlus Analytics Challenge".

Nuestro objetivo es transformar los datos crudos de clientes (demográficos, digitales y transaccionales) en una **inteligencia de negocio predictiva y accionable**.

### Objetivos Clave de la Solución:

| # | Objetivo FinPlus | Resultado de la Solución |
| :-: | :--- | :--- |
| **1** | Comprender Clientes | **Segmentación Avanzada (Clustering)** para crear perfiles 360°. |
| **2** | Detectar Riesgos | **Modelo Predictivo de Abandono (Churn Score)** asignado a cada cliente. |
| **3** | Oportunidades | **Features RFM** y métricas de propensión para impulsar el *cross-selling*. |
| **4** | Toma de Decisiones | **Dashboard Ejecutivo** (Entregable 5) con KPIs claros y narrativos. |

## 2. ⚙️ Arquitectura del Proyecto (Medallion Architecture)

El proyecto utiliza una arquitectura moderna de Big Data basada en capas de datos, garantizando **trazabilidad, calidad y rendimiento** con PySpark. 

[Image of Medallion data architecture diagram (Bronze, Silver, Gold layers)]


### 2.1. Estructura de Carpetas

| Carpeta | Contenido | Propósito |
| :--- | :--- | :--- |
| `data/` | `CLIENTS.csv`, `BEHAVIOURAL.csv` | Datos originales (Capa Bronce - Raw Data). |
| `docker/` | `Dockerfile`, `docker-compose.yml` | Configuración del entorno de PySpark y JupyterLab. |
| `notebooks/` | `01_EDA.ipynb`, `02_Modelado.ipynb` | Análisis exploratorio y prototipado. |
| `src/` | `main_pipeline.py`, `feature_engineering.py` | **Código de Producción** (ETL, Limpieza y Funciones). |
| `docs/` | `Propuesta_Inicial.pdf`, `Diagrama_Arquitectura.pdf` | Documentación formal del proyecto. |
| `dashboards/` | Capturas/Enlace del Dashboard | Visualización de los resultados. |

### 2.2. Roles del Equipo

| Miembro | Rol | Responsabilidad Principal |
| :--- | :--- | :--- |
| [Nombre 1] | **Project Lead (PL)** | Gestión de hitos, alineación de negocio y presentación de resultados. |
| [Nombre 2] | **Data Architect (DA)** | Diseño de arquitectura, entorno Docker y gobernanza de código (GitHub). |
| [Nombre 3] | **Data Engineer (DE)** | Desarrollo del pipeline ETL con PySpark (Limpieza y Features). |
| [Nombre 4] | **Data Scientist (DS)** | Análisis avanzado (Fase 4.6), KPIs y diseño del Dashboard Ejecutivo. |

---

## 3. 🛠️ Guía de Instalación y Ejecución del Pipeline

Para replicar el entorno y ejecutar todo el análisis (Entregables 4 y 6), siga estos sencillos pasos.

### Requisitos Previos

1.  **Git** (para clonar el repositorio).
2.  **Docker Desktop** (para el entorno reproducible).

### 3.1. Puesta en Marcha

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/](https://github.com/)[SuUsuario]/FinPlusAnalytics_TeamX.git
    cd FinPlusAnalytics_TeamX/
    ```

2.  **Navegar a la Carpeta Docker:**
    ```bash
    cd docker/
    ```

3.  **Construir el Entorno (Instala PySpark, Python, librerías):**
    ```bash
    docker-compose build
    ```

4.  **Ejecutar el Contenedor (Inicia JupyterLab):**
    ```bash
    docker-compose up
    ```
    *Una vez iniciado, acceda a `http://localhost:8888` en su navegador.*

### 3.2. Ejecución del Pipeline ETL y Análisis

Dentro de la terminal del contenedor o abriendo un Notebook de Jupyter, ejecute el script principal:

1.  **Detener el Servidor (Ctrl+C)** si está abierto.
2.  **Navegar a la Raíz del Proyecto:**
    ```bash
    cd ..
    ```
3.  **Ejecutar el Pipeline Maestro:** (Asumiendo que `main_pipeline.py` orquesta la limpieza, features y modelos).
    ```bash
    docker exec -it finplus_analytics_container spark-submit src/main_pipeline.py
    ```

    * **Resultado:** Este comando generará las tablas de la **Capa Oro** final y los datasets para el dashboard, completando el **Entregable 4 y 6**.

---

## 4. 🔗 Entregables y Resultados

| Entregable | Contenido | Ubicación |
| :--- | :--- | :--- |
| **Entregable 1 & 2** | Propuesta Inicial y Diagrama de Arquitectura. | `docs/` |
| **Entregable 3** | Evidencia de Commits y PRs (Revisar **Historial de GitHub**). | GitHub |
| **Entregable 4** | Código ETL (Limpieza y Features). | `src/` |
| **Entregable 5** | Dashboard Ejecutivo (Visualización). | [**LINK AL DASHBOARD** (Tableau/PowerBI)] |
| **Entregable 6 (Opcional)** | Código de Modelado (Clustering, Churn Score). | `src/` |

**¡Gracias por su tiempo! Esperamos convertirnos en su socio analítico 2025.**