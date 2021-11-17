FROM ubuntu:18.04
RUN apt-get update
RUN apt -y install gnupg software-properties-common
RUN apt -y install python3.8


ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt

RUN apt -y install postgresql postgresql-client postgresql-contrib

# RUN apt install .tmp-build-deps \ 
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev


RUN wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
RUN chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
RUN apt-install-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main"
RUN apt -y install qgis qgis-plugin-grass



FROM postgres:12

LABEL maintainer="PostGIS Project - https://postgis.net"

ENV POSTGIS_MAJOR 3
ENV POSTGIS_VERSION 3.0.0+dfsg-2~exp1.pgdg100+1

RUN apt update \
    && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
    && apt install -y --no-install-recommends \
    postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
    postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts=$POSTGIS_VERSION \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./initdb-postgis.sh /docker-entrypoint-initdb.d/postgis.sh
COPY ./update-postgis.sh /usr/local/bin


RUN pip install -r /requirements.txt
RUN apt del .tmp-build-deps

RUN mkdir /app
COPY ./app /app
WORKDIR /app