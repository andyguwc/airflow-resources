# ECS

## Why ECS
Amazon ECS eliminates the need for you to install, operate, and scale your own cluster management infrastructure. The reason you might use Docker-based containers over traditional virtual machine-based application deployments is that it allows a faster, more flexible, and still very robust immutable deployment pattern in comparison with services such as traditional Elastic Beanstalk, OpsWorks, or native EC2 instances.

The reason you might use ECS or Elastic Beanstalk containers with EC2 Container Registry over similar offerings such as Docker Hub or Docker Trusted Registry is higher performance, better availability, and lower pricing. In addition, ECR utilizes other AWS services such as IAM and S3, allowing you to compose more secure or robust patterns to meet your needs.


## ECS Components
Assumes a ECR Repo increated and image pushed to ECR 

ECS Cluster – “An ECS cluster is a logical grouping of container instances that you can place tasks on.” With an ECS cluster, you can manage multiple services

ECS Service – With an ECS service, you can run a specific number of instances of a task definition simultaneously in an ECS cluster 
- Needs to define these 
    - Define ideal number of instances
    - Task 
    - Load balancer (& optional auto scale group)
- If you specify count as one and kill the docker container, the service will restart one to make sure always one is running. While a task without service will disappear after finished running

ECS Task Definition – A task definition is the core resource within ECS. 
- This is where you define which Docker images to run, CPU/Memory, ports, commands and so on. 
- Everything else in ECS is based upon the task definition. 
- Can think of a docker-compose file
- Can create new revisions of the task 


Creation Steps: 
- Create ECS Cluster with 1 Container Instance
- Create a Task Definition
- Create an ELB and Target Group to later associate with the ECS Service
- Create a Service that runs the Task Definition
- Confirm Everything is Working
- Scale Up the Service to 4 Tasks.


## CloudFormation 
Reference https://stelligent.com/2016/05/26/automating-ecs-provisioning-in-cloudformation-part-1/

Cluster depends on
- VPC
Service depends on
- VPC
- Cluster
- Load Balancer (optional)
- Task Definition
Task depends on
- VPC
- Container Image

Also needs IAM role and security group 


"EcsCluster":{
      "Type":"AWS::ECS::Cluster",
      "DependsOn":[
        "MyVPC"
      ]
    },

"EcsService":{
    "Type":"AWS::ECS::Service",
    "DependsOn":[
    "MyVPC",
    "ECSAutoScalingGroup"
    ],
    "Properties":{
    "Cluster":{
        "Ref":"EcsCluster"
    },
    "DesiredCount":"1",
    "DeploymentConfiguration":{
        "MaximumPercent":100,
        "MinimumHealthyPercent":0
    },
    "LoadBalancers":[
        {
        "ContainerName":"php-simple-app",
        "ContainerPort":"80",
        "LoadBalancerName":{
            "Ref":"EcsElb"
        }
        }
    ],
    "Role":{
        "Ref":"EcsServiceRole"
    },
    "TaskDefinition":{
        "Ref":"PhpTaskDefinition"
    }
    }
},

PhpTaskDefinition":{
      "Type":"AWS::ECS::TaskDefinition",
      "DependsOn":[
        "MyVPC"
      ],
      "Properties":{
        "ContainerDefinitions":[
          {
            "Name":"php-simple-app",
            "Cpu":"10",
            "Essential":"true",
            "Image":{
              "Fn::Join":[
                "",
                [
                  {
                    "Ref":"AWS::AccountId"
                  },
                  ".dkr.ecr.us-east-1.amazonaws.com/",
                  {
                    "Ref":"ECSRepoName"
                  },
                  ":",
                  {
                    "Ref":"ImageTag"
                  }
                ]
              ]
            },
            "Memory":"300",
            "PortMappings":[
              {
                "HostPort":80,
                "ContainerPort":80
              }
            ]
          }
        ],
        "Volumes":[
          {
            "Name":"my-vol"
          }
        ]
      }
    },

## Logging and Debugging 

Set up CloudWatch Logs
Write aws log configs 
Define log groups 


Checking Status 
SSH into the EC2 (ECS)
Run $ docker ps 


Checking the logs
Once SSH into the EC2 (ECS), run below to see logs (location depends on the mounting dir)
$ ls -l /var/log/ecs 


## Customizing ECS
cloudformation init (cfn-init)
integrate 


## Resources
ECS and CloudFormation
https://stelligent.com/2016/05/26/automating-ecs-provisioning-in-cloudformation-part-1/

Docker on AWS
https://github.com/docker-production-aws/aws-starter