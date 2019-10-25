# Docker Intro
<!-- https://github.com/StephenGrider/DockerCasts -->

## Basics
- What is Docker
    - Docker is a platorm for creating and running containers
    - Docker ecosystem: docker client, server, machine, images, hub, compose 

- Image & Container
    - Image: single file with all the deps and config required to run a program
        - CLI reaches dockerhub to download the image
        - image contains a file system snapshot and startup command
    - Container: instance of an image. Runs a program
        - with own memory, networking, and hard drive 

- Container background
    - in a computer we have multiple applications / processes running which issue requests (system calls) to kernel to interact with a piece of hardware (cpu, memory, hard disk)
    - with namespacing, isolate resources / subgroups of hardware 
    - control groups limit amount of resources used per process 


- Why Docker
    - Easy to install and run software without worrying about dependencies 



# Docker CLI & Server

## Docker CLI
    - used for issuing commands
    - sometimes need to run $ eval "$(docker-machine env default)"

## Docker Server (Daemon)
    - tool for creating images and running containers, etc.

- Process
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    3. The Docker daemon created a new container from that image which runs the executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it to your terminal.

## Basic Commands 

Creating and running a container from a image
$ docker run hello-world 
docker run is identical to docker create (filesystem allocated) + docker start (execute the process)

Command overwrite docker run <image name> <command overwrite>
$ docker run busybox echo hi there 
$ docker run busybox ping google.com

list all active containers on the machine
$ docker ps 

list all containers ever created 
$ docker ps -a  

start a container back up
$ docker start 36ed314a8223

remove stopped containers 
$ docker system prune 
remove specific containers
$ docker container rm cc3f2ff51cab cd20b396a061

retrieve log outputs
$ docker create busybox echo hi there 
$ docker logs <container id>

stop a container 
typically use the stop command 
$ docker stop (send a sigterm message to the process to shut down with time to clean up)
$ docker kill (send a sigkill signal to shut down immediately )

## Execute Multiple Commands
for example execute redis-server and redis-cli inside one container 
exec allows running another command 
$ docker exec -it <container id> <command>

$ docker exec -it 720765aabab4 redis-cli

note: -it flag allows ability to take inputs from terminal to the running process 
-i means input, -t means text looks good

open up shell terminal in running container 
sh is a command shell 
$ docker exec -it 720765aabab4 sh

starting with a shell
use this everytime you want to poke around in a container 
$ docker run -it busybox sh


# Docker Images 

## Dockerfile
- creating docker images - configuration to define how container should behave 
- Dockerfile -> Docker Client -> Docker Server -> Usable Image

Dockerfile
- specify a base image
- run some commands to install additional programs
- specify a command to run on container startup 


<!-- # Use an existing docker image
# Use alpine as base image OS (which already has the apk)
FROM alpine 

# Download and install dependency
# use apk as apache package manager to install redis 
RUN apk add --update redis 

# Startup command
CMD ["redis-server"] -->


## Docker Build Process
. indicates we want ot build out of the current directory
$ docker build . 

Every step along the way, we took the image generated from previous step, make a container, execute the command, and save the file system as output snapshot, then shut down the temporary container 


<!-- Download from base -->
Step 1/3 : FROM alpine
latest: Pulling from library/alpine
9d48c3bd43c5: Pull complete 

Digest: sha256:72c42ed48c3a2db31b7dafe17d275b634664a708d901ec9fd57b1529280f01fb
Status: Downloaded newer image for alpine:latest
 ---> 961769676411

Step 2/3 : RUN apk add --update redis
<!-- get a temporary container from the previous image -->
 ---> Running in 391904dcc2a7
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.10/community/x86_64/APKINDEX.tar.gz
(1/1) Installing redis (5.0.5-r0)
Executing redis-5.0.5-r0.pre-install
Executing redis-5.0.5-r0.post-install
Executing busybox-1.30.1-r2.trigger
OK: 7 MiB in 15 packages
 ---> a362e45aed73
 <!-- took a snapshot of the container (with redis running) and stopped it  -->
Removing intermediate container 391904dcc2a7

<!-- CMD setting primary command -->
Step 3/3 : CMD redis-server
 ---> Running in 65ef6a355d5c
 ---> ed681a46d27c
Removing intermediate container 65ef6a355d5c
Successfully built ed681a46d27c


Cache
- Docker knows nothing has changed from the last time running docker build 
- When changing Docker file make sure changes are as far down as possible 


## Tagging an Image 
- $ docker build -t username/redis:latest .
- convention is dockerID/projectname:version directory

## Docker Commit 
- input a container, and using commit, we get image as an output
docker commit -c 'CMD ["redis-server"]' ed681a46d27c 


