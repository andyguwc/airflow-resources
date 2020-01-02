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
- Web Console 

- SDK 
    - Support application code to interact with the services 
    - Making it easier and more robust 

- CLI
    - Write shell scripts or batch files 
    - Made for operations engineers more than developers 

Blueprints
    - Infrastructure as code


## AWS Setup
Create key value pair for User 

EC2 create key value pair
- Used for SSH into the EC2 instance 
- Make sure change the access rights of the mykey.pem
$ chmod 400 mykey.pem 



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

Relational Databases

## Capabilities 
- scheduled automatic backups (and manual snapshots)
- update software
- easy to take DB snapshots and change the hardware
- multiple AZ
- RDS run on EC2 instances
    - When creating Database, it created EC2 instance with operating system and database engine 
- Database read replica (non production copy with eventual consistency)
- Monitoring (with cloudwatch)
- Encryption at rest 

## Concepts 
Database instances - the environment for setup
Multiple database engine - mysql, postgres, oracle, etc. 
Data backup - restored to a point in time 


## Pricing 
- DB instance type (upfront)
- Storage per GB (sometimes IO requests too)
- Data transfer out 
- Backup storage 

## Setup 

Creating Instances (Upfront Choices)
- Type of Instance 
- How much Storage
- Type of Storage 
- Region 
- Level of resilience 
- Which database engine
- Who needs access 

Storage Types 
- General Purpose SSD 
    - 5GB - 3 TB in size
    - pay storage only 
    - 3 IOPS per GB 
    - Small to Medium DBs
- Provisioned IOPS SSD 
    - 100 GB - 3 TB in size
    - Set 1000 - 30000 IOPs
    - Pay storage + IOPS
- Magnetic Storage 
    - 5GB - 3TB in size 
    - 100 IOPS
    - Pay storage + IOPS
    - Best Price

Steps
- Launch DB Instance 
    - Choose Engine (e.g. MySQL)
    - Pick DB Instance Class (size) and Options like Multi-AZ, Storage Type, etc. 
    - Provide instance ID, master username, password 
- Configure Network & Security 
    - VPC
    - Security Group (provide access to specific IP to DB instance)
- Securing Instances 
    - IAM Policies applied to RDS server - which actions to perform on what resources 
        - DB instances
        - DB read replicas 
        - DB snapshots
        etc.
    - Security Groups 
        - DB Security Groups vs. VPC Security Groups
            - EC2 Security Group when DB not in VPC
            - VPC Security Group when DB in a VPC
        - Add one to many authorizations

## Connecting to an Instance
- Use DNS, not IP

- Connect via Client tools 
    - Access from machine with approved source IP (via Security Group)
    - add rule in security groups
    - use Client to access the database (host, username, password)
    - with connection string 
    - using a client tool like MySQL workbench 

- Connect in App using ORM - Object Relational Mapping (Sequalize)
    - Converts between database and in app objects 
    - data and model parts of the code 

Add the AmazonRDSFullAccess to the ec2-role and allow access to RDS instance from ec2-sg by adding to the RDS instance secruity group 


## Importing Data 
Choose tool/pattern based on 
- Data size
- Source / destination engine 

Take snapshots, disable automatic backups before load 

## Lifecycle Activities 

Backup and Restore 
- Automated Backup
    - regular backup during backup window
    - 0 -35 day backup retention period 
- Restore instance ot any time during retention period 
    - Default security group (needs to switch to customized one)
- Instance Action -> Restore to a point in time 
    - this will create a brand new instance 
    - copy new endpoint to the app and DB client 


Snapshots
- Manual database backups 
- Can copy or restore snapshots (across regions will take long)


Database Scaling 

Scale Performance
- Increase storage amount 
    - Instance Action modify move to bigger instance
    - Brief moment of outage
- Change storage type 
- Change instance class 


Scale Availability 

