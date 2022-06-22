FROM continuumio/miniconda3

WORKDIR /src/ogc-api-processes-fastapi

COPY environment.yml /src/ogc-api-processes-fastapi/

RUN conda install -c conda-forge gcc python=3.10 \
    && conda env update -n base -f environment.yml

COPY . /src/ogc-api-processes-fastapi

RUN pip install --no-deps -e .
