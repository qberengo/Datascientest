# Image des tests : un seul conteneur qui joue les 6 tests contre l'API
FROM python:3.13-slim
WORKDIR /tests
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["sh", "run_all.sh"]
