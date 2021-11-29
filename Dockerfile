FROM python:3.8-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc  \
    && apt-get clean

RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin  python3-gdal    

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt


RUN pip install -r requirements.txt

COPY . /app



# ENV PYTHONUNBUFFERED=1
# RUN mkdir /app
# COPY . /app

# WORKDIR /app
# # RUN apt-get -y update
# # RUN apt-get -y upgrade
# RUN apt-get update && \
#     apt-get install -y software-properties-common && \
#     rm -rf /var/lib/apt/lists/*

# RUN add-apt-repository -y ppa:ubuntugis/ppa
# RUN apt-get remove libpq5
# RUN apt install libpq-dev gdal-bin libgdal-dev
# RUN pip install -r /app/requirements.txt

# COPY . ./app
# RUN apt-get install gdal-bin -y

# RUN add-apt-repository -y ppa:ubuntugis/ppa
# RUN apt-get -y update
# RUN apt-get -y upgrade

# ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
# ARG C_INCLUDE_PATH=/usr/include/gdal
# RUN pip install GDAL

# ENV PYTHONUNBUFFERED 1
# COPY ./requirements.txt /requirements.txt

# RUN apt install .tmp-build-deps \ 
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

# RUN apt-get -y install wget
# RUN wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
# RUN chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
# RUN add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main"
# RUN apt-get update
# RUN apt -y install qgis qgis-plugin-grass 


# RUN pip install -r /requirements.txt
# RUN apt del .tmp-build-deps

# RUN mkdir ./app
# COPY ./app ./app
# WORKDIR ./app