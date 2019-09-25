# Airflow Intro 
Workflow Management tool

Airflow Advantages
- Retry
- Monitoring
- Dependencies (data dependencies and execution dependencies) 
- Scalability
- Deployment 
- Backfill historical data 


- Framework to define tasks & dependencies in python
- executing, scheduling, and distributing tasks across worker nodes
- View of runs, logging feature
- UI, possibility to define REST interface 
- Interact well with databases 

DAG
- Multiple tasks which can be executed independently
- Can click into the logs inside Airflow

Direct Acyclic Graph: no cycles and data in each node flows in only one direction
- Each node is a task
- Edges represent dependencies amongst tasks
- Data flow graphs

Operators
- DAGs do not perform any computation. Operators decide what actually gets done. 
- For example - bashoperator: usd to run bash command 
- Task: once an operator is instantiated, referred to as task

Categories of operators
- Sensors: keep running until a certain criteria is met 
- Operators: triggers a certaina action 
- Transfers: move data from one location to another 

Can extend base operators

Define task dependencies 
- use set upstream or set downstream operators
- DagRuns and TaskInstances


 Applications
- data warehousing: cleanse, organize, data quality check
- machine learning: automate machine learning workflows 
- growth analytics: compute metrics
- experimentation: compute A/B testing experimentation frameworks 


# Set up Airflow
https://github.com/tuanavu/airflow-tutorial/tree/v0.2

Managing all of the dependencies is difficult 
Therefore it's better to use docker 
Easy of deployment from testing to production environments 

Docker container
Isolated environment to run the application
Container is more lightweight than VM because it doesn't have Hypervisor

$ docker-compose up -d --build
Visit the following (if using docker machine)
http://192.168.99.100:8080/admin/

This immediately starts the postgress and web server 


# Host Airflow on Google Cloud
On-premise: too much devops work 

GCP
- infrastructure scalability
- security
- ease of use 
- operability & maintainability

Deployment
- manual deployment
- auto deployment - can set up continuous integration popeline to automatically deploy every time a merge request is done in the master branch 


# Writing first workflow 

https://medium.com/apply-data-science/airflow-tutorial-4-writing-your-first-pipeline-6ebcd0b7bbeb

A Dag file - python script with configuration

Step 1: Import Modules 
import python dependencies

```
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
```

Step 2: Set up Default Argument
Define default and DAG specific arguments 
start_date: run from a specific date 
depends on past: status of a previous date. The next one will be triggered if the first one is

```
default_args = {
    'owner': 'airflow',    
    'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(2018, 12, 30),
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

```

Step 3: Instantiate a DAG
Give the DAG name, configure the schedule, and set the DAG settings

```
dag = DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    # Continue to run DAG once per day
    schedule_interval=timedelta(days=1),
)
```

Step 4: Tasks
Layout all the tasks in the workflow

```
# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    dag=dag,
)

templated_command = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds, 7)}}"
    echo "{{ params.my_param }}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag,
)
```

Step 5: Set up Dependencies
Set up dependencies or the order of the tasks 
Set downstream and set upstream

```
# This means that t2 will depend on t1
# running successfully to run.
t1.set_downstream(t2)

# similar to above where t3 will depend on t1
t3.set_upstream(t1)
```

# Example Big Query Data Pipeline
https://github.com/tuanavu/airflow-tutorial/blob/v0.6/docs/bigquery_github_trends.md

Create big query project
Open and explore data in big query
To to the ipython notebook directory and docker-compose up
Go to docker port 8889 with the token which opens the notebook
Then fill in the project id and run the code to authenticate access 


# Airflow Variables

https://www.applydatascience.com/airflow/airflow-variables/


config variables
list of tables
list of IDs to generate tasks from 

Instead of storing lots of variables in DAG, better to store them inside a single variable inside JSON value 

Recommended way - can access delete and edit variables in the UI
dag_config = Variable.get("example_variables_config", deserialize_json=True)
var1 = dag_config["var1"]
var2 = dag_config["var2"]
var3 = dag_config["var3"]

start = DummyOperator(
    task_id="start",
    dag=dag
)

Get value, set value, etc.


get value of var1
docker-compose run --rm webserver airflow variables --get var1

set value of var4
docker-compose run --rm webserver airflow variables --set var4 value4]

import variable json file
docker-compose run --rm webserver airflow variables --import /usr/local/airflow/dags/config/example_variables.json
