
# AWS Services for Wordpress App 
Elastic Load Balancing (ELB)
- The load balancer distributes traffic to a bunch of virtual machines, and is highly available by default. Requests are routed to virtual machines as long as their health check succeeds.

EC2 
- The EC2 service provides virtual machines. You’ll use a Linux machine with an optimized distribution called Amazon Linux to install Apache, PHP, and WordPress. You aren’t limited to Amazon Linux; you could also choose Ubuntu, Debian, Red Hat, or Windows. Virtual machines can fail, so you need at least two of them. The load balancer will distribute the traffic between them.

RDS for MySQL
- You choose the database size (storage, CPU, RAM), and RDS takes over operating tasks like creating
backups and installing patches and updates. RDS can also provide a highly available MySQL database by replication.

Elastic File System 
- Elastic File System (EFS)—WordPress itself consists of PHP and other application files. User uploads, for example images added to an article, are stored as files as well. By using a network file system, your virtual machines can access these files. EFS provides a scalable, highly available, and durable network filesystem using the NFSv4.1 protocol.

Security groups
- Control incoming and outgoing traffic to your virtual machine, your database, or your load balancer with a firewall. For example, use a security group allowing incoming HTTP traffic from the internet to port 80 of the load balancer. Or restrict network access to your database on port 3306 to the virtual machines running your web servers.


# CloudFormation 

## Steps 
- create a load balancer (ELB)
- create a MySQL database (RDS)
- create a networking filesystem (EFS)
- create and attach firewall rules (security groups)
- create virtual machines running web servers
    - Create EC2
    - Mount the network filesystem
    - Install Apache and PHP
    - Download and extract Wordpress
    - Configure it to use MySQL
    - Start the Apache web server 
- the deletion is also automated 

## Create CloudFormation Template
- CloudFormation create a stack 
    - Input needs Template (can be a s3 location or a local file) 

- Make sure to tag (like system:wordpress) so we can find the resource better 
    - Use tags to differentiate between testing and production resources 

- Create a resource group to filter for those with system:wordpress tag

## EC2 
- Instance type—Tells you about how powerful your EC2 instance is. You’ll learn
more about instance types in chapter 3.
- IPv4 Public IP—The IP address that is reachable over the internet. You can use
that IP address to connect to the virtual machine via SSH.
- Security groups—If you click View Rules, you’ll see the active firewall rules, like
the one that enables port 22 from all sources (0.0.0.0/0)
- AMI ID—If you click the AMI ID, you’ll see the version number of the OS, among other things.

## Load Balancer
- The load balancer forwards incoming requests to one of your virtual machines. A target group is used to define the targets for a load balancer. The load balancer performs health checks to ensure requests are routed to healthy
targets only.
- Use the DNS name to connect to the Load Balancer 

## MySQL RDS
- Engine
- Storage Type - Magnetic (normal) or SSD (better performance)
- Automated Backups (enabled or disabled)
- Maintenance Window

## EFS
- To mount the Elastic File System from a virtual machine, mount targets are needed. You should use two mount targets for fault tolerance. 
- The network filesystem is accessible using a DNS name for the virtual machines.


