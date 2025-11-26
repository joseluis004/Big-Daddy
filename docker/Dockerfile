FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Java (JRE) y dependencias de sistema (necesario para Spark)
RUN apt-get update && \
    apt-get install -y openjdk-17-jre default-libmysqlclient-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar el archivo de dependencias y las instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Variables de entorno para PySpark
ENV SPARK_HOME="/usr/local/lib/python3.10/site-packages/pyspark"
ENV PATH="$PATH:$SPARK_HOME/bin"

# Exponer el puerto de JupyterLab
EXPOSE 8888

# Comando para iniciar JupyterLab al ejecutar el contenedor
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser", "--NotebookApp.token=''"]