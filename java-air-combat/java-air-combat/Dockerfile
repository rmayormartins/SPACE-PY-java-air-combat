FROM python:3.9

# Instalar Java
RUN apt-get update && \
    apt-get install -y default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verificar instalação do Java
RUN java -version && javac -version

# Configurar diretório de trabalho
WORKDIR /code

# Copiar requirements e instalar dependências Python
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copiar código da aplicação
COPY . /code

# Expor porta
EXPOSE 7860

# Comando para executar a aplicação
CMD ["python", "app.py"]