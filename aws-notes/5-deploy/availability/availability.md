# Availability Zones

A VPC is bound to a region
A subnet within a VPC is linked to an availability zone
A virtual machine is launched into a single subnet 

Some services operate globally over multiple regions: Route 53 (DNS) and CloudFront (CDN).
- Some services use multiple availability zones within a region so they can recover from an availability zone outage: S3 (object store) and DynamoDB (NoSQL database).
- The Relational Database Service (RDS) offers the ability to deploy a masterstandby setup, called Multi-AZ deployment, so you can fail over into another availability zone with a short downtime if necessary.
- A virtual machine runs in a single availability zone. But AWS offers tools to build an architecture based on EC2 instances that can fail over into another availability zone.




# AutoScaling

Autoscaling ensures an EC2 instance is always running 
- make sure new instance is started if the original instance fails
- starting in multiple subnets. So in case of outage of an entire availability zone, a new instance can be launched in another subnet in another availability zone 

## Configure auto-scaling
To launch an auto-scaling group we need: 
- launch configuration specifying the AMI and instance type
- auto-scaling group tells EC2 how many VMs should be started 

Require properties
- LaunchConfiguration
    - ImageId
    - InstanceType
    - DesiredCapability 
- AutoScalingGroup
    - MinSize
    - MaxSize
    - VPCZoneIdentifier (subnet IDs you want to start virtual machines in)
    - HealthCheckType (health check used to identify failed virtual machines)


```
LaunchConfiguration:
Type: 'AWS::AutoScaling::LaunchConfiguration'
Properties:
    AssociatePublicIpAddress: true
    ImageId: !FindInMap [RegionMap, !Ref 'AWS::Region', AMI]
    InstanceMonitoring: false
    InstanceType: 't2.micro'
    KeyName: !Ref KeyName
    SecurityGroups:
    - !Ref SecurityGroup
    UserData:
    'Fn::Base64': !Sub |
        #!/bin/bash -x
        ...
AutoScalingGroup:
Type: 'AWS::AutoScaling::AutoScalingGroup'
Properties:
    LaunchConfigurationName: !Ref LaunchConfiguration
    Tags:
    - Key: Name
    Value: 'jenkins-multiaz'
    PropagateAtLaunch: true
    DesiredCapacity: 1
    MinSize: 1
    MaxSize: 1
    VPCZoneIdentifier:
    - !Ref SubnetA
    - !Ref SubnetB
    HealthCheckGracePeriod: 600
    HealthCheckType: EC2
CreationPolicy:
    ResourceSignal:
    Timeout: PT10M
DependsOn: VPCGatewayAttachment
```


# Network Interface Recovery 

Ensure Public IP is static with new VM instance. A few options:
- Allocate an Elastic IP, and associate this public IP address during the bootstrap of the virtual machine.
    - Basically gets the instance ID during VM start and allocate the Elastip IP with the virtual machine instance ID
- Create or update a DNS entry linking to the current public or private IP address of the virtual machine.
    - This can be achieved via Route 53 (DNS)
- Use an Elastic Load Balancer (ELB) as a static endpoint that forwards requests to the current virtual machine.



# Elastic Load Balancing 
