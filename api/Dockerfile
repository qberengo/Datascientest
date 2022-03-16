FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y
EXPOSE 8000
WORKDIR /test_doc/
ADD main.py /test_doc/main.py
VOLUME /test_doc
CMD python3 main.py