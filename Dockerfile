# Usamos una imagen ligera de Miniconda
FROM continuumio/miniconda3

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de entorno que creaste antes
COPY environment.yml .

# Creamos el entorno de Conda dentro del contenedor
RUN conda env create -f environment.yml

# Copiamos el resto de los archivos (main.py, etc.)
COPY . .

# Nos aseguramos de que el script use el entorno de Conda
SHELL ["conda", "run", "-n", "open_science_focas", "/bin/bash", "-c"]

# Comando para ejecutar el script al arrancar
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "open_science_focas", "python", "main.py"]