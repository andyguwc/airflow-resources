# Elastic MapReduce (EMR)

## EMR Basics
Deploy Spark and Hadoop 
- viewed as Hadoop as a service (managed cluster platform) - start a cluster to run tasks and pay for the time 
- simplify big data frameworks to process and analyze sizeable amounts of data
- run compute on data stored in S3. EMR can see S3 files the same way hadoop see HDFS 

Ways to query with SQL
- EMR
    - Hive
    - SparkSQL
    - Presto 
- Athena (leverages Presto)

Columnar file formats
- Parquet and ORC
- Agnostic formats
- Economical due to compression 

EMR has direct integrations with RDS, Redshift and DynamoDB 


## EMR Architecture Layers
- Storage
    - various file systems (HDFS, EMRFS, local file systems)
- Cluster Resource Managememt (YARN)
    - managing resources
    - schedule jobs processing data 
- Data processing frameworks 


## MapReduce and MPP 
Both algorithms based on divide and conquer for large data volumes 
- Cluster with lots of servers
- Node gets subset of data to work on
- Work in parallel
- With more data just add more servers 
- Elasticity works well here 

Map Reduce
- parse
- aggregate

MPP
- Partition query across RDBMS nodes 
- just one pass 

Streaming 
- Streaming data produced is high volume / small payload
- real time analytics 


## AI on EMR
- SparkML
- MXNet
- TensorFlow
- Jupyter and Zeppelin (notebooks)


## Configure EMR

Required Properties
- Need a EC2 key pair to SSH into the cluster
- Steps are units of work submitted to the cluster 
- Nodes
    - Master: 
        - manage and run components. Runs the YARN itself
    - Core:
        - run the data node daemon to coordinate data storage and access data
        - track tasks
    - Task:
        - Add more computing power 

Security Groups
- master security group
    - Allow other security groups related to EMR
    - CIDRs for other AWS services 
    - Allow SSH from my IP
- slave security group 
    - similar as above


EMRFS
- AWS implementation of the HDFS
    - Used by all EMR clusters for reading and writing to S3
    - Stores persistent data in S3 that is useable by Hadoop
    - Enables use of data encryption
- Allow Access to EMRFS
    - AmazonElasticMapReduceEC2Role 
        - Allow actions to specific buckets we'd interact with 
- Can allow encryption with AWS-KMS


Submit an EMR Job (Step)
- Add Step type
- Script location
    - note the script references other parameters as ${}
- Input location
- Output location 
- Arguments 


Submit Steps using CLI
- Get the master public DNS
- SSH into that
- Add Step by 

aws emr add-steps --cluster-id xxx --steps Type=xxx,Name=xxx \
ActionOnFailure=CONTINUE,Args=[-f, s3://script-locaion-xxx],INPUT=s3://input-location-xxx,OUTPUT=s3://output-location --region us-west-2



## Hive on EMR
Query map reduce clusters

Application - exporting DynamoDB data using Hive
- EMR utilizes built-in connection for accessing other AWS services
- We can perform DynamoDB operations such as loading data into an EMR cluster and exporting to S3
- Steps
    - First create a Hive compatible table within DynamoDB
    - While launching cluster - need to edit the software configurations 
    - SSH into the master
    - Run Hive commands on the DynamoDB table 
        - first map to an external table 
        - STORED by (DynamoDB connector)
        - map the columns



## Spark on EMR
- Distributed processing framework 
- Enables ML, stream processing on EMR cluster
- Optimized DAG engine that caches active data in memory
- Natively supoorts Scala, Python and Java




## MLlib
- Spark machine learning library 
- Algorithms, pipelines, persistenc, featurization, etc.
- More efficient than MapReduce

Run a Zeppelin Notebook
- Spin up MLlib
- Applications: have Spark and Zeppelin installed 
- Instead of typical SSH 
- Tunneling localhost 8080 to hadoop master node 8090
$ ssh -i ~/admin.pem -N -L 8080:ec2-18-xxxx.compute-1.amazonaws.com:8890 hadoop@ec2-18-xxx.compute-1.amazonaws.com






