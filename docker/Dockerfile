FROM python:3.7-alpine
LABEL mantainer "Tomas Vukasovic <tomowl@pm.me>"

ADD . /coc
WORKDIR /coc
ENV PYTHONPATH /coc/coc
RUN apk update
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN echo docker/requirements.txt
RUN pip3 install -r docker/requirements.txt
