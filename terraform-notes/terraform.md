

# Overview of Terraform 

Automating infrastruture deployment 
- Provisioning resources
- Planning updates
- Reusing templates 

# Terraform Components Provisioning Resources
Terraform executable 
Terraform file 

Variable
Variable to store access key information 

Provider 
provider "aws" {
    access_key = "access_key"
    secret_key = "secret_key"
    region = "us-east-1"
}

Resources
An instance to host web components
Example AWS instance to run nginx
resource "aws_instance" "nginx" {
    ami = "ami-etterewtrre"
    instance_type = "t2.micro"
    key_name = "${var.key_name}"
}

Provisioner 
Remote or not provisioner 

Output 
output "aws_public_ip" {
    value = 
    "${aws_instance.ex.public_dns}"
}

Integrate multiple providers

CLI 
Store the vars in another directory and import via CLI
plan -var-file-'../terraform.tfvars'
apply ...
destroy ... 


# Updating Configuration 

Consistent and predictable updates 

Terraform maintains a state file 
- JSON file 
- Do not edit 
- Resource mappings (dependency tree) and metadata 

When deploying new instances
- the state file become locked (the state file stored in a remote location)
- multiple environments (dev vs. prod)

Terraform planning 
- inspect state 
- refresh state 
- dependency graph 
- additions and deletions 

Scaling 
- needs to add load balancer between DNS and servers 
- place subnets in separate availability zones and put instances in separate subnets 

Data Types and Security Groups

data "aws_availability_zones" 
"available" {}

resource "aws_subnet" "subnet1"
{
    cidr_block=
    "${var.subnet1_address_space}"
    vpc_id = "${aws_vpc.vpc.id}"
    availability_zone = 
    "${data.aws_availability_zones.available.names[0]}"
}

Once created the security group can assigned it to the elastic load balancer

resource "aws_security_group"
"elb-sg" {
    name="nginx_elb_sg"
    vpc_id = "${aws_vpc.vpc.id}"
    ingress {}
    egress {}
}

resource "aws_elb" "web" {
name = "nginx-elb"

    security_groups = 
    ["${aws_security_group.elb-sg.id}"]
}


Scaling 
First add networking then add subnets

resource "aws_vpc" "vpc" {
  cidr_block = "${var.network_address_space}"
  enable_dns_hostnames = "true"

}

resource "aws_internet_gateway" "igw" {
  vpc_id = "${aws_vpc.vpc.id}"

}

resource "aws_subnet" "subnet1" {
  cidr_block        = "${var.subnet1_address_space}"
  vpc_id            = "${aws_vpc.vpc.id}"
  map_public_ip_on_launch = "true"
  availability_zone = "${data.aws_availability_zones.available.names[0]}"
}

set up routing table 
resource "aws_route_table" "rtb" {
  vpc_id = "${aws_vpc.vpc.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.igw.id}"
  }
}

resource "aws_route_table_association" "rta-subnet1" {
  subnet_id      = "${aws_subnet.subnet1.id}"
  route_table_id = "${aws_route_table.rtb.id}"
}


Will automatically create terraform.tfstate file
- JSON file you should not touch 
- automatically creates dependencies (instance depends on subnet and security group, etc.)

When running update
- terraform calculates the changes to be made 


# Configure Resources After Creation 

After resources are created you want to take additional actions 
- make html into S3 to load into instances 
- consolidate log files into S3 

Terraform Provisioners
- multiple uses (local/remote)
- creation or destruction 

Multiple provisioners
- if something goes wrong, flag the resource as tainted and clean up afterwards 

local exec provisioner runs a command locally 

provisioner "local-exec" {
    command = "local command here"
}

provisioner "remote-exec" {
    scripts = "[list, of, local, scripts]"
}

# Terraform Syntax

- Configuration file is converted to JSON 
- Interpolation 
- Conditional, function, template

Create a variable 
variable var_name {
    key = value 
}

Use a variable (interpolation syntax ${})
${var.name} # get string
${var.map["key"]} # get map element 
${var.list[idx]} # get list element

Create a provider 
prover provider_name {
    key = value # depends on the resource
}

Create a data object 
data data_type data_name {}

Use data object 
${data_type.data_name.attribute(args)}

Create resource 
resource resource_type resource_name {
    key = value 
}

Reference resource
${resource_type.resource_name.attribute(args)}


