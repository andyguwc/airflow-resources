##################################################
# Airflow Benefits
##################################################

'''
Issues with Naive Cron Scripts
'''

# Failure handling
# Monitoring 
# Dependency (upstream data missing, execution dependency)
# Scalability - centrazlied 
# Deployment
# Process historic data - backfill/rerun historical data 

'''
Airflow Benefits
'''
# Framework for define tasks and dependencies in python
# Execute,schedule,distribute tasks across worker nodes


# Handle dependencies
# View of present/past runs
# Extensible
# UI
# Interact well with database 
# Ease of deployment of workflow changes 




##################################################
# DAG / Operator / Task
##################################################

# Concepts https://airflow.apache.org/concepts.html#concepts-operators

# DAG: a description of the order in which work should take place
# Operator: a class that acts as a template for carrying out some work
# Task: a parameterized instance of an operator
# Task Instance: a task that 1) has been assigned to a DAG and 2) has a state associated with a specific run of the DAG

'''
DAG Components
'''

# Python script specifying the DAG's structure as code 
# DAGs do not perform actual tasks, just scheduling and organizing them

# Step 1: Importing Modules 
from datetime import timedelta 

import airflow 
from airflow import DAG 
from airflow.operators.bash_operator import BashOperator 


# Step 2: Default Arguments
# dictionary containing all arguments applying to all tasks in the workflow
default_args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'end_date': datetime(2018,12,30),
    'dependds_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False, 
    'email_on_retry': False,
    'retries':1,
    'retry_delay: timedelta(minutes=5)',
}   


# Step 3: Instantiate a DAG
# give the DAG name, configure the schedule, and set the DAG settings 
dag = DAG(
    'tutorial',
    default_args = default_args,
    description='A simple tutorial DAG',
    # continue to run DAG every day
    schedule_interval=timedelta(day=1),
)


# Step 4: Tasks 
t1 = BashOperator(
    task_id = 'print_date',
    bash_command='date',
    dag=dag,
)


# Step 5: Set up Dependencies 
# Set the dependencies or the order which the tasks should be executed in 
t1.set_downstream(t2) # t2 is downstream of t1, that is t2 depends on t1 
t1.set_downstream([t2,t3])
t1>>[t2,t3]
t3.set_upstream(t1)

# DAGs comprise Tasks which are instantiations of various Operators, organized in some dependent order
# Taks typically don't communicate with each other 
import airflow.models as af_models
import datetime 

DAG = af_models.DAG(
    dag_id = 'my_dag',
    start_date=datetime(2018,1,1),
    schedule_interval='0 10 ***'
)

first_task = PythonOperator(
    task_id = 'my_first_task',
    python_callable=module.some_func,
    dag = DAG
)

second_task = PythonOperator(
    task_id = 'my_second_task',
    python_callable=module.another_func,
    dag = DAG
)

second_task.set_upstream(first_task)




'''
Task Arguments
'''
# Once an operator is instantiated, it is referred to as a "task". Instantiating a task requires a task_id and DAG container
# DAG container sets the execution context and organizes the tasks

# retries 
# email_on_failure
# on_failure_callback
# pool 
# queue
# execution_timeout
# trigger_rule 



'''
Types of Operators
'''

# An operator describes a single task in a workflow. Operators are usually (but not always) atomic, meaning they can stand on their own and don’t need to share resources with any other operators. 
# The DAG will make sure that operators run in the correct certain order; other than those dependencies, operators generally run independently. In fact, they may run on two completely different machines.


# Sensor
# a type of operator that will keep running until a certain criteria is met 
# example: waiting for certain time, external file or source 

# Operator 
# trigger a certain action (run a bash, execute a python function, or execute a hive query)
# BashOperator: executes a bash command
# PythonOperator: calls a python function 

# Transfer
# Move data from one location to another 
# S3ToRedshiftTransfer 


# Can extend from Base operators 


##################################################
# Schedules & Triggers 
##################################################

# https://airflow.apache.org/scheduler.html

# The first DAG Run is created based on the minimum start_date for the tasks in your DAG.
# Subsequent DAG Runs are created by the scheduler process, based on your DAG’s schedule_interval, sequentially.
# When clearing a set of tasks’ state in hope of getting them to re-run, it is important to keep in mind the DAG Run’s state too as it defines whether the scheduler should look into triggering tasks for that run.

'''
Alerts & SLAs
'''
# Airflow has built in task retry 

# can notify with alerts and SLAs

'''
DagRuns and TaskInstances
'''
# A DagRun is a DAG with a sepcific execution time 
# TaskInstances are the tasks belonging to DagRuns 

# A task instance represents a specific run of a task and is characterized as the combination of a dag, a task, and a point in time. 
# Task instances also have an indicative state, which could be “running”, “success”, “failed”, “skipped”, “up for retry”, etc.



##################################################
# Templatizing Code 
##################################################



'''
Variables
'''
# Variables are key values stores in Airflow's metadata 

# Store static values like 
#  - config variables 
#  - a config file 
#  - a list of tables 
#  - list of IDs to dynamically generate tasks from 


##################################################
# Airflow Architecture
##################################################

# Airflow’s Architecture
# https://medium.com/@dustinstansbury/understanding-apache-airflows-key-concepts-a96efed52b1a

# Airflow’s operation is built atop a Metadata Database which stores the state of tasks and workflows (i.e. DAGs). 
# The Scheduler and Executor send tasks to a queue for Worker processes to perform. 
# The Webserver runs (often-times running on the same machine as the Scheduler) and communicates with the database to render task state and Task Execution Logs in the Web UI. 


# At its core, Airflow is simply a queuing system built on top of a metadata database. The database stores the state of queued tasks and a scheduler uses these states to prioritize how other tasks are added to the queue. 
# This functionality is orchestrated by four primary components (refer to the Left Subpanel of Figure 3.2):

