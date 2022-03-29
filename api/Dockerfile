FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install Flask && pip3 install requests && pip3 install scikit-learn
EXPOSE 5000
ADD app.py /data/app.py
WORKDIR /data/
CMD python3 app.py
