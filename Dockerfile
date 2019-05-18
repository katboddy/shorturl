FROM python:3.6

MAINTAINER Kat Boddy <kat@sparrowsonline.com>

#M copy application source code
COPY app /app
WORKDIR /app

RUN python setup.py develop
EXPOSE 5000

CMD python main.py
