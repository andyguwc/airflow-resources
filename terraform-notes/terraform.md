

# Overview of Terraform 

AWS Authentication
https://blog.gruntwork.io/a-comprehensive-guide-to-authenticating-to-aws-on-the-command-line-63656a686799

Declarative Approach
With Terraform’s declarative approach, the code always represents the latest state of your infrastructure.

Idempotent - if applied multiple times, the infrastructure should be the same 

Automating infrastruture deployment 
- Provisioning resources
- Planning updates
- Reusing templates 

Benefits:
- Automated deployment
- Consistent environment 
- Repeatable process
- Reusable components 
- Documented architecture



# Terraform Components Provisioning Resources
Terraform executable 
Terraform file 

## Variable
Variable to store access key information 

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_region" {
    default = "us-east-1"
}

## Provider 
provider "aws" {
    access_key = "var.access_key"
    secret_key = "var.secret_key"
    region = "var.aws_region"
}


## Resources
An instance to host web components
Example AWS instance to run nginx
resource "aws_instance" "nginx" {
    ami = "ami-etterewtrre"
    instance_type = "t2.micro"
    key_name = "${var.key_name}"
}

Provisioner 
Remote or not provisioner 

## Output 
get things out of the deployment 

output "aws_public_ip" {
    value = 
    "${aws_instance.ex.public_dns}"
}

Integrate multiple providers

## CLI 
Store the vars in another directory and import via CLI
plan -var-file-'../terraform.tfvars'
apply ...
destroy ... 


# Updating Configuration 

## State 
Terraform maintains a state file 
- JSON file 
- Do not edit 
- Resource mappings (dependency tree) and metadata 

When deploying new instances
- the state file become locked (the state file stored in a remote location)
- multiple environments (dev vs. prod)


## Terraform Plan
$ terraform plan -out m3.tfplan 
$ terraform apply "m3.tfplan"
$ terraform destroy 

Run the plan and store it in a file to reference 
Tells us which resources will be created 

Terraform planning 
- inspect state 
- refresh state 
- dependency graph 
- additions, updates, and deletions 
- parallel execution of apply 
- save the plan


## Example - Adding VPC and Scaling 

add VPC
add internet gateway
add subnets
add route table
add route table association

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


## Example - Scaling with Load Balancer 

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


- Configuration file is converted to JSON 
- Interpolation 
- Conditional, function, template


# Variable

## Variable Syntax
variable var_name {
    key = value 
}

Use a variable 
var.<VARIABLE_NAME>
interpolation syntax ${}
${var.name} # get string
${var.map["key"]} # get map element 
${var.list[idx]} # get list element

Create a provider 
prover provider_name {
    key = value # depends on the resource
}

Provide a value via the -var command-line
terraform plan -var "server_port=8080"

Can also set the variable via an environment variable TF_VAR_<name>
$ export TF_VAR_server_port=8080
$ terraform plan

Default value 
variable "server_port" {
    description = "port the server will use"
    type = number 
    default = 8080
}

## Variables and Multiple States 
- name, type, default 
- multiple sources 
    - File, environment variable, var option (at command line)
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


# Output 

## Output Syntax
output "public_ip" {
  value       = aws_instance.example.public_ip
  description = "The public IP address of the web server"
}


# Resource 
resource resource_type resource_name {
    key = value 
}

## Reference resource
${resource_type.resource_name.attribute(args)}
${aws_instance.test_instance.name}

Example Web Server and Security Group
resource "aws_instance" "app" {
  instance_type     = "t2.micro"
  availability_zone = "us-west-2a"
  ami               = "ami-04590e7389a6e577c"
  vpc_security_group_ids = [aws_security_group.instance.id]
  user_data = <<-EOF
              #!/bin/bash
              echo "Hello, World" > index.html
              nohup busybox httpd -f -p 8080 &
              EOF
  tags = {
    Name = "terraform-example"
  }
}

resource "aws_security_group" "instance" {
  name = "terraform-example-instance"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
} 


# Data Object 
Create a data object 
data data_type data_name {}

Use data object 
${data_type.data_name.attribute(args)}


# Deploy Environments
- Commonality and differences
- abstractions and reuse 
- production access 
- Using workspaces

State file for each environment (or even application in environment)
- running terraform plan for development 
- store variables data 
- terraform plan -state=".\dev\dev.state" -var-file="common.tfvars" -var-file=".\dev\dev.tfvars"

## Workspace 
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

## Multi Providers

Azure provider 

Azure RM DMS resource 

 
# Terraform CLI

configuration command 
terraform init 


