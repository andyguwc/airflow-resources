## Summary 

Using ECR and ECS (Fargate) to Deploy a Simple Flask Application

1. Setup 

- Use virtualenv and virtualenvwrapper 
$ cd /Users/tianyougu/dev/
$ mkproject <example_project>
$ workon <example_project>
add path to virtualenv to make sure absolute path imports work
(optional) make sure environment variables work 
$ nano $VIRTUAL_ENV/bin/postactivate

- Pip install and generate requirements.txt
$ pip3 freeze > requirements.txt

2. Make sure the app runs ok locally 

3. Add Dockerfile 

- Dockerfile

FROM python:3.7-stretch

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . . 

ENTRYPOINT [ "python3" ]
CMD [ "run.py" ]


- Make sure docker file runs ok 
$ docker build -t <image-name> . 

$ docker run -p 8080:8080 -t <image-name>

- Note
    - because I'm using docker toolbox $ eval $(docker-machine env default)
    - And my localhost is http://192.168.99.100:8080/
    - alpine versions has issues with pip so just use stretch 

4. (optional) Add Docker-Compose

- docker-compse.yaml

version: '3'
services:
  model:
    build: .
    env_file: .env
    command: python3 app/main.py
    volumes:
      - .:/usr/local/app
    # ports:
    #   - "8000:8000"
    # environment:
    #   - TWS_HOST=${TWS_HOST}


- (optional) Add Makefile

Makefile 

build:
	@docker build . --rm
	
start:
	@docker-compose up -d

cli:
	@docker-compose run --rm model bash

5. AWS CLI - Push Docker Image to ECR
AWS CLI Configure (authenticate) - make sure use an admin role not the root user 
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

Authenticate Build Tag Push 
https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_AWSCLI.html


6. Configure ECS 

Go to https://console.aws.amazon.com/ecs/home?region=us-west-2#/getStarted and create custom app 
- basically configure task definition and configure network 
- note to setup port mapping and (optional) add load balancers
- note the vpc and subnets are automatically created 
- note it's best to create multiple tasks 

Under tasks find the Public IP and visit the port from that IP

Notes on First Run 
https://aws.amazon.com/getting-started/tutorials/deploy-docker-containers/

Notes on Task Definitions
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-task-definition.html


Followup 
- Figure out env variables
- Where to find logs 
- How to deploy multiple containers
- VPC and Security Groups what if not automatic

## Best Resources
Full Tutorial on End to End Deployment
https://www.learnaws.org/2018/02/06/Introduction-AWS-Fargate/

https://towardsdatascience.com/how-to-deploy-a-docker-container-python-on-amazon-ecs-using-amazon-ecr-9c52922b738f

https://codeburst.io/a-complete-guide-to-deploying-your-web-app-to-amazon-web-service-2854ff6bc399

https://aws.amazon.com/getting-started/tutorials/deploy-docker-containers/

Docker
https://towardsdatascience.com/how-docker-can-help-you-become-a-more-effective-data-scientist-7fc048ef91d5


## Virtual Env 

virtualenvwrapper
https://docs.python-guide.org/dev/virtualenvs/

add paths to virtualenv
https://stackoverflow.com/questions/10738919/how-do-i-add-a-path-to-pythonpath-in-virtualenv

adding env variables in virtualenv 
https://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv




## Docker Compose for Python 

https://blog.codeship.com/using-docker-compose-for-python-development/

Example simple Dockerfile and docker-compose.yaml 
https://github.com/jamesmawm/High-Frequency-Trading-Model-with-IB

Linux Alpine for Python Pandas
https://github.com/docker-library/python/issues/381

Docker and Docker Compose env variables 
https://docs.docker.com/compose/environment-variables/

Good Docker Curriculum 
https://docker-curriculum.com/


Docler Logs
docker logs -f <CONTAINER>

https://docs.docker.com/config/containers/logging/


## Deploying to AWS

Install AWS Cli in Virtual Environment 
https://docs.aws.amazon.com/cli/latest/userguide/install-virtualenv.html

AWS Cli Configure 
Make sure to create IAM roles
https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

AWS Cli for AWS Fargate
https://docs.aws.amazon.com/AmazonECS/latest/userguide/ECS_AWSCLI_Fargate.html#AWSCLI_register_task_definition

Another Full Tutorial
https://www.learnaws.org/2018/02/06/Introduction-AWS-Fargate/

Full Tutorial 
https://aws.amazon.com/getting-started/projects/build-modern-app-fargate-lambda-dynamodb-python/module-two/

ECS - First Run 
https://aws.amazon.com/getting-started/tutorials/deploy-docker-containers/

Notes on Task Definitions
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-task-definition.html

Authenticate Docker to AWS and Push then Image
Authenticate, Build, Tag, Push 
https://docs.aws.amazon.com/AmazonECR/latest/userguide/registries.html#registry_auth
https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html

Important resource to deploy 
https://aws.amazon.com/getting-started/tutorials/deploy-docker-containers/

Elastic Beanstalk Examples 
https://github.com/NYPL-Simplified/Simplified/wiki/Docker-Deployment-Example:-Elastic-Beanstalk-with-CloudWatch



## Python Logging 
https://realpython.com/python-logging/