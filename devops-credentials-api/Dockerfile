FROM quay-enterprise-quay-quay-enterprise.apps.ocppaz0.ar.bsch/santandertec/santander-tecnologia-docker-base-images-python-base:v3.8

USER root

RUN update-crypto-policies --set LEGACY

USER 1001

COPY . .

RUN pip install -r requirements.txt

ENV PORT 8080
EXPOSE $PORT

CMD [ "python", "run.py" ]
