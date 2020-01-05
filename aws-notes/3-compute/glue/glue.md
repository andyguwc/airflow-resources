# Glue

AWS re:Invent 2018: Building Serverless Analytics Pipelines with AWS Glue (ANT308)
AWS re:Invent 2018: Build and Govern Your Data Lakes with AWS Glue (ANT309)


## Glue Basics
- Data catalog and integration/prep platform
- Crawlers, Tables and Jobs
    - Crawlers add tables to Glue catalog
    - Then data integration jobs can run against these tables
- Runs on Spark in serverless environment 


## Glue Catalogs
- Glue crawlers
    - takes inventory of the data 
    - if no customized classifier matches the schem, built-in schemas tries to match your data schema
    - inferred schema is created and the metadata is written to data catalog
- Catalog data is the index to the location and schema of your data 
- Centralized metadata catalog
- Transformation
    - relationalizes semi-structured data 


## Glue ETL Scripts
- Read dynamic frame from source 
- Data transformation + data cleaning 
- Write out dynamic frames

Dynamic Frames
- designed for processing semi-structured data 
- no need to have schema up-front 

## Configure Glue

- Upload Python ETL Script for transformation
    - create dynamic frameworks for the tables we want to join
    - apply joins
    - construct bucket URL and write the dynamic frame to desired s3 bucket in PARQUET format
- CloudFormation stack for Glue
    - which creates the various Glue assets
- Run Glue crawler on the RDS database
- Review that the glue table is populated
- Run the Glue job ETL script to perform transformations




# Other Services

## Data Pipeline
- Code free
- Drag and drop interface

## Lake Formation
- Accelerated version of Glue
- Automate lots of tasks to create a data lake