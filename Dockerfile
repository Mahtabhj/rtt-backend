FROM node:12-alpine3.12 as build-stage
RUN apk add --no-cache python2 g++ make

ARG STATE=local

RUN mkdir /rtt-backend-admin
RUN mkdir /rtt-backend-admin/rttadmin
WORKDIR /rtt-backend-admin/rttadmin
COPY rtt/rttadmin /rtt-backend-admin/rttadmin
RUN npm install
RUN npm rebuild node-sass
RUN npm run build:$STATE

FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN mkdir /rtt-backend-app
RUN mkdir /rtt-backend-app/rtt
WORKDIR /rtt-backend-app/rtt
COPY requirements.txt gunicorn_start.sh /rtt-backend-app/rtt/
EXPOSE 8000
RUN pip install -r requirements.txt
COPY rtt /rtt-backend-app/rtt/
RUN mkdir -p /rtt-backend-app/rtt/rttadmin/build
COPY --from=build-stage /rtt-backend-admin/rttadmin/build /rtt-backend-app/rtt/rttadmin/build/
VOLUME /rtt-backend-app
ADD . /rtt-backend-app