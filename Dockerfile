# Use uma imagem base com Python 3
FROM python:3.9-slim

# Atualizando o sistema e instalando wget e libcairo2
RUN apt-get update && \
    apt-get install -y wget libcairo2 libcairo2-dev && \
    apt-get clean

# Baixando e instalando o Mash
RUN wget https://github.com/marbl/Mash/releases/download/v2.3/mash-Linux64-v2.3.tar && \
    tar -xvf mash-Linux64-v2.3.tar && \
    mv mash-Linux64-v2.3/mash /usr/local/bin && \
    rm -rf mash-Linux64-v2.3 mash-Linux64-v2.3.tar && \
    apt-get remove --purge -y wget && \
    apt-get autoremove -y

# Copiando os arquivos gdt.py e newick_to_img.py para /usr/local/bin
COPY gdt.py /usr/local/bin/
COPY newick_to_img.py /usr/local/bin/

# Instalando pacotes Python necessários via pip
RUN pip install numpy scipy matplotlib biopython cairosvg

# Tornando os scripts executáveis
RUN chmod +x /usr/local/bin/gdt.py && \
    chmod +x /usr/local/bin/newick_to_img.py

# Definindo o diretório de trabalho
WORKDIR /data

