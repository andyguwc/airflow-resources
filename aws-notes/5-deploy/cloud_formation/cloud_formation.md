
# CloudFormation Basics

- Declarative approach 
    - tells CloudFormation how your infrastructure should look 
    - not telling what actions are needed to create that infrastructure and no specification on sequences

- Benefits
    - Consistent description of infrastructure on AWS
    - Can handle dependencies 
    - Replicable 
    - Customizable
    - Testable - just start a new infrastructure, run the tests, and shut it down 
    - Documentation for the infrastructure 


# CloudFormation Template 
Parameters—Parameters are used to customize a template with values: for example,
domain name, customer ID, and database password.

Resources—A resource is the smallest block you can describe. Examples are a virtual machine, a load balancer, or an Elastic IP address.

Outputs—An output is comparable to a parameter, but the other way around.
An output returns something from your template, such as the public name of an EC2 instance.

Example Templates
https://github.com/awslabs/aws-cloudformation-templates


## Parameter
Parameters:
    Demo:
        Type: Number 
        Description: 'This parameter is for demonstration'


Parameters:
    KeyName:
        Description: 'Key Pair name'
        Type: 'AWS::EC2::KeyPair::KeyName'
    NumberOfVirtualMachines:
        Description: 'How many virtual machine do you like?'
        Type: Number
        Default: 1
        MinValue: 1
        MaxValue: 5
    WordPressVersion:
        Description: 'Which version of WordPress do you want?'
        Type: String
     
        AllowedValues: ['4.1.1', '4.0.1']


## Resource
Resources:
    VM: (name or logical ID of the resource you can choose)
        Type: 'AWS::EC2::Instance' (defines an EC2 instance)
        Properties: (properties needed for the type of resource)
            ImageId: 'ami-xxxx'
            InstanceType: 't2.micro'
            KeyName: mykey
            NetworkInterfaes:
                - AssociatePublicIpAddress: true 
                DeleteOnTermination: true 
                DeviceIndex: 0 
                GroupSet:
                - 'sg-123'
                SubnetId: 'subnet-123'


## Functions
!Ref NameOfSomething (a placeholder for what is referenced by the name)

In the shell script
With !Sub, all references within ${} are substituted with their real value. The real value will be the value returned by !Ref, unless the reference contains a dot, in which case it will be the value returned by !GetAtt:
!Sub 'Your VPC ID: ${VPC}' # becomes 'Your VPC ID: vpc-123456'
!Sub '${VPC}' # is the same as !Ref VPC
!Sub '${VPC.CidrBlock}' # is the same as !GetAtt 'VPC.CidrBlock'
!Sub '${!VPC}' # is the same as '${VPC}'

The function !Base64 encodes the input with Base64. You’ll need this function because the user data must be encoded in Base64:
!Base64 'value' # becomes 'dmFsdWU='

## Outputs

Outputs:
    ID:
        Value: !Ref Server (references the EC2 instance)
        Description: 'ID of the EC2 instance'
    PublicName:
        Value: !GetAtt 'Server.PublicDnsName' (get the attribute PublicDnsName of the EC2 instance)
        Description: 'Public name of the EC2 instance'

Query the outputs 
$ aws cloudformation describe-stacks --stack-name sample \
--query "Stacks[0].Outputs[0].OutputValue"

## UserData
Putting user data in the Instance makes sure the code is executed upon start 

UserData:
    'Fn::Base64': !Sub |
        #!/bin/bash -x
        bash -ex << "TRY"
        while ! nc -z ${EFSFileSystem}.efs.${AWS::Region}.amazonaws.com 2049; do sleep 1; done
        mkdir /var/www
        mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2 "${EFSFileSystem}.efs.${AWS::Region}.amazonaws.com:/" /var/www/
        /opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource LaunchConfiguration --region ${AWS::Region}
        TRY
        /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource AutoScalingGroup --region ${AWS::Region}
    
Add the below to the end of UserData
Install all updates (which may make your system unpredictable)
yum -y update 

Install security updates 
yum -y --security update

A script to run this security update on all running virtual machines 
https://github.com/AWSinAction/code2/blob/master/chapter06/update.sh

``` 
#!/bin/bash -ex
PUBLICIPADDRESSESS="$(aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query "Reservations[].Instances[].PublicIpAddress" --output text)"

for PUBLICIPADDRESS in $PUBLICIPADDRESSESS; do
  ssh -t "ec2-user@$PUBLICIPADDRESS" "sudo yum -y --security update"
done 
``` 




