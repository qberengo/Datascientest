FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install fastapi && pip3 install requests
EXPOSE 8000
ADD main.py /data/main.py
WORKDIR /data/
CMD python3 main.py
