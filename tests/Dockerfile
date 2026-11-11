# Image des tests : un seul conteneur qui joue les 6 tests contre l'API
FROM python:3.13-slim
WORKDIR /tests
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Sécurité supplémentaire : retire les fins de ligne Windows (CRLF) si le dépôt a été cloné sous Windows
RUN sed -i 's/\r$//' run_all.sh
CMD ["sh", "run_all.sh"]
