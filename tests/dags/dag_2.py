from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta

default_args = {
    'owner': 'ssongman',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id="my_dag2_v4",
    default_args=default_args,
    description="This is a my_dag2 that song write",
    start_date=datetime(2022, 9, 1),
    schedule_interval="@daily"
) as dag:
    
    task1 = BashOperator(
    	task_id='first_task',
        bash_command="echo hello world, this is the first task!"
    )
    
    task2 = BashOperator(
    	task_id='second_task',
        bash_command="echo hey, I am task2 and will be running after task1!"
    )
    
    task3 = BashOperator(
    	task_id='third_task',
        bash_command="echo hey, I am task3 and will be running after task1!"
    )
    
    # task dependency method 1
    #task1.set_downstream(task2)
    #task1.set_downstream(task3)

    # task dependency method 2
    #task1 >> task2
    #task1 >> task3

    # task dependency method 2
    task1 >> [task2, task3]