# Terraform State
Every time you run Terraform, it records information about what infrastructure it created in a Terraform state file. By default, when you run Terraform in the folder /foo/bar, Terraform creates the file /foo/bar/terraform.tfstate. This file contains a custom JSON format that records a mapping from the Terraform resources in your configuration files to the representation of those resources in the real world.

## Why Remote State 

Problems
- Shared storage for state files
To be able to use Terraform to update your infrastructure, each of your team members needs access to the same Terraform state files. That means you need to store those files in a shared location.

- Locking state files
As soon as data is shared, you run into a new problem: locking. Without locking, if two team members are running Terraform at the same time, you can run into race conditions as multiple Terraform processes make concurrent updates to the state files, leading to conflicts, data loss, and state file corruption.

- Isolating state files
When making changes to your infrastructure, it’s a best practice to isolate different environments. For example, when making a change in a testing or staging environment, you want to be sure that there is no way you can accidentally break production. But how can you isolate your changes if all of your infrastructure is defined in the same Terraform state file?


Solution - Terraform Remote State
- A Terraform backend determines how Terraform loads and stores state. The default backend, which you’ve been using this entire time, is the local backend, which stores the state file on your local disk. Remote backends allow you to store the state file in a remote, shared store.
- After you configure a remote backend, Terraform will automatically load the state file from that backend every time you run plan or apply and it’ll automatically store the state file in that backend after each apply, so there’s no chance of manual error.
- Locking - Most of the remote backends natively support locking. To run terraform apply, Terraform will automatically acquire a lock; if someone else is already running apply, they will already have the lock, and you will have to wait.


## Enable Remote State Storage 

