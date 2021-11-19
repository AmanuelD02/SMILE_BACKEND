FROM ubuntu:18.04
RUN apt-get update
RUN apt -y install gnupg software-properties-common
RUN apt -y install python3.6


ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt

# RUN apt install .tmp-build-deps \ 
#     gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

# RUN apt-get -y install wget
# RUN wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import
# RUN chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg
# RUN add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main"
# RUN apt-get update
# RUN apt -y install qgis qgis-plugin-grass 


RUN pip3 install -r /requirements.txt
RUN apt del .tmp-build-deps

# RUN mkdir ./app
# COPY ./app ./app
# WORKDIR ./app