# Airflow Setting







# 1. airflow service 설명

- `airflow-scheduler` - The [scheduler](https://airflow.apache.org/docs/apache-airflow/stable/concepts/scheduler.html) monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
- `airflow-webserver` - The webserver is available at `http://localhost:8080`.
- `airflow-worker` - The worker that executes the tasks given by the scheduler.
- `airflow-init` - The initialization service.
- `postgres` - The database.
- `redis` - [The redis](https://redis.io/) - broker that forwards messages from scheduler to worker.





# 2. airflow install



## 1) helm install

### helm repo

```sh

$ helm repo add bitnami https://charts.bitnami.com/bitnami

$ helm search repo airflow
NAME            CHART VERSION   APP VERSION     DESCRIPTION
bitnami/airflow 13.1.4          2.3.4           Apache Airflow is a tool to express and execute...

$ helm fetch bitnami/airflow

```





### helm install

```sh

$ kubectl create ns airflow

$ helm -n airflow install my-aireflow bitnami/airflow \
    --set auth.username=song \
    --set auth.password=songpass \
    --set ldap.enabled=false \
    --set ingress.enabled=true \
    --set ingress.ingressClassName=traefik \
    --set ingress.hostname=airflow.211-253-28-14.nip.io \
    --debug --dry-run

    #--set git.dags.enabled=true
    #--set git.dags.repositories[0].repository=https://github.com/USERNAME/REPOSITORY
    #--set git.dags.repositories[0].name=REPO-IDENTIFIER
    #--set git.dags.repositories[0].branch=master


NAME: my-aireflow
LAST DEPLOYED: Sat Sep 17 07:39:18 2022
NAMESPACE: airflow
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
CHART NAME: airflow
CHART VERSION: 13.1.5
APP VERSION: 2.3.4

** Please be patient while the chart is being deployed **

Airflow can be accessed via port 8080 on the following DNS name from within your cluster:

    my-aireflow-airflow.airflow.svc.cluster.local

To connect to Airflow from outside the cluster, perform the following steps:

1. Get the Airflow URL and associate its hostname to your cluster external IP:

    export CLUSTER_IP=$(minikube ip) # On Minikube. Use: `kubectl cluster-info` on others K8s clusters
    echo "Airflow URL: http://airflow.211-253-28-14.nip.io"
    echo "$CLUSTER_IP  airflow.211-253-28-14.nip.io" | sudo tee -a /etc/hosts

2. Open a browser and access Airflow using the obtained URL.

3. Get your Airflow login credentials by running:

    export AIRFLOW_PASSWORD=$(kubectl get secret --namespace "airflow" my-aireflow-airflow -o jsonpath="{.data.airflow-password}" | base64 -d)
    echo User:     song
    echo Password: $AIRFLOW_PASSWORD





$ kubectl -n airflow get secret --namespace "airflow" my-aireflow-airflow -o jsonpath="{.data.airflow-password}" | base64 -d





```





### helm upgrade



```sh

$ helm -n airflow ls

$ helm -n airflow upgrade my-aireflow bitnami/airflow \
    --set auth.username=song \
    --set auth.password=songpass \
    --set ldap.enabled=false \
    --set ingress.enabled=true \
    --set ingress.ingressClassName=traefik \
    --set ingress.hostname=airflow.211-253-28-14.nip.io \
    --set git.dags.enabled=true
    --set git.dags.repositories[0].repository=https://github.com/USERNAME/REPOSITORY
    --set git.dags.repositories[0].name=REPO-IDENTIFIER
    --set git.dags.repositories[0].branch=master
    
    #--set airflow.cloneDagFilesFromGit.enabled=true 
    #--set airflow.cloneDagFilesFromGit.repository=REPOSITORY_URL  
    #--set airflow.cloneDagFilesFromGit.branch=master 
    #--set airflow.baseUrl=http://127.0.0.1:8080 


# git repository 주소 변경 - 20220919
$ helm -n airflow upgrade my-aireflow bitnami/airflow \
    --set auth.username=song \
    --set auth.password=songpass \
    --set ldap.enabled=false \
    --set ingress.enabled=true \
    --set ingress.ingressClassName="" \
    --set ingress.annotationsio/ingress.provider=traefik \
    --set ingress.hostname=airflow.211-253-28-14.nip.io \
    --set git.dags.enabled=true \
    --set git.dags.repositories[0].repository="https://github.com/ssongman/airflow.git" \
    --set git.dags.repositories[0].branch="main" \
    --set git.dags.repositories[0].name=my-dags \
    --set git.dags.repositories[0].path="tests/dags"
    

$ helm -n airflow ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
my-aireflow     airflow         6               2022-09-17 17:25:00.087948063 +0000 UTC deployed        airflow-13.1.5  2.3.4




```













### ingress 수정

KTCloud / k3s 환경일 경우  ingress.provider: "traefik" 로 수정해야 한다.

```yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.provider: "traefik"
...
spec:
  ingressClassName: traefik     <-- 삭제
```





## 2) docker-compose install

참고 링크 : https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html'



### Setting the right Airflow user

On **Linux**, the quick-start needs to know your host user id and needs to have group id set to `0`. Otherwise the files created in `dags`, `logs` and `plugins` will be created with `root` user. You have to make sure to configure them for the docker-compose:

```
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```





### Initialize the database

```
docker-compose up airflow-init
```



### Running Airflow

Now you can start all services:

```
docker-compose up
```



접속

```

http://localhost:8081

login 
user: airflow
password: airflow.


```







### clean up

```sh
$ docker-compose down --volumes --remove-orphans
$ docker-compose down --volumes --rmi all

rm -rf '<DIRECTORY>'

```











# 3. Git sync





## 1) Git 권한 부여

git 에서 read 권한이 필요한 경우 (예를들면 public 이 아닌 경우) 에 gitlab 에서 다양한 방법으로 권한을 부여 할 수 있다.



### (1) Personal Token 발급



- Gitlab 위치
  - User Setting > Access Tokens > Personal Access Tokens
  - 권한
    - Read Repo



- 발급된 Token 정보
  - gitlab : http://gitlab2.211-253-28-14.nip.io/
  - user : root
  - token

```
glpat-1RFMF4MrzVbw7tK35VsR
```



### (2) SSH 인증서



## 2) helm 설정파일 수정하기

앞서 적용한 --set 적용 파라메타들이 모두 적용하여 upgrade 해야 하니 values.yaml 이나 --set 내용을 잘 기록해 놓아야 한다.



- helm chart 설정파일의 git sync 부분을 수정

```
http://{내 githubid} : {내 access token} @ github.com / {내 githubid} / {github repository명}
```



```yaml

# Git sync
dags:
  persistence:
    # Enable persistent volume for storing dags
    enabled: false
    # Volume size for dags
    size: 1Gi
    # If using a custom storageClass, pass name here
    storageClassName:
    # access mode of the persistent volume
    accessMode: ReadWriteOnce
    ## the name of an existing PVC to use
    existingClaim:
    ## optional subpath for dag volume mount
    subPath: ~
  gitSync:
    enabled: true

    # git repo clone url
    # ssh examples ssh://git@github.com/apache/airflow.git
    # git@github.com:apache/airflow.git
    # https example: https://github.com/apache/airflow.git
    repo: "http://root:glpat-1RFMF4MrzVbw7tK35VsR@gitlab2.211-253-28-14.nip.io/song/airflow-test"
    branch: main
    rev: HEAD
    depth: 1
    # the number of consecutive failures allowed before aborting
    maxFailures: 0
    # subpath within the repo where dags are located
    # should be "" if dags are at repo root
    subPath: "tests/dags"
    # if your repo needs a user name password
    # you can load them to a k8s secret like the one below
    #   ---
    #   apiVersion: v1
    #   kind: Secret
    #   metadata:
    #     name: git-credentials
    #   data:
    #     GIT_SYNC_USERNAME: <base64_encoded_git_username>
    #     GIT_SYNC_PASSWORD: <base64_encoded_git_password>
    # and specify the name of the secret below
    
```



## 3) helm upgrade

```sh

$ helm -n airflow upgrade my-aireflow bitnami/airflow \
    --set auth.username=song \
    --set auth.password=songpass \
    --set ldap.enabled=false \
    --set ingress.enabled=true \
    --set ingress.ingressClassName="" \
    --set ingress.annotationsio/ingress.provider=traefik \
    --set ingress.hostname=airflow.211-253-28-14.nip.io \
    --set git.dags.enabled=true \
    --set git.dags.repositories[0].repository="http://gitlab2.211-253-28-14.nip.io/song/airflow-test.git" \
    --set git.dags.repositories[0].branch="main" \
    --set git.dags.repositories[0].name=my-dags \
    --set git.dags.repositories[0].path="tests/dags"


# git repository 주소 변경 - 20220919
$ helm -n airflow upgrade my-aireflow bitnami/airflow \
    --set auth.username=song \
    --set auth.password=songpass \
    --set ldap.enabled=false \
    --set ingress.enabled=true \
    --set ingress.ingressClassName="" \
    --set ingress.annotationsio/ingress.provider=traefik \
    --set ingress.hostname=airflow.211-253-28-14.nip.io \
    --set git.dags.enabled=true \
    --set git.dags.repositories[0].repository="https://github.com/ssongman/airflow.git" \
    --set git.dags.repositories[0].branch="main" \
    --set git.dags.repositories[0].name=my-dags \
    --set git.dags.repositories[0].path="tests/dags"


$ helm -n airflow ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
my-aireflow     airflow         6               2022-09-17 17:25:00.087948063 +0000 UTC deployed        airflow-13.1.5  2.3.4


```





# 4. kubernetes pod operator

- 작업을 병렬화

- 종속성에 따라 적절하게 예약

- 필요할 때 데이터를 기록적으로 재 처리 가능
- Kubernetes cronjob과 유사하나 DAG으로 표현할 수 있어 데이터 처리 과정이나 동작 관리에 대해서 cronjob의 기능보다 효율적으로 관리 할 수 있음



## 1) 권한설정

airflow namespace 의 default sa 가 다른 namespace 의 pod 를 관리할 권한이 있어야 한다.



- 충분한 권한 부여(cluster-admin)

```yaml

$ cat > 11.airflow_clusterrole.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: airflow-rolebinding
  namespace: song
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: default
  namespace: airflow
---



$ kai create -f 11.airflow_clusterrole.yaml
```





- 필요한 권한만 부여

```yaml

cat > 12.service_role.yaml
---
# custom-role-binding.yaml
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: airflow-role
  namespace: song
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - create
  - get
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: airflow-rolebinding
  namespace: song
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: airflow-role
subjects:
- kind: ServiceAccount
  name: airflow
  namespace: airflow
```









## 2) 



참고링크 : https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-2/



```python
```









## 3) sample dag

### (1) kubernetes_pod



- python_kubernetes.py

```python
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

```



### (2) arguments

- sample1

```python

pyspark_submit_sample = KubernetesPodOperator(
    task_id='pyspark_submit_sample',
    name='pyspark_submit_sample',
    namespace='airflow',
    image='spark_client_1:1.0',
    arguments=["pyspark","pyspark_sample.py"],
    hostnetwork=True,
    in_cluster=True,
    is_delete_operator_pod=True,
    startup_timeout_seconds=300,
    execution_timeout=timedelta(minutes=120),
    retries=2,
    retry_delay=timedelta(minutes=2),
    image_pull_policy='IfNotPresent',
    service_account_name='airflow',
    on_retry_callback=SlackTool.make_handler(slack_channel,
                                             color='warning',
                                             message="Retry Task"),
    dag=dag
)
```



- sample2

```python

    quay_k8s = KubernetesPodOperator(
        namespace='default',
        image='quay.io/apache/bash',
        image_pull_secrets=[k8s.V1LocalObjectReference('testquay')],
        cmds=["bash", "-cx"],
        arguments=["echo", "10", "echo pwd"],
        labels={"foo": "bar"},
        name="airflow-private-image-pod",
        is_delete_operator_pod=True,
        in_cluster=True,
        task_id="task-two",
        get_logs=True,
    )
    
```











# 13. Dag



> 참조링크 : https://www.youtube.com/watch?v=K9AnJ9_ZAXE

아주유용함



## 1) Dag Define 순서

1) Import Modules
2) Define default arguments
3) Instantiate the Dag
4) Define tasks
5) Define dependencies