- Set up s3 bucket 
resource "aws_s3_bucket" "terraform_state" {

  bucket = var.bucket_name

  // This is only here so we can destroy the bucket as part of automated tests. You should not copy this for production
  lifecycle {
    prevent_destroy = true 
  }

  // Enable versioning so we can see the full revision history of our state files
  versioning {
    enabled = true
  }

  // Enable server-side encryption by default
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

- Configure terraform backend 
To configure Terraform to store the state in your S3 bucket (with encryption and locking), you need to add a backend configuration to your Terraform code. This is configuration for Terraform itself, so it resides within a terraform block, and has the following syntax:
terraform {
  backend "<BACKEND_NAME>" {
    [CONFIG...]
  }
}
where BACKEND_NAME is the name of the backend you want to use (e.g., "s3") and CONFIG consists of one or more arguments that are specific to that backend (e.g., the name of the S3 bucket to use).

terraform {
  backend "s3" {
    # Replace this with your bucket name!
    bucket         = "terraform-up-and-running-state"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-2"

    # Replace this with your DynamoDB table name!
    dynamodb_table = "terraform-up-and-running-locks"
    encrypt        = true
  }
}


# Terraform Workspaces
Terraform workspaces allow you to store your Terraform state in multiple, separate, named workspaces.

Terraform workspace show 
default 

Teeraform switched to workspace "example1"
terraform workspace new example1 

terraform workspace list 

terraform workspace select example1

Inside each of those workspaces, Terraform uses the key you specified in your backend configuration, so you should find an example1/workspaces-example/terraform.tfstate and an example2/workspaces-example/terraform.tfstate.


# File Isolation
Put the terraform configuration files for each environment into a separate folder 

Configure a backend for each environment, using different authentication mechanisms and access controls 

Top level are different environments
- stage
- prod
- mgmt (environment for devops tooling)
- global (put resources across all environments)

Within each environment are different components
- VPC
- datas-storage
- services

Within each component
- inputs.tf
- outputs.tf
- main.tf



# Module 

- Abstracting common components
- Modules make code reuse easier 

Example VPC Module
- VPC
- Subnets
- Internet gateway
- Routing 

## Inputs 
Input variables can be used as parameters
And make sure the main.tf is using the vars instead of hard-coded names

The input variables are the API of the module, controlling how it will behave in different environments.


/modules/services/webserver-cluster/main.tf
variable "cluster_name" {
  description = "The name to use for all the cluster resources"
  type        = string
}

variable "db_remote_state_bucket" {
  description = "The name of the S3 bucket for the database's remote state"
  type        = string
}

variable "db_remote_state_key" {
  description = "The path for the database's remote state in S3"
  type        = string
}

in staging environment, set the new input variables accordingly 

/stage/services/webserver-cluster/main.tf
module "webserver_cluster" {
  source = "../../../modules/services/webserver-cluster"

  cluster_name           = "webservers-stage"
  db_remote_state_bucket = "(YOUR_BUCKET_NAME)"
  db_remote_state_key    = "stage/data-stores/mysql/terraform.tfstate"
}

## Locals
instead of using input variables (which people can overwrite accidentally)
define local values instead
locals {
  http_port    = 80
  any_port     = 0
  any_protocol = "-1"
  tcp_protocol = "tcp"
  all_ips      = ["0.0.0.0/0"]
}

## Outputs
Access output variables using module.<MODULE_NAME>.<OUTPUT_NAME>
output "asg_name" {
  value       = aws_autoscaling_group.example.name
  description = "The name of the Auto Scaling Group"
}

module.frontend.asg_name

resource "aws_autoscaling_schedule" "scale_out_during_business_hours" {
  scheduled_action_name = "scale-out-during-business-hours"
  min_size              = 2
  max_size              = 10
  desired_capacity      = 10
  recurrence            = "0 9 * * *"

  autoscaling_group_name = module.webserver_cluster.asg_name
}


## Source
github repo source

Here is what that would look like in live/stage/services/webserver-cluster/main.tf if your modules repo was in the GitHub repo github.com/foo/modules (note that the double-slash in the following Git URL is required):
module "webserver_cluster" {
  source = "github.com/foo/modules//webserver-cluster?ref=v0.0.1"

  cluster_name           = "webservers-stage"
  db_remote_state_bucket = "(YOUR_BUCKET_NAME)"
  db_remote_state_key    = "stage/data-stores/mysql/terraform.tfstate"

  instance_type = "t2.micro"
  min_size      = 2
  max_size      = 2
}

The ref parameter allows you to specify a particular Git commit via its sha1 hash, a branch name, or, as in this example, a specific Git tag


## Example S3 Module

Terraform Modules
- Code reuse
- Remote or local sources
    - Terraform registry
- Root module
    - Support versioning 
- Provider inheritance 

Any set of terraform configuration files in a folder is a module 



## Example Module
Modules
- /s3 
    - main.tf
    - outputs.tf
    - variables.tf

Name assigned to the S3 bucket
The s3 module as below 

variable "name" {}

resource "aws_s3_bucket" "bucket" {
    name = var.name
}

output "bucket_id" {
    value = aws_s3_bucket.bucket.id
}

Create module bucket 
So we can refer to it 
module "bucket" {
    name = "taco-bucket"
    source = ".\\Modules\\s3"
}

Use taco-bucket
resource "aws_s3_bucket_object" {
    bucket = module.bucket.bucket_id
}


# Terraform Functions

## Count 
Terraform resource has a meta parameter called count 

resource "aws_iam_user" "example" {
  count = 3
  name  = "neo"
}

resource "aws_iam_user" "example" {
  count = 3
  name  = neo.${count.index}
}

## Array Lookup 
variable "user_names" {
    description = "Create IAM users with these names" 
    type = list(string)
    default = ["neo", "trinity", "morpheus"]
}

resource "aws_iam_user" "example" {
    count = length(var.user_names)
    name = var.user_names[count.index]
}

once using count on a resource it becomes an array of resources rather than just one resource. Need to specify its index 

output "neo_arn" {
    value = aws_iam_user.example[0].arn
    description = "The ARN for user Neo" 
}

output "all_arns" {
    value = aws_iam_user.example[*].arn
    description = "The ARN for all users"
}

limitations with arrays 
- terraform identifies each resources within the array by its position (index)
- if you remove an item, all the items will shift 
- instead can use for_each 

## For each
resource "aws_iam_user" "example" {
    for_each = toset(var.user_names)
    name = each.value 
}

## For Loop

variable "names" {
  description = "A list of names"
  type        = list(string)
  default     = ["neo", "trinity", "morpheus"]
}

output "upper_names" {
  value = [for name in var.names : upper(name)]
}

can also filter by if condition
output "short_upper_names" {
    value = [for name in var.names: upper(name) if length(name) <5]
}


## Loops with String Directives 
%{for <ITEM> in <COLLECTION>}<BODY>% { endfor }

variable "names" {
    description = "Name to render"
    type = list(string)
    default = ["neo", "trinity", "morpheus"]
}

output "for_directive" {
    value = <<EOF
    %{for name in var.names}
        ${name}
    %{endfor}
    EOF
}


conditions
extract just the first character from var.instance_type
count = format("%.1s", var.instance_type) == "t" ? 1:0



## Function categories
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


## Resource arguments 
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

## File 
data "template_file" "user_data" {
  template = file("user-data.sh")

  vars = {
    server_port = var.server_port
    db_address  = data.terraform_remote_state.db.outputs.address
    db_port     = data.terraform_remote_state.db.outputs.port
  }
}

