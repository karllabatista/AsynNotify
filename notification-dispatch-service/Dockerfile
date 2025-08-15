FROM python:3.10-alpine

WORKDIR /notification-dispatcher-service

# Se precisar compilar extensões nativas
RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# Ajusta PYTHONPATH
ENV PYTHONPATH=/notification-dispatcher-service/

CMD ["python3","src/main.py"]