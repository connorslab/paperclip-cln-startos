ARG BASE_IMAGE=paperclip-cln:ark-20260930
FROM ${BASE_IMAGE}
USER root
RUN apt-get update && apt-get install -y --no-install-recommends python3-venv openssl && rm -rf /var/lib/apt/lists/*
COPY sideflash /opt/sideflash
COPY pyln-client /opt/pyln-client
RUN python3 -m venv /opt/sideflash/venv && /opt/sideflash/venv/bin/pip install /opt/pyln-client -r /opt/sideflash/requirements.txt && chmod +x /opt/sideflash/run
COPY runtime /opt/startos
ENTRYPOINT ["/usr/bin/tini","--","python3","/opt/startos/start.py"]
