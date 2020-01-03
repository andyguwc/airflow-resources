
# VPC

## Concepts
https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html

Amazon VPC is the networking layer for Amazon EC2. If you're new to Amazon EC2, see What is Amazon EC2? in the Amazon EC2 User Guide for Linux Instances to get a brief overview.

The following are the key concepts for VPCs:

A virtual private cloud (VPC) is a virtual network dedicated to your AWS account.

A subnet is a range of IP addresses in your VPC. Subnets enable you to group instances based on your security and operational needs. A public subnet is a subnet that has access to the Internet through an Internet gateway.

A route table contains a set of rules, called routes, that are used to determine where network traffic is directed.

An internet gateway is a horizontally scaled, redundant, and highly available VPC component that allows communication between instances in your VPC and the internet. It therefore imposes no availability risks or bandwidth constraints on your network traffic.

A VPC endpoint enables you to privately connect your VPC to supported AWS services and VPC endpoint services powered by PrivateLink without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection. Instances in your VPC do not require public IP addresses to communicate with resources in the service. Traffic between your VPC and the other service does not leave the Amazon network.


# Security Group 

A security group acts as a virtual firewall to control the traffic for its associated instances. To use a security group, you add the inbound rules to control incoming traffic to the instance, and outbound rules to control the outgoing traffic from your instance. To associate a security group with an instance, you specify the security group when you launch the instance. If you add and remove rules from the security group, we apply those changes to the instances associated with the security group automatically.

Your VPC comes with a default security group. Any instance not associated with another security group during launch is associated with the default security group.


## Security Group Basics
Limiting ports close down many security loopholes and prevent acccidental sending emails using SMTP for example
- HTTP traffic port 80
- HTTPS traffic port 443

Inbound security-group rules filter traffic based on its source. The source is either an
IP address or a security group. Thus you can allow inbound traffic only from specific
source IP address ranges.

Outbound security-group rules filter traffic based on its destination. The destination
is either an IP address or a security group. You can allow outbound traffic to only specific
destination IP address ranges.

SSH Only Security Group (name ssh-only)
- Type SSH, Protocol TCP, Port Range 22, Source Anywhere 

HTTP and SSH (name webserver)
- SSH TCP 22 0.0.0.0/0
- HTTP TCP 80 0.0.0.0/0 

Security Group consists of rules based on the following
- Direction (inbound or outbound)
- IP protocol (TCP, UDP, ICMP)
- Port
- Source/destination based on IP address, address range, or security group


## Security Group vs. ACL 

Security groups: Security groups act as a firewall for associated Amazon EC2 instances, controlling both inbound and outbound traffic at the instance level. When you launch an instance, you can associate it with one or more security groups that you've created.

Network access control lists (ACLs): Network ACLs act as a firewall for associated subnets, controlling both inbound and outbound traffic at the subnet level. 


## Associate Security Groups with EC2 Instances
Example of allowing SSH traffic
https://github.com/AWSinAction/code2/blob/master/chapter06/firewall3.yaml


```
Resources:
  SecurityGroup:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: 'Learn how to protect your EC2 Instance.'
      VpcId: !Ref VPC
      Tags:
      - Key: Name
        Value: 'AWS in Action: chapter 6 (firewall)'
      # allowing inbound ICMP traffic
      SecurityGroupIngress:
      - IpProtocol: icmp
        FromPort: '-1'
        ToPort: '-1'
        CidrIp: '0.0.0.0/0'
      # allowing inbound SSH traffic
      - IpProtocol: tcp
        FromPort: '22'
        ToPort: '22'
        CidrIp: '0.0.0.0/0'
  Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: !FindInMap [RegionMap, !Ref 'AWS::Region', AMI]
      InstanceType: 't2.micro'
      KeyName: !Ref KeyName
      SecurityGroupIds:
      - !Ref SecurityGroup
      SubnetId: !Ref Subnet
      Tags:
      - Key: Name
        Value: 'AWS in Action: chapter 6 (firewall)'
```


## Define Rules between Security Groups
We can control network traffic based on whether the source or destination belongs to a specific security group.
For example, a MySQL database can only be accessed if the traffic comes from your web servers, or that only your proxy servers are allowed to access the web servers 

Example of bastion host 
- Only one virtual machine, the bastion host, can be accessed via SSH from the internet
- All other virtual machines can only be reached via SSH from the bastion host 
- To implement the concept of a bastion host, you must follow these two rules:
    - Allow SSH access to the bastion host from 0.0.0.0/0 or a specific source address.
    - Allow SSH access to all other virtual machines only if the traffic source is the bastion host.
https://github.com/AWSinAction/code2/blob/master/chapter06/firewall5.yaml

