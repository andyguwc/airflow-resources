# AWS Intro 

## What is AWS
- collection of cloud computing services
- can work together 
- to run web applications 

## Wy AWS
AWS Benefits
- cost
- scalability
- deloy different global locations (reduced latency, increased redundancy)
    - AWS regions which include availability zones (collection of data centers with redundant failover)
- can add and build new services 

Alternatives
- Azure: windows virtual machines, .NET applications
    - not the AWS global reach 
    - lacks services 
- Heroku 
    - easy app deployment 


EC2 for computing
S3 for storage 
RDS for databases
Route53 for URLs

## AWS Development 
Local Development & AWS Development 
- Similar 
    - application runs on OS/platform
    - requires platform to be installed
    - HTTP servers listen on ports
    - Connects to outside databases 
- Different
    - Local: everyone runs on same machine
    - AWS: one service = one responsibility. For example, database as a service, file served from S3. Connections done via AWS SDK 

- Each service given a local IP address 
    - not connected to the outside world 
    - talks via ports
    - some services access via amazong resource ID
    - connections may just be HTTP requests
 
## AWS Tooling 
Web Console 

SDK 
Support application code to interact with the services 
Making it easier and more robust 

CLI
Write shell scripts or batch files 
Made for operations engineers more than developers 



# EC2
An instance is like a computer (run applications, virtual desktop, 3rd party software, etc.)

Elastic - instances running computing operations can increase or decrease at will 

Steps:
- Choose an AMI (operating system + preinstalled software)
- Choose instance type (specs - CPU, RAM, Network Performance)
    - compute optimized, or storage, or memory 
- Configure instance
    - network VPC & subnet 
- Choose storage
- Configure Security group 
    - IP-based communication rules for a single or group of service instances
    - Control who can SSH into EC2 instance
    - Allow access between EC2 instances 
    - Allow access to databases
    - Accept HTTP requests
- Key pair to allow SSH 


Create Public IP for instances
- Elastic IP 
- Associate the instance and private IP to this Public IP adress
- download pem key value pair

Connect to EC2 instance via SSH 
$ chmod 400 ~/Downloads/pizza-keys.pem 
log to the instance 
$ ssh -i ~/Downloads/pizza-keys.pem ec2-user@100.21.116.12 

Upload and deloy application to EC2
- Update EC2
$ sudo yum update
$ curl -sL https://rpm.nodesource.com/setup_12.x | sudo bash -
$ sudo yum install -y nodejs

- Transfer demo application code to EC2 instance 
remove unnecessary modules
$ rm -rf node_modules
copy from local folder to EC2 instance 
$ scp -r -i ~/Downloads/pizza-keys.pem ./pizza-luvrs ec2-user@100.21.116.12:/home/ec2-user/pizza-luvrs
log in to EC2 again and cd to pizza-luvrs
$ ssh -i ~/Downloads/pizza-keys.pem ec2-user@100.21.116.12 
run npm install and npm start within EC2
enter elastic IP and port http://100.21.116.12:3000/ and should see application running 


Scale EC2
- Create AMI by snapshot existing EC2 instance 
- Load balancer - routing appliance that maintains a consistent DNS entry and balances requests to multiple instances 
    - Create application load balancer by first selecting port to listen on
    - make sure within VPC, with new secruity group and updated port for routing
    - configure target group routing 
    - enable instance stickiness on load balancer - user directed to same IP for subsequent requests
- Auto scaling group - expands and shrinks a pool of instances based on pre-defined rules
    - work on launcher 
        - use custom AMI
        - enter starter script into launch configuration user data 
    - work on scaler
    - change security group - inbound only fro load balancer 
    - create auto-scaling groups 
        - create scale-up and scale-down autoscaling policies 

<!-- #! /bin/bash
echo "start pizza-luvrs"
cd /home/ec2-user/pizza-luvrs
npm start -->

- Simulate Load 
    - use apache benchmark 
    $ ab -n 100 -c 5 http://pizza-loader-275934584.us-west-2.elb.amazonaws.com/


