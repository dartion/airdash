#FROM python:3.7-alpine
FROM python:3.8.2-alpine

WORKDIR /app

COPY discreETLy/requirements.txt requirements.txt
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk add --update --no-cache mariadb-connector-c

RUN apk add --no-cache --virtual .build-deps gcc musl-dev gcc build-base libffi-dev
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && apk del build-dependencies
RUN apk add gcc python3-dev jpeg-dev zlib-dev
RUN apk add autoconf automake make gcc musl-dev perl bash zlib-dev bzip2-dev xz-dev curl-dev libressl-dev

RUN apk add python3-dev
RUN apk add postgresql-dev
RUN pip install -r requirements.txt
RUN apk del .build-deps

RUN mkdir /var/run/discreetly

COPY ./discreETLy .

EXPOSE 8000
CMD tail -f requirements.txt
CMD python wsgi.py runserver -h 0.0.0.0

#CMD ["sh", "-c", "SECRET_KEY=`cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1` gunicorn --worker-class sync --log-level DEBUG --reload -b 0.0.0.0:8000 --graceful-timeout 5 --workers 2 --access-logfile - 'dashboard.app:create_app()'"]
