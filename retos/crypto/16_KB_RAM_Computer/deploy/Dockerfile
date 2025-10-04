FROM python:3.11

RUN apt-get update -y && apt-get install socat -y

WORKDIR /app
COPY app .
RUN useradd -ms /bin/bash ctf
USER ctf
EXPOSE 5000

ENTRYPOINT ["socat", "TCP-LISTEN:5000,fork,reuseaddr", "EXEC:'python server.py',stderr"]