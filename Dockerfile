FROM python:3.8.12-bullseye
LABEL maintainer="geoyee@yeah.net"

RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  && apt-get install -y libgomp1 \
    ffmpeg libsm6 libxext6 \
    git \
    build-essential \
    gdal-bin libgdal-dev 
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal
RUN pip install --upgrade pip
RUN pip install GDAL==3.2.2 --no-cache-dir
RUN pip install -r requirements.txt

# Set environment variables
ENV FLASK_APP=run.py

# Run
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]