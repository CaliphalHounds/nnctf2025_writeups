FROM python:3.9-slim

WORKDIR /app

COPY app .
COPY requirements.txt .

RUN useradd -ms /bin/bash ctf
USER ctf

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "server.py"]
