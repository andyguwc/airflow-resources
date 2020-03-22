# CLI Basics

## Install and Configure
$ sudo pip install awscli 
$ aws --version 

Make sure you add a user "mycli" under IAM
- with programmatic access 
- AdministratorAccess policy attached

Configure with access key, secret key, default region name, and output format 
$ aws configure 

# Commands 

## General Format 
General format is 
aws <service> <action> [--key value ...]
aws <service> help 
aws <service> <action> help 

aws ec2 describe-regions --output table 

Query format is JMESPath 

$ aws ec2 describe-images --query "Images[0].ImageId"
$ aws ec2 describe-images --query "Images[0].ImageId" --output text
$ aws ec2 describe-images --query "Images[*].State"

## Common Commands
Get a list of available regions
$ aws ec2 describe-regions

Get a list of running EC2 isntances of type t2.micro 
$ aws ec2 describe-instances --filters "Name=instance-type,Values=t2.micro" 

$ aws ec2 run-instances --image-id ami-xxx --instance-type t2.micro --key-name norcal

$ aws ec2 describe-instances --instance-ids --query 'Reservations[].Instances[].State'

$ aws ec2 create-tags --resources i-xxx --tags "Key=Name, Value=xxx"

$ aws s3 mb s3:// 



# Applications

## Script to Create a Temp Instance for Testing 
- a script to create a new virtual machine, connect to it, and run some tests and terminate
- run below and press Enter to terminate 
chmod +x virtualmachine.sh && ./virtualmachine.sh 

