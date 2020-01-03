

# Launch an RDS Database

## Launching Instances
Launch a database instance
Connect an application to the database endpoint

Attributes needed to connect to launch an RDS database
AllocatedStorage Storage size of your database in GB
DBInstanceClass Size (also known as instance type) of the underlying virtual machine
Engine Database engine (Aurora, PostgreSQL, MySQL, MariaDB,
Oracle Database, or Microsoft SQL Server) you want to use
DBName Identifier for the database
MasterUsername Name for the master user
MasterUserPassword Password for the master user

## Instance Types
Because a database has to read and write data to a disk, I/O performance is important
for the database’s overall performance. RDS offers three different types of storage
1 General purpose (SSD)
2 Provisioned IOPS (SSD)
3 Magnetic

The general purpose (SSD) option offers moderate baseline performance with the ability to burst. 
The throughput for general purpose (SSD) depends on the amount of initialized storage size. 
Magnetic storage is an option if you need to store data at a low cost, or if you don’t need to access it in a predictable, performant way.


## CloudFormationg Template for RDS
CloudFormation template for launching a MySQL database
https://github.com/AWSinAction/code2/blob/master/chapter11/template.yaml

wordpress application involving RDS
aws cloudformation create-stack --stack-name wordpress --template-url \
https://s3.amazonaws.com/awsinaction-code2/chapter11/template.yaml \
--parameters ParameterKey=KeyName,ParameterValue=mykey \
ParameterKey=AdminPassword,ParameterValue=test1234 \
ParameterKey=AdminEMail,ParameterValue=your@mail.com

```
DatabaseSecurityGroup:
# allowing traffic on the mysql default port for web servers
Type: 'AWS::EC2::SecurityGroup'
Properties:
    GroupDescription: 'awsinaction-db-sg'
    VpcId: !Ref VPC
    SecurityGroupIngress:
    - IpProtocol: tcp
    FromPort: 3306
    ToPort: 3306
    # this references the security group of EC2 instances running web servers
    SourceSecurityGroupId: !Ref WebServerSecurityGroup
Database:
Type: 'AWS::RDS::DBInstance'
DeletionPolicy: Delete # enable snapshot in production 
Properties:
    AllocatedStorage: 5
    BackupRetentionPeriod: 0
    DBInstanceClass: 'db.t2.micro'
    DBName: wordpress
    Engine: MySQL
    MasterUsername: wordpress
    MasterUserPassword: wordpress
    VPCSecurityGroups:
    - !Sub ${DatabaseSecurityGroup.GroupId}
    DBSubnetGroupName: !Ref DBSubnetGroup
DependsOn: VPCGatewayAttachment
DBSubnetGroup:
Type: 'AWS::RDS::DBSubnetGroup'
Properties:
    DBSubnetGroupDescription: DB subnet group
    # use subnet A or B to launch RDS database instances
    SubnetIds:
    - Ref: SubnetA
    - Ref: SubnetB
```


# Importing Data into a Database

To import a database from local environment to Amazon RDS
- Export the local database (using mysql commands itself)
- Start a virtual machine in the same region and VPC as the RDS database
- Upload the database dump to the virtual machine (via S3)
- Run an import of the database dump to RDS database on the virtual server 

First get the IP address of the virtual machines ($PublicIpAddress)

$ aws ec2 describe-instances --filters "Name=tag-key,\
Values=aws:cloudformation:stack-name Name=tag-value,\
Values=wordpress" --output text \
--query "Reservations[0].Instances[0].PublicIpAddress"

Then SSH into the machin
$ ssh -i $PathToKey/mykey.pem ec2-user@$PublicIpAddress

Download the database dump from S3 
$ wget https://s3.amazonaws.com/awsinaction-code2/chapter11/wordpress-import.sql

To import the database dump to the RDS database instance, need port, hostname, endpoint of the MySQL database 
$ aws rds describe-db-instances --query "DBInstances[0].Endpoint"