# Project Example with Docker 
Steps
- Create NodeJS Web app
- Create a Dockerfile
- Build image from dockerfile
- Run image as container
- Connect to web app from a browser


## Tags and Filelinks
FROM node:6.14
<!-- alpine as slim/simple as possible -->
FROM node:alpine  

## Copy Build Files
No file is there by default 

COPY ./ ./ <!-- copy from current working directory to container -->
Path to folder to copy from your machine relative to build context
Place to copy stuff inside the container 

$ docker build -t andyguwc/simpleweb .
<!-- 
FROM node:alpine

COPY ./ ./
RUN npm install 

CMD ["npm","start"] 
-->

to play around in the shell 
$ docker run -it andyguwc/simpleweb sh

## Container Port Mapping
Anytime someone makes requests to a given port to local network, take that request and forward to some port into a container 

Port mapping
docker run -p 8080: 8080 imageid
- route incoming request to this port on local host to
- this port inside the container 

<!-- note in docker toolbox use 192.168.99.100 as localhost -->


## Specifying Root Directory

workdir /usr/app 
- any following command will be executed relative to this path in the container

## Rebuilds & Caching 
Making a change to the file makes COPY step invalidated, which also needs complete reinstall of dependencies 

Solution: just copy over the package.json and install dependencies, then copy the rest of the files 

WORKDIR /usr/app 

## Install Dependencies
COPY ./package.json ./
RUN npm install
COPY ./ ./ 


# Docker Compose

## Multiple Components
Need multiple components
- Node app server
- Redis server (containing the number of times visited)

Container do not have any communications, to set networking we can use Docker Compose 
- saves a lot of repetitive commands from Docker CLI 

## Docker Compose File 
write out the build and run commands in the docker-compose.yml

Pseudo Code
Here are the container I want created:
- redis server
    - make it using the redis image
- node app
    - make it using the Dockerfile in directory
    - map port 8081 to 8081


<!-- 
docker-compose.yml

version: '3'
services:
  redis-server:
    image: 'redis'
  node-app:
    build: .
    ports: 
      - "8081:8081" 
-->

## Networking
Two containers in the same docker-compose file are automcatically linked

<!-- below the redis-server is also the service name -->
const client = redis.createClient({
  host: 'redis-server'
});

## Docker Compose Commands

Launch containers 
- $ docker run myimage
- $ docker-compose up 

Launch in background
- $ docker-compose up -d

Rebuild
in docker we use 
- $ docker build .
- $ docker run myimage
while for docker-compose 
- $ docker-compose up --build 

Stop docker compose containers 
- $ docker-compose down

Container maintenance
- if status code 1,2,3 that's error, otherwise 0 
- automatic container restarts

 <!-- node-app:
    restart: always
    build: .
    ports: 
      - "8081:8081" -->

- restart policies
    - "no"
    - "always"
    - "on-failure"
    - "unless-stopped"

need to run from appropriate directory 
$ docker-compose ps 


# Development  

## Development Workflow 

Development -> Testing -> Deployment 

Github repo -> Travis CI -> AWS hosting 
- Github first pull, then develop and create PR 
- Travis CI runs tests and if tests run well, merge PR with master
- Travis CI automatically pushes to AWS hosting


Common commands to run in example node react app 
- start a development server
    - $ npm run start
- run tests associated with the project
    - $ npm run test
- build a production version of the application
    - $ npm run build 


## Creating Dev Dockerfile 
In development 
- npm run start
- Dockerfile.dev, with -f representing specifying file name 
- $ docker build -f Dockerfile.dev . 
- $ docker run -p 3000:3000 10cbd9810747

In Production
- npm run build
- Dockerfile