# 1. Metadata Database: this database stores information regarding the state of tasks. Database updates are performed using an abstraction layer implemented in SQLAlchemy. This abstraction layer cleanly separates the function of the remaining components of Airflow from the database.

# 2. Scheduler: The Scheduler is a process that uses DAG definitions in conjunction with the state of tasks in the metadata database to decide which tasks need to be executed, as well as their execution priority. The Scheduler is generally run as a service.

# 3. Executor: The Executor is a message queuing process that is tightly bound to the Scheduler and determines the worker processes that actually execute each scheduled task. There are different types of Executors, each of which uses a specific class of worker processes to execute tasks. 
# For example, the LocalExecutor executes tasks with parallel processes that run on the same machine as the Scheduler process. Other Executors, like the CeleryExecutor execute tasks using worker processes that exist on a separate cluster of worker machines.

# 4. Workers: These are the processes that actually execute the logic of tasks, and are determined by the Executor being used.


# Web UI
# 1. Webserver: This process runs a simple Flask application which reads the state of all tasks from the metadata database and renders these states for the Web UI.
# 2. Web UI: This component allows a client-side user to view and edit the state of tasks in the metadata database. Because of the coupling between the Scheduler and the database, the Web UI allows users to manipulate the behavior of the scheduler.
# 3. Execution Logs: These logs are written by the worker processes and stored either on disk or a remote file store (e.g. GCS or S3). The Webserver accesses the logs and makes them available to the Web UI.



##################################################
# Development & Deployment Process
##################################################
'''
Best Practices
'''

# Optimizely 
# https://medium.com/engineers-optimizely/airflow-at-optimizely-38c6d17a25f5

# Commit code, merge to master 
# Jenkins job listns on push to master, tar balls master branch code to s3
# DAG on airflow to sync code from s3 to airflow host 

# Deploying DAGs
# Have a dev/prod airflow cluster 
# Deploy using a bootstrap script/docker 
# Leverage airflow variables to differentiate between dev and prod


# At Optimizely, we currently run a Airflow v1.8.2 setup with the webserver, scheduler and 16 workers managed by Celery running on single AWS EC2 instance. 
# This simple and modest setup has served us well: we currently manage ~100 workflows. We use monit to automatically manage and monitor any of the worker, scheduler or webserver processes.
# We also have a Docker cleanup workflow to periodically clean up orphaned or unused Docker resources on the instance. Scaling the cluster horizontally to a multi-node setup is well-documented and is something we may do in future.
# We have a separate EC2 Airflow node for our development and our production environment, which we differentiate by the value of a custom Airflow Variable called environment, that tweaks the schedule of the DAGs to be different for development and production environments, 
# since we typically just want to test the DAG workflow execution in the development Airflow node and don’t want the DAGs to run on the same schedule on the development environment as it does on Production.


# We have 3 repositories currently contributing DAGs to our Airflow system, with each repository owned by a different team. Each team is free to deploy their DAGs with whatever strategy they choose. Typically, whenever an engineer/analyst commits changes to a DAG, and merges the changes to master development branch of their repo, our CI (Continuous Integration) process creates an artifact of the repository at the tip of master branch and pushes it to S3, which is then pulled by the respective team’s code_sync DAG on our Airflow server. Each repository deploys its DAGs to its own subfolder under $AIRFLOW_HOME/dags, which is where the scheduler scans for any DAGs.
# Since all metadata regarding DAG runs is persisted to a metadata store(MySQL database in our case), it becomes very easy to report on job performance statistics(using SQL), allowing for continuous improvement to existing workflows.

# Lyft
# https://eng.lyft.com/running-apache-airflow-at-lyft-6e53bb8fccff

# Quizlet 
# https://medium.com/tech-quizlet/going-with-the-flow-how-quizlet-uses-apache-airflow-to-execute-complex-data-processing-pipelines-1ca546f8cc68



'''
Setup with Docker 
'''
# Check http://localhost:8080/

# $ docker-compose up -d

# Displays log output
# $ docker-compose logs 

# List containers
# $ docker-compose ps 

# Stop containers
# $ docker-compose down


'''
Test
'''
## Other commands

# If you want to run airflow sub-commands, you can do so like this:

# - `docker-compose run --rm webserver airflow list_dags` - List dags
# - `docker-compose run --rm webserver airflow test [DAG_ID] [TASK_ID] [EXECUTION_DATE]` - Test specific task

# If you want to run/test python script, you can do so like this:
# - `docker-compose run --rm webserver python /usr/local/airflow/dags/[PYTHON-FILE].py` - Test python script


# Command Line Interface 
# airflow test DAG_ID TASK_ID EXECUTION_DATE. Allows the user to run a task in isolation, without affecting the metadata database, or being concerned about task dependencies. This command is great for testing basic behavior of custom Operator classes in isolation.
# airflow backfill DAG_ID TASK_ID -s START_DATE -e END_DATE. Performs backfills of historical data between START_DATE and END_DATE without the need to run the scheduler. This is great when you need to change some business logic of a currently-existing workflow and need to update historical data. (Note that backfills do not create DagRun entries in the database, as they are not run by the SchedulerJob class).
# airflow clear DAG_ID. Removes TaskInstance records in the metadata database for the DAG_ID. This can be useful when you’re iterating on the functionality of a workflow/DAG.
# airflow resetdb: though you generally do not want to run this command often, it can be very helpful if you ever need to create a “clean slate,” a situation that may arise when setting up Airflow initially (Note: this command only affects the database, and does not remove logs).

'''
Host on Cloud
'''



##################################################
# UI
##################################################
# Graph View

# Tree View 
#  - Click into the Log

# Details 
#  - Can see the default_args