Update EC2
- upload new code to EC2
- create new AMI 
- update launch configration (making sure new IAM role can access S3)
- update auto scaling group 



Local dev can use configured user credentials but 
Assign IAM role to EC2 launch configuration 


# S3
- Store files and allow easy configuration regarding access 
- Object - file and metadata (filetype and modified date)
- Bucket is root resource to add/delete/modify objects
    - stores objects 
    - create ulr name space for the objects(Bucket Region + Bucket Name + Object Path)
- Access via IAM roles (AmazonS3FullAccess Policy)

Pricing
- amount of data stored
- number of requests
- amount of data transferred


Permissions
- grant access to other AWS accounts 


Latency 
- cross-region replication 
- or use CloudFront to solve geographic latency 

Creating S3 bucket 
- create S3 buckets
- policy generator https://awspolicygen.s3.amazonaws.com/policygen.html
- copy into bucket permissions


Upload objects to S3: copy from local folder to s3 bucket 
- can use conole, CLI, or SDK
- $ aws s3 cp ./assets/js s3://pizza-luvrs-tg/js --recursive --exclude ".DS_Store"
- get the root path and update url paths for static assets
https://pizza-luvrs-tg.s3-us-west-2.amazonaws.com/
- change local file store function to s3 file store
- enable CORS Cross origin resource sharing 

Accessing S3 with EC2
- assign IAM role to newly launched instances 
    - create EC2 role (roles are like users but without log in)
    - give the role access to S3
    - Create new launch configuration
        - AMI with updated code
        - IAM role with the ec2-role
        - enter starting script 
        - assign public IP to every instance





# RDS
- scheduled automatic backups
- update software
- easy to take DB snapshots and change the hardware
- multiple AZ
- RDS run on EC2 instances
    - When creating Database, it created EC2 instance with operating system and database engine 
- Database read replica (non production copy with eventual consistency)

Connecting to a database in RDS
- add rule in security groups
- use Client to access the database (host, username, password)


ORM - Object Relational Mapping (Sequalize)
Converts between database and in app objects 

Update the code to use the ORM
- data and model parts 

Add the AmazonRDSFullAccess to the ec2-role and allow access to RDS instance from ec2-sg by adding to the RDS instance secruity group 


# DynamoDB
- support both document and key-value models 
- benefits
    - unlimited elastic storage
    - no hardware choices
    - pay for what you use 

Pricing
- provisioned throughput capacity
- amount of data stored
- guaranteed great read/write performance

Table contains a set of items 
each item should have primary keys 

read/write operations per second provisioned for DynamoDB

Relational: strict data schema
NOSQL like DynamoDB flexible wiht data schema, but limited query properties 

Connect to application
- require aws-sdk in the app data (dynamoStore.js)
- create the put item get item functions 
- making sure the acccess and security group is updated for EC2, etc.



# Redshift 
- data warehouse
- Take RDS, Dynamo, and S3 to Redshift 
- basic structure a cluster (collection of nodes)

Features
- can set up VPC protection
- data warehouse encryption
- no public IP

Pricing
- pay for what you use 
- dense compute vs. dense storage 
    - dense compute - cheaper, less storage
    - dense storage - more expensive 



# Route53
Amazon service for DNS management 
Translates human readable URL to an IP address 
Provides health checks for given URL paths 

Pricing
- hosted zone
- queries 
- DNS entries 



# Elastic Beanstalk
Elastic Beanstalk - more convenient and feature rich way to run applications
- Take application code and run on EC2 instance
- Scaling, monitoring, and resource provisioning

Basic structure is an application
- represents a logical application 
- runs a single platform (node.js, java)
- has application versions - Application versions are stored in S3
- application has an environment: ami, ec2 instances, auto scaling group

Application deployment steps 
- upload new code to EC2 instance
- create AMI
- update load configuration
- update auto scaling group 
- terminate old instances 