To rotate files within S3, upload the S3 config file first 
- use provisionder "file"

Then create a second file on nginx log rotation 
- automatically upload logs from nginx to S3 
- upload sync commands to s3 bucket 

Run commands 
- provisioner "remote-exec
- install nginx 
- copy file from ec2 instance to a location
- install s3 command utility and run some s3 commands to copy to local home directory
- copy into nginx directory 

Create iam user for S3

Create actual S3 bucket 

Put object (html file etc.) into S3 bucket 


# Terraform Functions
Built-in to Terraform 

Test in terraform console 
- command console to let terraform evaluate functions 

Function categories
- Numeric 
- String 
- Collection 
- Filesystem 
- IP networking 
- Date and time 

Example: Configure Networking 
variable network_info {
    default = "10.1.0.0/16
}

Returns 10.1.0.0/24
cidr_block = cidrsubnet(var.network_info, 8,0)

Returns 10.1.0.5
host_ip = cidrhost(var.network_info, 5)

Example: Create ami maps 
variable "amis" {
    type = "map"
    default = {
        us-east-1 = "ami-1234"
        us-west-1 = "ami-5678"
    }
}

ami = lookup(var.amis, "us-east-1", "error")


Resource arguments 
- depends on 
- count 
- for each

resource "aws_instance" "taco_servers {
    count = 2
    tags {
        Name = "customer - ${count.index}"
    }

    depends_on = [aws_iam_role_policy.allow_s3]
}


resource "aws_s3_bucket" "taco_toppings" {
    for_each = {
        food = "public-read"
        cash = "private"
    }

    bucket = "${each.key} - ${var.bucket_suffix}"
    acl = each.value 
}

# Using Variables in Deployments
Dev, QA, production
- one configuration, multiple inputs and multiple environments as outpus


## Variables and multiple states 
- name, type, default 
- multiple sources 
    - File, environment variable, var option
- overriding variables and precendents
    - Environment < file < command line 


Specify default variable and type 

variable "environment_name" {
    type = string
    default = "development"
}

Specify variable in file 
environment_name = "uat"

Speicfy variable in-line (key=value)
terraform plan -var 'environment_name=production'


Create variable map 
variable "cidr" {
    type = map(string)
    default = {
        development = "10.0.0.0/16"
        uat = "10.1.0.0/16"
        production = "10.2.0.0/16"
    }
}

Use map based on environment 
cidr_block = lookup(var.cidr, var.environment_name)


## Multiple environments
- Commonality and differences
- abstractions and reuse 
- production access 
- Using workspaces


State file for each environment (or even application in environment)
- running terraform plan for development 
- terraform plan -state=".\dev\dev.state" -var-file="common.tfvars" -var-file=".\dev\dev.tfvars"


Workspace 
- place the state file in child direcory of dev 
- terrafoorm workspace new dev 
- terraform plan 


Deploy workspace
- initialize terraform configuration 
    - $ terraform workspace new Development 
    - $ terraform plan -out dev.tfplan to geenrate plan for workspace environment
- terraform apply 
    - this will deploy development environment 
- to deploy uat environment 
    - $ terraform workspace new UAT
    - $ terraform plan -out dev.uatplan

Credentials management 
- store in a variables file
- submit in a command line
- store within environment variables 
- use secrets management service (so terraform can retrieve dynamically)

- AWS environment variables
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY

- Secret management service (e.g. hashicorp vault)
    - terraform reaches out to vault and vault talks to AWS to provision credentials 


# Terraform CLI

configuration command 
terraform init 


# Multi Providers

Azure provider 

Azure RM DMS resource 

 
# Using a Module for Common Configurations

- Abstracting common components
- Modules make code reuse easier 

Example VPC Module
- VPC
- Subnets
- Internet gateway
- Routing 

Example S3 Module


Terraform Modules
- Code reuse
- Remote or local sources
    - Terraform registry
- Root module
    - Support versioning 
- Provider inheritance 

Name assigned to the S3 bucket
variable "name" {}

resource "aws_s3_bucket" "bucket" {
    name = var.name
}

output "bucket_id" {
    value = aws_s3_bucket.bucket.id
}

Create module bucket 
module "bucket" {

}

Use taco-bucket
resource "aws_s3_bucket_object" {
    bucket = module.bucket.bucket_id
}

Modules
- /s3 
    - main.tf
    - outputs.tf
    - varuables.tf