Read Replicas 
- DB replica for read access 
- Async replication 
- MySQL and PostgreSQL 
- Can make a replica an instance 
- Scale high traffic instances
- Source for reports 
- Highly available read access 
- Replica size should match source DB 
- In App
    - read operations against the read replica host 

Multi-AZ Deployment (high availability)
- Synchronous standby instance in different AZ
- Configured at instance create/convert time 
- Performance degradation (write transaction to multiple locations)
- Endpoint won't change 
- Reboot with Failover 


## Monitoring & Maintenance 

Database Logs
- View 
- Watch (real time update)
- Download 
- Query 
- Retention Periods 

CloudWatch metrics & alerting 
- Event push notification
- View events 
- CloudTrail audit of API requests 



# DynamoDB
- support both document and key-value models 
- benefits
    - unlimited elastic storage
    - no hardware choices
    - pay for what you use 
    - native redundancy

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

## Core Concepts
- data warehouse
- Take RDS, Dynamo, and S3 to Redshift 
- basic structure a cluster (collection of nodes)
- based on postgres SQL (can use postgres drivers, etc.)
- MPP 
- Columnar data storage 

- Star chemas (denormalized dimension tables)
- Snowflake schemas 

Fully managed 
- Built in data replication and backup 

Redshift Architecture
- Drivers make connection to the Cluster 
- Cluster has Leader Node and Compute Nodes 
- Leader node dealt with outside communication and organzie the compute nodes
- Node has slices (with separate memory, computation etc.)

Columnar Data Storage 
- Typical each row stored in a separate block 
- Columnar each data block stores a single column for multiple rows 


## Features
- can set up VPC protection
- data warehouse encryption
- no public IP
- nativ eredundancy 
- postgres-like engine 


## Pricing
- pay for what you use 
- node type (dense compute vs. dense storage)
    - dense compute - cheaper, less storage
    - dense storage - more expensive 
- Backup storage 

## Creating Clusters and Databases 
Dense Storage Nodes vs. Dense Compute Nodes
- Storage with a lot of data 
    xlarge
    - 1-32 nodes
    - 2 TB HDD
- Compute for complex queries 
    xlarge
    - 1-32 nodes
    - 160 GB SSD 

Cluster Considerations
- Region (depends on Source DB)
- Node Type 
- Cluster Size 
- Parameter Group
- Security Group
    - Set of rules identifying IPs that can access the cluster
- IAM 
    - API actions 
    - Allow or Deny 
    - Resource tied to action 
    
Apply Security 
- Security Group
    - Authorization for this machine
    - Add IP range 
    - Or pick EC2 security group
- IAM
    - Policy specifically for Redshift 
    - Admin or ReadOnly 
- Encryption
    - Redshift encrypts all data 
    

Access Cluster
- Use connection string via SSL 
- Check IP Access and SSL certificate
- Connect Client to cluster 

Download JDBC Driver and Client Tool


## Data Loading
Table Creation
- Specify column information during table creation
    - compression type
    - data distribution style
    - sort keys 

Best Practices
- Consider distribution style 
- Carefully choose sort key 
- Use COPY and automatic compression 
- Small column size 
- Leverage data/time types
- Define constraints 
- Use multiple files in COPY
- Validate data with NOLOAD option 
- Use manifests during COPY
- VACCUM and ANALYZE after load
- Merge using staging tables 

S3
- COPY command is best 
- Delimited (encrypted, compressed) flat files 

DynamoDB
- COPY command 
- Attribute mapping to column names 
- Can throttle throughput

RDS -> S3 -> Redshift
- RDS export to csv
- Upload csv to S3
- COPY command in Redshift client (SQL workbench)

Changing Cluster Size
- Choose to resize cluster (programatically or via console)
- Cluter put into read only mode
- New target cluster created
- Data copied from source to target
- Connections switch to target cluster 

CloudWatch Metrics
- CPU utilization
- Health Status
- Throughput 
- Read, write IOPS
- Read, write latency

Viewing Query & Performance Metrics
- identify relationship between cluster and DB performance 


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

















