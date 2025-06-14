FROM apache/airflow:2.8.1-python3.10

# 1. root 권한으로 pip 설치
USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. DAG 복사 (이건 airflow 유저로 해도 OK)
COPY dags/ /opt/airflow/dags/
