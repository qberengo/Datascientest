# Image de l'API : Python officiel, version légère (fonctionne sur processeurs Intel/AMD et ARM)
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py bike.csv credentials.csv ./
EXPOSE 5000
CMD ["python", "app.py"]
