
# Elastic Beanstalk Basics

Deploy a common web application. The OS and runtime are managed by AWS 

AWS Elastic Beanstalk lets you handle the following recurring problems:
- Providing a runtime environment for a web application (PHP, Java, and so on)
- Updating the runtime environment for a web application
- Installing and updating a web application automatically
- Configuring a web application and its environment
- Scaling a web application to balance load
- Monitoring and debugging a web application


# Deploy
Creating an application
$ aws elasticbeanstalk create-application --application-name etherpad

Creating a version for Elastic Beanstalk
$ aws elasticbeanstalk create-application-version --application-name etherpad \
--version-label 1 \
--source-bundle "S3Bucket=awsinaction-code2,S3Key=chapter05/etherpad.zip"

Creating an environment to execute 
$ aws elasticbeanstalk create-environment --environment-name etherpad \
--application-name etherpad \
--option-settings Namespace=aws:elasticbeanstalk:environment,\
OptionName=EnvironmentType,Value=SingleInstance \
--solution-stack-name "$SolutionStackName" \
--version-label 1

Track environment status 
$ aws elasticbeanstalk describe-environments --environment-names etherpad

Clean up 
$ aws elasticbeanstalk terminate-environment --environment-name etherpad
wait until status changed to terminated do the delete
$ aws elasticbeanstalk delete-application --aplication-name etherpad 


# Monitor & LOgs
Click Logs from the submeanu 
Request logs 

