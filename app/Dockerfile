FROM continuumio/miniconda3:4.8.2

ENV PATH /opt/conda/bin:$PATH

RUN apt-get update && apt-get install -y \
    libxrender-dev \
    curl

# set application location
RUN mkdir -p /srv/game_api
RUN mkdir -p /srv/game_api/components
RUN mkdir -p /srv/game_api/test
WORKDIR /srv/game_api

# add application source code and install python packages
COPY ./__init__.py ./app.py ./game_api.py ./models.py ./requirements.txt /srv/game_api/
COPY ./components/. /srv/game_api/components/
COPY ./tests/. /srv/game_api/test/
RUN pip install -r /srv/game_api/requirements.txt