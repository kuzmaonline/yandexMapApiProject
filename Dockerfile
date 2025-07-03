FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cron \
    rsyslog && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p logs static/data && \
    chmod +x /app/fetch_coordinates.py && \
    touch /var/log/cron.log && chmod 0666 /var/log/cron.log

COPY crontab /etc/cron.d/app-cron
RUN chmod 0644 /etc/cron.d/app-cron && \
    crontab /etc/cron.d/app-cron

RUN echo '#!/bin/sh\n\
service rsyslog start\n\
service cron start\n\
python /app/fetch_coordinates.py\n\
tail -f /var/log/cron.log /var/log/syslog' > /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"] 