Steps
- zip the code and upload $zip -r package.zip .
- configure options and VPC
- modify security and all the options
- Add EB, RDS, etc policies to EC2 IAM role
    - add AmazonRDSFullAccess
- change Security Group access 
- restart app servers 




# CloudFormation Template
Infrastructure as code
Provision resources using configuration templates in JSON
- for example to create a development stack to match prod
Template JSON document
- stack: a group of AWS resources created by a single template 
    - can update or delete a stack, for example change size of EC2 instance 
- CloudFormation only creates the resources explicitly 
    - CloudFormer creates a template based on existing infrastructure



# VPC
Secure resources into groups that follow access rules and share a logical space - networking 
- security groups secure single instances
- VPCs secure groups of instances 
- separating your reosurces from others on AWS or public
- with VPCs, the resources have private IP addresses ranges which they can communicate with each other 

A layer of security separating your resources from others and the public 
- can remove any public access to resources
- and have VPN

For networking needs
- commonly used for launching EC2 instances

Features
- configure routing tables
- use NAT gateway
- internal IP

Structure
- subnets (private/public subnets)
- assign groups to each

Pricing
- basic VPC configuration is free 

Security group
- defines allowed incoming/outgoing IP addresses and ports to/from instances. Like a mini-firewall 

Routing tables
VPC uses routing tables and network access control list (IP filtering table)

Network access control list
- IP filtering table 
- applies rules for entire VPC

Subnets
- instances must be launched within subnets within the VPC
- with its own separate routing table and network access control list 
- public / private subnets: private subnet must have a NAT gateway to public subnet to access the outside world 

Creating a VPC 
- ensure in the correct region 
- set VPC configuration
    - choose range of IP addresses 
    - subnets
    - set internet gateway / routes
- each subnet can only live within one availability zone so need to create more subnets for more avaiability zones 




# CloudFront
Content delivery network 
- Makes data and resources available quicker
- Works with Route53, load balancer, EC2, and S3
    - Reduce distance between user and app


CloudFront Distribution 
- specify original content location (s3 bucket) and a unique cloudfront URL will be linked 
- distribution 
    - determines cache behavior based on path 
    - set time-to-live for specific content 
    - fine tuned control over caching behavior 

Create distribution
- path pattern
- cache allowed methods 
- set TTL



# ElastiCache
Managed service for in-memory cache service 
- Managed maintenance upgrades
- Automatic read replicas
- Node management

Cluster
- running several nodes (individual EC2 instances running caching software)

Steps
- Create security group for ElastiCache cluster 
- Select Redis 
- Create a Cache subnet group (VPC to host elasticache clusters)
- Give EC2 IAM role full access to ElastiCache
- in the app, put the cache redis configuration in there 







# CloudWatch 
Setting alarms and notifications in response to events

Monitoring
- monitoring resources
- action on alerts
- can also filter logs 


Metrics examples 
- DynamoDB read/write throughput
- EC2 CPU usage 
- Estimated billing charges

SNS
- topics that we can subscribe to 

CloudWatch Alarm 



# IAM 
Identity & Access management
Configuring and managing users 

Users / Policies / Groups 

IAM Policy 
- collection of permissions to access different services
    - resource permission
    - service permission
- default no permissions
- policies can be applied to individual users or to groups 
- policy statement
    - effect: allow or deny
    - action: operation user can perform on services
    - resource: specific resources user can perform action on 

Users/Groups 
- Permissions via policies 
- IAM Groups: can apply policies to groups 
- Users can be added to multiple groups 
- Example: Developer Group Policy has EC2 Full Access while Tester Group Policy has DynamoDB Read-only and S3 Full Access Test Bucket

Best practice is to assign policies to IAM groups instead of Users 


Root account
- administer all services
- modify billing info
- manage users

Best practices
- MFA: authentication that requires more than one factor to authenticate 


User Login
https://485216659578.signin.aws.amazon.com/console



# Example AWS Application
First install Node and AWS CLI

AWS account and Access key to initialize, making sure things are configured by running:
$ aws ec2 describe-instances

















