FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y
EXPOSE 8000
ADD main.py /test_doc/main.py
CMD python3 main.py