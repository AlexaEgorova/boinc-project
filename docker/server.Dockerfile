FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /home/server

COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel \
 && pip install --no-cache-dir -Ur requirements.txt

COPY . .

ENV WORKERS_PER_CORE=1

CMD uvicorn app:app --host 0.0.0.0 --port 8000 \
                    --log-config=log_config.yaml \
                    --forwarded-allow-ips="*"
