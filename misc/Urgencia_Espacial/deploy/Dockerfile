# docker build -t urgencia_espacial .
# docker run -it -p 13332:5000 urgencia_espacial --restart always
# docker run -d -p 13332:5000 --name urgencia_espacial_container --restart always urgencia_espacial
FROM python:3.11

RUN apt-get update -y && apt-get install socat -y

WORKDIR /app
COPY app /app
RUN pip install reedsolo
RUN useradd -ms /bin/bash ctf
USER ctf

EXPOSE 5000

ENTRYPOINT ["socat", "TCP-LISTEN:5000,fork,reuseaddr", "EXEC:'python3 server.py',stderr"]