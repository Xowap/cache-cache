FROM xowap/trafficserver:latest

COPY etc/compress.config /etc/trafficserver
COPY etc/header_rewrite.config /etc/trafficserver
COPY etc/logging.yaml /etc/trafficserver
COPY etc/plugin.config /etc/trafficserver
COPY etc/records.config.yaml /etc/trafficserver
COPY etc/remap.tpl.config /etc/trafficserver

EXPOSE 9000
