FROM python:3.10.10-slim

ARG TARGETARCH

ENV api_id="your api id" \
    api_hash="your api hash" \
    phone="your phone number" \
    Proxy="false" \
    ProxyType="socks5" \
    ProxyTarget="host.docker.internal" \
    ProxyPort="1080"

WORKDIR /app

COPY entrypoint.sh requirements.txt jms.py cm.py libtdjson_${TARGETARCH}.so ./

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron && \
    echo "0 9 * * * cd /app && /usr/local/bin/python cm.py >> /app/cm.log 2>&1\n5 9 * * * cd /app && /usr/local/bin/python jms.py >> /app/jms.log 2>&1" >> /etc/cron.d/cronpy && \
    chmod 0644 /etc/cron.d/cronpy && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* && \
    mv libtdjson_${TARGETARCH}.so libtdjson.so && \
    crontab /etc/cron.d/cronpy

ENTRYPOINT ["sh", "entrypoint.sh"]