```
# security group attached to the host
SecurityGroupBastionHost:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
        GroupDescription: 'Allowing incoming SSH and ICPM from anywhere'
        VpcId: !Ref VPC 
        SecurityGroupIngress:
        - IpProtocol: icmp
          FromPort: "-1"
          ToPort: "-1"
          CidrIP: '0.0.0.0/0'
        - IpProtocol: tcp 
          FromPort: '22'
          ToPort: '22'
          CidrIP: !Sub '${IpForSSH}/32'

# security group attached to the instance
SecurityGroupInstance:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
        GroupDescription: 'Allowing incoming SSH from the Bastion Host.'
        VpcId: !Ref VPC
        SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: '22'
          ToPort: '22'
          SourceSecurityGroupId: !Ref SecurityGroupBastionHost
```



# Subnets

## Public & Private Subnets
Subnets allow you to separate concerns. Create a separate subnet for your databases,
web servers, proxy servers, or application servers, or whenever you can separate
two systems. 

Another rule of thumb is that you should have at least two subnets: public
and private. A public subnet has a route to the internet; a private subnet doesn’t. Your
load balancer or web servers should be in the public subnet, and your database should
reside in the private subnet.

Example Implementation 
You’ll also create a private subnet for your web servers and one public subnet for your
proxy servers. The proxy servers absorb most of the traffic by responding with the latest
version of the page they have in their cache, and they forward traffic to the private
web servers. You can’t access a web server directly over the internet—only through the
web caches.

The VPC uses the address space 10.0.0.0/16. To separate concerns, you’ll create
two public subnets and one private subnet in the VPC:
- 10.0.1.0/24 public SSH bastion host subnet
- 10.0.2.0/24 public Varnish proxy subnet
- 10.0.3.0/24 private Apache web server subnet



# Networking Components

## Network Interfaces
An elastic network interface (referred to as a network interface in this documentation) is a virtual network interface that can include the following attributes:
a primary private IPv4 address
one or more secondary private IPv4 addresses
one Elastic IP address per private IPv4 address
one public IPv4 address, which can be auto-assigned to the network interface for eth0 when you launch an instance
one or more IPv6 addresses
one or more security groups
a MAC address
a source/destination check flag
a description


## Route Tables 
https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html

Contains a set of rules, called routes, that are used to determine where network traffic from your subnet or gateway is directed

Route Table Concepts
The following are the key concepts for route tables.
- Main route table—The route table that automatically comes with your VPC. It controls the routing for all subnets that are not explicitly associated with any other route table.
- Custom route table—A route table that you create for your VPC.
- Route table association—The association between a route table and a subnet, internet gateway, or virtual private gateway.
- Subnet route table—A route table that's associated with a subnet.
- Gateway route table—A route table that's associated with an internet gateway or virtual private gateway.
- Local gateway route table—A route table that's associated with an Outposts local gateway. For information about local gateways, see Local Gateways in the AWS Outposts User Guide.
- Destination—The destination CIDR where you want traffic to go. For example, an external corporate network with a 172.16.0.0/12 CIDR.
- Target—The target through which to send the destination traffic; for example, an internet gateway.
- Local route—A default route for communication within the VPC.


Each route in a table specifies a destination and a target. For example, to enable your subnet to access the internet through an internet gateway, add the following route to your subnet route table.

Destination	Target
0.0.0.0/0	igw-12345678901234567
The destination for the route is 0.0.0.0/0, which represents all IPv4 addresses. The target is the internet gateway that's attached to your VPC.

CIDR blocks for IPv4 and IPv6 are treated separately. For example, a route with a destination CIDR of 0.0.0.0/0 does not automatically include all IPv6 addresses. You must create a route with a destination CIDR of ::/0 for all IPv6 addresses.

## Internet Gateways
https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html

An internet gateway is a horizontally scaled, redundant, and highly available VPC component that allows communication between instances in your VPC and the internet. It therefore imposes no availability risks or bandwidth constraints on your network traffic.

An internet gateway serves two purposes: to provide a target in your VPC route tables for internet-routable traffic, and to perform network address translation (NAT) for instances that have been assigned public IPv4 addresses.

To enable access to or from the internet for instances in a VPC subnet, you must do the following:
- Attach an internet gateway to your VPC.
- Ensure that your subnet's route table points to the internet gateway.
- Ensure that instances in your subnet have a globally unique IP address (public IPv4 address, Elastic IP address or IPv6 address).
- Ensure that your network access control and security group rules allow the relevant traffic to flow to and from your instance.


## NAT
You can use a NAT device to enable instances in a private subnet to connect to the internet (for example, for software updates) or other AWS services, but prevent the internet from initiating connections with the instances. A NAT device forwards traffic from the instances in the private subnet to the internet or other AWS services, and then sends the response back to the instances. When traffic goes to the internet, the source IPv4 address is replaced with the NAT device’s address and similarly, when the response traffic goes to those instances, the NAT device translates the address back to those instances’ private IPv4 addresses.