Making sure changes propagate to running container 
- use volume mounting
- set up a placeholder inside docker container, with reference to the local folders, 
- $ docker run -p 3000:3000 -v /app/node_modules -v "$(pwd)":/app 
<image_id>
    - put a bookmark on the node_modules folder (don't try to map it up)
    - map the pwd into the /app directory

- using docker-compose 
    - context: where we want the files to be pulled from 
<!-- Dockerfile.dev
version: '3'
services:
  web:
    build: 
      context: .
      dockerfile: Dockerfile.dev
    ports: 
      - "3000:3000"
    volumes:
      - /app/node_modules
      - .:/app 
-->

## Executing Tests
Run tests associated with the project 
$ npm run test 
$ docker run -it d2d61a2776ae npm run test

Live update tests 
- start a second service to just run tests 
<!-- Dockerfile.dev
 tests:
    build: 
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - /app/node_modules
      - .:/app
    command: ["npm", "run", "test"] 
-->

- use docker attach to forward commands from terminal to the container 


## Multi Step Build 
Dockerfile for production will start a Nginx server 

Build application and use nginx for the run phase 
Dockerfile:
- build phase
    - use node:alpine
    - copy the package.json file
    - install dependencies 
    - run 'npm run build'
- run phase
    - use nginx
    - copy over the result of 'npm run build'
    - start nginx 

<!-- Dockerfile 
FROM node:alpine as builder 

WORKDIR '/app'

COPY package.json .
RUN npm install 
COPY . .
RUN npm run build 

FROM nginx 
COPY --from=builder /app/build /usr/share/nginx/html  
-->

$ docker run -p 8080:80 3f70388d6dfc


# Continuous Integration and AWS Deployment 

## Single Container Process 
Steps:
- push code to github
- travis automatically pulls repo 
- travis builds an image, tests code
- travis pushes code to AWS EB 
- EB builds image, deploys it 


## Travis CI 
Push code to Github -> Github let Travis know -> Travis download the code and do some work (e.g., run tests, deploy, etc.)

Travis YML Config 
- in the .travis.yml file 
- steps 
    - tell travis we need a copy of docker running
    - build image using Dockerfile.dev
    - run test suite (inside the container)
    - deploy code to AWS


<!-- .travis.yml
sudo: required 
services:
  - docker 

before_install:
  - docker build -t andyguwc/docker-react -f Dockerfile.dev . 

script:
  - docker run -e CI=true andyguwc/docker-react npm run test 

-->

- config to auto deploy to AWS 
    - add deploye settings
    - travis will zip up code files and put them in a S3 bucket
    - then travis will tell elastic beanstalk to deploy the new application
    - generate a new user to be used by travis CI with programmatic access by travis ci 
        - store the secret keys in travis ci environment variables 
    
<!-- 
.travis.yml
deploy: 
  provider: elasticbeanstalk 
  region: "us-west-2"
  app: "docker"
  env: "Docker-env"
  bucket_name: "xxx.us-west-2.xxx"
  bucket_path: "docker"
  on:
    branch: master
  access_key_id: $AWS_ACCESS_KEY
  secret_access_key:
    secure: "$AWS_SECRET_KEY" 
-->


## Elastic Beanstalk 
Easy to run containers 
- create an application
- create environment - set base configuration and select Docker as preconfigured platform 
    - elastic beanstalk will do load balancing 


## Build Multi Container Application 

- Create App
    - /worker set up redis worker (su`bscriber) to listen on new index values (messages) and calculate fib numbers to write back to redis
    - /server to set up the main application (express.js) 
        - redis connection (as publisher)
        - postgres connection 
        - set up routes (get all values or current values, and for submitting values to start the publisher)
    - /client set up react app 
        - set up components
        - set up form tags
        - handle submit 
        - routing in the react app
    
- Add Docker Devs
    - Make dev Dockerfiles for each of React App, Express Server, Worker
    - workflow
        - copy over package.json 
        - run npm install 
        - copy over everything else
        - docker compose should set up a volume to share files so we don't need to rebuild image every time 
    - build Dockerfile.dev for /client, /server, /worker 

- Docker Compose 
    - postgres:  
    - redis:  
    - server:
        - build
        - volumes - to make sure container source code updates 
        - env variables - specifying env variables (in keys.js) for the server 

- Specifying Env Variables in Docker Compose 
    - variableName=value (set a variable in the container at runtime)
        - the image doesn't know, 
    - variableName
        - ithe value is taken from the computer
    - anytime specifying name inside docker compose service, just refer to the service name instead of the full url as host 

- Add nginx image 
    - routing (static content to React server but API request to Express server)
    - if /api in the route, then redirect to the express server otherwise to react server 
    - set default.conf to allow nginx to default traffic 

- Deploy Steps:
    - Push code to github
    - Travis automatically pulls repo
    - Travis builds a test image, tests code
    - Travis builds prod images
    - Travis pushes built prod images to Docker Hub
    - Travis pushes project to AWS EB 
    - EB pulls image from Docker Hub, deploys 

- Build Production Dockerfiles 
    - for server and worker change CMD ["npm","run","start"]
    - for react make sure Nginx w/prod react files are on port 3000

- Build travis.yaml
    - before_install has the build context for running the tests
    - script 
    - after_success
        - docker build xxx
        - log in to the docker CLI (env variables put in travis tool) 
        - take those images and push them to docker hub 
    
- Multi Container Deployments on AWS 
    - Dockerrun.aws.json
        - docker-compose.yml -> Dockerrun.aws.json 
        - Dockerrun.aws.json will just pull the image 
        - elastic beanstalk delegates the docker hosting to elastic container (via passing task definitions)
        - https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html
    - Elastic Beanstalk environment
    - Create Redis with Elastic Cache
    - Create Postgres with RDS 
    - Use VPC and Security Groups to make sure services are linked
        - VPC is based on region, it's like a box protecting all the services
        - Security group is like Firewall Rules, which allows rules for incoming traffic and outgoing traffic 
            - Allow any incoming traffic on Port 80 from any IP
            - Allow any traffic from any other AWS service that has this security group 
    - Setting Environment Variables 
        - using the console on Elastic Beanstalk to set environment properties 
    - IAM Keys for Deployment 
        - Full Access to lots of the services 
        - Put the keys in the travis-ci variables 
    - Check request logs to verify deployment 


RDS Database Creation
- Go to AWS Management Console and use Find Services to search for RDS
- Click Create database button
- Select PostgreSQL
- Check 'only enable options eligible for RDS Free Usage Tier'
- Set DB Instance identifier to multi-docker-postgres
- Set Master Username to postgres
- Set Master Password to postgres and confirm
- Make sure VPC is set to Default VPC
- Set Database Name to fibvalues
- Create Database

ElastiCache Redis Creation
- Go to AWS Management Console and use Find Services to search for ElastiCache
- Click Redis in sidebar
- Make sure Redis is set as Cluster Engine
- In Redis Settings form, set Name to multi-docker-redis
- Change Node type to 'cache.t2.micro'
- Change Number of replicas to 0
- Scroll down to Advanced Redis Settings
- Subnet Group should say “Create New" and Set Name to redis-group
- VPC should be set to default VPC
- Tick all subnet’s boxes
- Create ElastiCache

Creating a Custom Security Group
- Go to AWS Management Console and use Find Services to search for VPC
- Create Security Group button and set Security group name to multi-docker
- Set Description to multi-docker
- Set VPC to default VPC
- Create a Security Group 
- Manually tick the empty field in the Name column of the new security group and type multi-docker, then click the checkmark icon.
- Edit Inbound Rules
- Set Port Range to 5432-6379
- Click in box next to Custom and start typing 'sg' into the box. Select the Security Group you just created, it should look similar to 'sg-…. | multi-docker’

Applying Security Groups to ElastiCache
- Go to AWS Management Console and use Find Services to search for ElastiCache
- Check box next to Redis cluster and click Modify
- Change VPC Security group to the multi-docker group and click Save

Applying Security Groups to RDS
- Go to AWS Management Console and use Find Services to search for RDS
- Check box next to your instance
- Click Modify DB instance button

Applying Security Groups to Elastic Beanstalk
- Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
- Click the multi-docker application tile
- Click Configuration link in Sidebar
- Scroll down to EC2 Security Groups and tick box next to multi-docker

Setting Environment Variables
- Go to AWS Management Console and use Find Services to search for Elastic Beanstalk
- Click the multi-docker application tile
- Modify configuration 
- Scroll down to Environment properties
    - In another tab Open up ElastiCache, click Redis and check the box next to your cluster. Find the Primary Endpoint and copy that value but omit the :6379
    - Set REDIS_HOST key to the primary endpoint listed above, remember to omit :6379
    - Set REDIS_PORT to 6379
    - Set PGUSER to postgres
    - Set PGPASSWORD to postgrespassword
    - Set the PGHOST key to the RDS postgres endpoint value listed above.
    - Set PGDATABASE to fibvalues
    - Set PGPORT to 5432

IAM Keys for Deployment
- Find Services to search for IAM
- Set User name to multi-docker-deployer
- Set Access-type to Programmatic Access
- Select Attach existing polices directly button
- Search for 'beanstalk' and check all boxes
- Click Create User - Copy Access key ID and secret access key for use later

AWS Keys in Travis
- Open up Travis dashboard and find your multi-docker app
- Scroll to Environment Variables
    - Add AWS_ACCESS_KEY and set to your AWS access key
    - Add AWS_SECRET_KEY and set to your AWS secret key
    
# Kubernetes 

## Why Kubernetes 

- Scaling Application
    - Worker Container is the limiting factor 
    - Node is a virtual machine / physical computer 
- Kubernetes
    - Has a Master which controls what each Node does 
    - Master relays the commands to each of the Nodes 
- Summary 
    - What is Kubernetes: system for running many different containers over multiple different machines 
    - Why use Kubernetes: when you need to run many different containers with different images

## Local Kube Development 

- Install Kubectl (CLI for interacting with our master)
- Install a VM driver virtualbox (to make a VM that will be your single node)
- Install minikube (run a single node on that VM)




    















