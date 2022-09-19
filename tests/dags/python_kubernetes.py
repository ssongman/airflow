from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago

from airflow.operators.dummy_operator import DummyOperator
#from airflow.kubernetes.secret import Secret
#from airflow.kubernetes.pod import Resources

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import os

default_args = {
    'owner': 'ssongman',
    'depends_on_past': False,
    'email': ['ssongmantop@gmail.com'],
    'retriey': 1,
    'retry_delay': timedelta(minutes=5)    
}

with DAG(
    'python_kubernetes_workflow_v3',
    default_args=default_args,
    description='python_kubernetes_workflow',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['python_kubernetes_workflow'],
) as dag:
    start = DummyOperator(task_id="start")


    t1 = KubernetesPodOperator(
        namespace='song',
        image='python:3.7',
        #image_pull_policy = 'Never',
        cmds=["python","-c", "print('hello task 1 ..................')"],
        labels={"foo": "bar"},
        name="task-1",
        is_delete_operator_pod=True,
        in_cluster=False,
        service_account_name='airflow',
        task_id="task-1",
        #config_file=os.path.expanduser('~')+"/.kube/config",
        get_logs=True
    )

    t2 = KubernetesPodOperator(
        namespace='song',
        image='python:3.7',
        #image_pull_policy='Never',
        cmds=["python", "-c", "print('hello task 2 ..................')"],
        labels={"foo": "bar"},
        name="task-2",
        is_delete_operator_pod=True,
        in_cluster=False,
        service_account_name='airflow',
        task_id="task-2",
        #config_file=os.path.expanduser('~')+"/.kube/config",
        get_logs=True
    )


    start >> t1 >> t2
