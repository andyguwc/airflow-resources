# EC2 Basics

## Launch Steps
- Select an OS (AMI)
- Choose Size of machine
- Confugring network details
- Adding storage
- Tagging 
- Configuring a firewall (security group)
- Select key pair used for SSH authentication 

## AMI 
- AMI contains an OS, additional software, and configuration
- AWS offers the Amazon Linux AMI, which is based on Red Hat Enterprise Linux and optimized for use with EC2

## Basic Settings
- VPC use default
- Security group use SSH Only 


# SSH Connecting 
- Console
    - Click instance and find the "Connect" tab which has details on command 
- Command
$ ssh -i $PathToKey/mykey.pem xx@xxxx.compute-1.amazonaws.com 

Add the key to SSH agent
ssh-add $PathToKey/mykey.pem
ssh ec2-user@xxxx

Enable AgentForwarding with -A 

ssh -A ec2-user@$BastionHostPublicName
Let you authenticate via the same key you used to log in to the bastion host for further SSH logins initiated from the host

- Installing and Running Software
Ubuntu 
$ sudo apt-get update 
$ sudo apt-get install xxx

Amazon Linux (CentOS)
$ sudo yum update 
$ sudo yum install 

- Install and start the web server
$ sudo yum install httpd -y
$ sudo service httpd start 

- Configure the web server 
add a file named a.conf under /etc/httpd/conf.d with content
<VirtualHost 172.31.x.x:80>
DocumentRoot /var/www/html/a
</VirtualHost>

then activate by 
$ sudo service httpd restart

- Check the machine's capabilities
First use ssh to connect then run 
$ cat /proc/cpuinfo 
$ free -m 

- See network interfaces attached to the virtual machine
$ ifconfig

- Check security updates 

$ yum --security check-update 


# Monitoring and Managing

- Monitor 
    - See logs: Choose instance settings -> get system log 
    - Monitor CPU: CPU, network, disk usage 

- Manage States
    - Stop
        - can be started again but likely on a different host 
    - Terminate
        - deleted together with network-attached storage and public and private IP addresses 
    - Start

- Modify Instance Settings
    - First stop it 
    - Choose Change Instance Type from the Actions menu under Instance Settings
    - Select new isntance type and apply 


# Allocate Public IP Address
- If need to host an pplication under a fixed IP address, use Elastic IPs

- Choose Elastic IPs from EC2 service 
- Allocate new address 
- Select the public IP and choose Associate Address from the Actions menu 
    - Resource type choose instance
    - Instance choose the ID of the virtual machine 
    - Select the private IP address 


# Applications

## Simple Web Server

AMI - Amazon Linuz AMI 

Security group - HTTP and SSH 
- SSH TCP 22 0.0.0.0/0
- HTTP TCP 80 0.0.0.0/0 

Connect to EC2 Instance via SSH 
- Install web server
$ sudo yum install httpd -y
- Start the web server 
$ sudo service httpd start 
- Direct to $PublicIP should see a placeholder site 

Allocate a fixed public IP address via Elastic IP

(optional) Can add an additional network interface
- put in the same subnet the EC2 is using 
- leave private IP address empty (auto-assigned)
- choose the same security group 

(optional) Then associate a second IP address with the new network interface
- from new Elastic IP choose associate address
    - resource type choose network interface 



## Provision a Working Web Server
Using user data to run a script on startup 
- executed at the end of the boot process 