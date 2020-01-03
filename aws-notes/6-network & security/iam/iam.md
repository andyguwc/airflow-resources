
# IAM 


## IAM Basics
- An IAM user is used to authenticate people accessing your AWS account.
- An IAM group is a collection of IAM users.
- An IAM role is used to authenticate AWS resources, for example an EC2
instance.
- An IAM policy is used to define the permissions for a user, group, or role.


## Security 
Secure your applications
Restrict access to AWS account 
Control network traffic to and from EC2 instances
Install software updates


## Policy 

Policies are defined in JSON
- Effect
- Action
- Resources

Example - Allow any EC2 action on any resources 

{
    "Version": "2019-01-01",
    "Statement": [ {
        "Sid": "1",
        "Effect": "Allow",
        "Action": "ec2:*",
        "Resources": "*"
    }]
}

If with multiple statements that apply to the same action, Deny overrides Allow 


## Users and Groups
First create a group for all users with admin access. To help centralize authorization. 

Create groups and users using the CLI 

$ aws iam create-group --group-name "admin"
$ aws iam attach-group-policy --group-name "admin" \
-- policy-arn "arn:aws:iam::aws:policy/AdministratorAccess"
$ aws iam create-user --user-name "myuser"
$ aws iam add-user-to-group --group-name "admin" --user-name "myuser "
$ aws iam create-login-profile --user-name "myuser" --password "$Password"


## Roles
EC2 instances need to access or manage AWS Resources - like S3, or itself 
When using an IAM role, the access keys are injected into the EC2 instance automatically 

Example - launch an EC2 which will automatically shut down 
For cloudformation, need to create an IAM Role with Action to assume role and stop instances
Then create an InstanceProfile to be passed into the EC2 resource definition 
https://github.com/AWSinAction/code2/blob/master/chapter06/ec2-iamrole.yaml

```

  Role:
    Type: 'AWS::IAM::Role'
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
        - Effect: Allow
          Principal:
            Service:
            - 'ec2.amazonaws.com'
          Action:
          - 'sts:AssumeRole'
      Policies:
      - PolicyName: ec2
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
          - Sid: Stmt1425388787000
            Effect: Allow
            Action:
            - 'ec2:StopInstances'
            Resource:
            - '*'
            Condition:
              StringEquals:
                'ec2:ResourceTag/aws:cloudformation:stack-id': !Ref 'AWS::StackId'
  
  InstanceProfile:
    Type: 'AWS::IAM::InstanceProfile'
    Properties:
      Roles:
      - !Ref Role

  Instance:
    Type: 'AWS::EC2::Instance'
    Properties:
      IamInstanceProfile: !Ref InstanceProfile
      ImageId: !FindInMap [RegionMap, !Ref 'AWS::Region', AMI]
      InstanceType: 't2.micro'
      KeyName: !Ref KeyName
      SecurityGroupIds:
      - !Ref SecurityGroup
      SubnetId: !Ref Subnet
      UserData:
        'Fn::Base64': !Sub |
          #!/bin/bash -x
          INSTANCEID="$(curl -s http://169.254.169.254/latest/meta-data/instance-id)"
          echo "aws ec2 stop-instances --instance-ids $INSTANCEID --region ${AWS::Region}" | at now + ${Lifetime} minutes
      Tags:
      - Key: Name
        Value: 'AWS in Action: chapter 6 (IAM role)'
```
