FROM python:3.10.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update \
    && apt upgrade -y \
    && apt install -y python3-pip \
                      python3-cffi \
                      python3-brotli \
                      libpango-1.0-0 \
                      libpangoft2-1.0-0 \
    && apt clean


WORKDIR /www/vr_lan

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
