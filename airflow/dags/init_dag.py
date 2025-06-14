from airflow import DAG;
from datetime import datetime;

with DAG('init_dag', start_date=datetime(2023,1,1)): 
    pass
