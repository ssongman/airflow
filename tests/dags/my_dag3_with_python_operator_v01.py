from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta

default_args = {
    'owner': 'ssongman',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

# task instance
def greet(age, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name  = ti.xcom_pull(task_ids='get_name', key='last_name')
    print(f"Hello World! My name is {first_name} {last_name}, "
          f"and I am {age} years old!")
    
def get_name(ti):
    ti.xcom_push(key='first_name', value='yj')
    ti.xcom_push(key='last_name', value='song')

with DAG(
    dag_id="my_dag3_with_python_operator_v06",
    default_args=default_args,
    description="This is a my_dag3 that ssongman write",
    start_date=datetime(2022, 9, 16),
    schedule_interval="@daily"
) as dag:
    task1 = PythonOperator(
    	task_id="greet",
        python_callable=greet,
        op_kwargs={'age':20}    # keyword arguments
    )
    
    task2 = PythonOperator(
    	task_id="get_name",
        python_callable=get_name
    )
    
    task2 >> task1
