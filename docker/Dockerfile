# Usar una imagen base de Python con Debian
FROM python:3.10-slim

# Instalar Java Runtime Environment (JRE) - CRÍTICO para Spark
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless wget && \
    apt-get clean;

# Variables de entorno para Spark
# Se instala PySpark a través de requirements.txt, pero Spark necesita esta configuración.
ENV SPARK_VERSION=3.5.0
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$PATH:$SPARK_HOME/bin

# Descargar y configurar Apache Spark (es necesario incluso si usamos PySpark)
RUN wget -qO- "https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz" | tar -xz -C /opt/
RUN ln -s /opt/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION $SPARK_HOME

# Copiar el archivo de dependencias
COPY requirements.txt /tmp/

# Instalar PySpark y otras librerías
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    pip install jupyterlab

# Directorio de trabajo y exposición de puerto
WORKDIR /app
EXPOSE 8888

# Comando para iniciar JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.token=''", "--ServerApp.password=''"]