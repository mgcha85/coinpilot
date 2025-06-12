FROM python:3.10-slim

WORKDIR /app
COPY collect.py .
RUN pip install python-binance requests

CMD ["python", "collect.py"]
