# CloudWatch

## CloudWatch Basics 

Logs
- segrecated into trace, debug, info, etc.

Metrics
- quantitative measurements of the system (e.g. errors, calls, etc.)
- log levels: output error level logs to centralized log store, and warn/info to local hard disk
- best practices
  - isolate and contain metrics submitted by one applicational product 
  - multiple dimensions (e.g. status code)


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


## Configure CloudWatch

Resources
- Log Group
  - Configure Log Data Retention Period 
- Log Stream 

Customized Metrics 
- put metrics data to S3 
- using the async cloudwatch client (don't hold out production in case cloudwatch doesn't respond)

Dashboards & Alarms 
- SMS allows cloudwatch to send alarms 

