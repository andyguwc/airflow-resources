# CloudWatch


## CloudWatch Triggering Recovery 
- EC2 detects outage and reports to CloudWatch
- CloudWatch alarm triggers recovery of the virtual machine
- EC2 launched on another host 
- EBC volume and Elastic IP stay the same and linked to the new instance 


First create a cloudwatch alarm, which consists of 
- A metric that monitors data 
- A rule defining a threshold
- Actions to trigger if the state of the alarm changes 

CloudFormation template to launch a CloudWatch alarm which triggers recovery if EC2 failed

```
RecoveryAlarm:
    Type: 'AWS::CloudWatch::Alarm'
    Properties:
        AlarmDescription: 'Recover EC2 instance...'
        Namespace: 'AWS/EC2'
        MetricName: 'StatusCheckFailed_System'
        Statistic: Maximum
        Period: 60 
        EvaluationPeriods: 5 
        ComparisonOperator: GreaterThanThreshold
        Threshold: 0
        AlarmActions:
        - !Sub 'arn:aws:automate:${AWS::Region}:ec2:recover'
        Dimensions:
        - Name: InstanceId
          Value: !Ref VM 
```