Run the command in the VM to import the data from the wordpress-import.sql file into the RDS databse instance 
$ mysql --host $DBHostName --user wordpress -p < wordpress-import.sql


# Backup and Snapshot 

## Configure Automated Snapshots
For CloudFormation, if the BackupRetentionPeriod is set to a valid value 
- BackupRetentionPeriod: 3 means keep snapshot for 3 days. Set the retention period to 0 to disable snapshots
- PreferredBackupWindow: '05:00-06:00' means creating snapshots automatically between 5-6 UTC

Creating a snapshot requires all disk activity to be frozen. Requests will be delayed or failed 

Database:
    Type: 'AWS::RDS::DBInstance'
    DeletionPolicy: Delete
    Properties:
        AllocatedStorage: 5
        BackupRetentionPeriod: 3
        PreferredBackupWindow: '05:00-06:00'
        DBInstanceClass: 'db.t2.micro'
        DBName: wordpress
        Engine: MySQL
        MasterUsername: wordpress
        MasterUserPassword: wordpress
        VPCSecurityGroups:
        - !Sub ${DatabaseSecurityGroup.GroupId}
        DBSubnetGroupName: !Ref DBSubnetGroup
DependsOn: VPCGatewayAttachment


## Manual Snapshots
To create a snapshot you have to know the instance identifier
$ aws rds describe-db-instances --output text \
--query "DBInstances[0].DBInstanceIdentifier"

Then create the snapshot
$ aws rds create-db-snapshot --db-snapshot-identifier \
wordpress-manual-snapshot \
--db-instance-identifier $DBInstanceIdentifier


## Restore Snapshots
To restore snapshots, need to know the database's subnet group 
$ aws cloudformation describe-stack-resource \
--stack-name wordpress --logical-resource-id DBSubnetGroup \
--query "StackResourceDetail.PhysicalResourceId" --output text

Then execute below to restore snapshots
$ aws rds restore-db-instance-from-db-snapshot \
--db-instance-identifier awsinaction-db-restore \
--db-snapshot-identifier wordpress-manual-snapshot \
--db-subnet-group-name $SubnetGroup 

Can also restore from the backup retention period to the last five minutes 

Copy snapshots to another region
$ aws rds copy-db-snapshot --source-db-snapshot-identifier \
arn:aws:rds:us-east-1:$AccountId:snapshot:\
wordpress-manual-snapshot --target-db-snapshot-identifier \
wordpress-manual-snapshot --region eu-west-1


# Access to Database

IAM Roles 
Grant all access to RDS actions
{
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "Stmt1433661637000",
        "Effect": "Allow",
        "Action": "rds:*",
        "Resource": "*"
    }]
}

Deny destructive actions

{
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "Stmt1433661637000",
        "Effect": "Deny",
        "Action": ["rds:Delete*", "rds:Remove*"],
        "Resource": "*"
    }]
}


Network access via security group

DatabaseSecurityGroup:
Type: 'AWS::EC2::SecurityGroup'
Properties:
    GroupDescription: 'awsinaction-db-sg'
    VpcId: !Ref VPC
    SecurityGroupIngress:
    - IpProtocol: tcp
    FromPort: 3306
    ToPort: 3306
    SourceSecurityGroupId: !Ref WebServerSecurityGroup


# Highly Available Database

## Highly Available MultiAZ
AWS RDS lets yuo launch highly available databases
- Consisting of a master one
- And a standby database 

Just add below under properties 
MultiAZ: true

## Creating Read Replica
aws rds create-db-instance-read-replica \
--db-instance-identifier awsinaction-db-read \
--source-db-instance-identifier $DBInstanceIdentifier 

RDS automatically triggers the following steps in the background:
1 Creating a snapshot from the source database, also called the master database
2 Launching a new database based on that snapshot
3 Activating replication between the master and read-replication databases
4 Creating an endpoint for SQL read requests to the read-replication database


## Monitoring a Database