## 2) DAG



```python
from airflow import DAG

from datetime import datetime

with DAG("my_dag", start_date=datetime(2022.09.01),
    schedule_interval="@daily", catchup=False) as dag:
    
    training_model_A = PythonOperator(
    
    )
    
```





## 9) sample dag

### (1) dag_1.py

```python
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from random import randint
from datetime import datetime

def _choose_best_model(ti):
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    best_accuracy = max(accuracies)
    if (best_accuracy > 8):
        return 'accurate'
    return 'inaccurate'


def _training_model():
    return randint(1, 10)

with DAG("my_dag", start_date=datetime(2021, 1, 1),
    schedule_interval="@daily", catchup=False) as dag:

        training_model_A = PythonOperator(
            task_id="training_model_A",
            python_callable=_training_model
        )

        training_model_B = PythonOperator(
            task_id="training_model_B",
            python_callable=_training_model
        )

        training_model_C = PythonOperator(
            task_id="training_model_C",
            python_callable=_training_model
        )

        choose_best_model = BranchPythonOperator(
            task_id="choose_best_model",
            python_callable=_choose_best_model
        )

        accurate = BashOperator(
            task_id="accurate",
            bash_command="echo 'accurate'"
        )

        inaccurate = BashOperator(
            task_id="inaccurate",
            bash_command="echo 'inaccurate'"
        )

        [training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, inaccurate]
        
```



## 

### (2) dag_2.py

```python
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

```





### (3) python_operator

my_dag3_with_python_operator_v01.py





```python
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
    
# task instance
def get_name(ti):
    ti.xcom_push(key='first_name', value='yj')
    ti.xcom_push(key='last_name', value='song')

with DAG(
    dag_id="my_dag3_with_python_operator_v05",
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

```





# 14. Rest API list



## 1) 필요기능



### dag 등록

### dag enable

### toggle 끄고 켜기

### 외부에서 API Call 로 특정 dag 실행하기



## 2) rest API 사용설정



### (1) ㄱ

기본적으로 API 를 사용할 수 없다. 아래와 같이 변경작업이 필요하다.







```
# auth_backend = airflow.api.auth.backend.deny_all
auth_backend = airflow.api.auth.backend.basic_auth

$ curl -X GET http://airflow.211-253-28-14.nip.io/api/v1/dags \
    -H username:password
    
```









# 99. 해야할일

- keyCloak 연동

- API 목록검증
- gitlab 연동
