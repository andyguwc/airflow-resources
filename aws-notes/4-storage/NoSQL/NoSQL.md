# DynamoDB 

## NoSQL
Scaling a traditional relational database is difficult due to transactional ACID guarantees requiring communications among all nodes during a two-phase commit 
- the more nodes added the slower the database becomes because more nodes must coordinate transactions between each other 

Types of NoSQL Databases 
- document, graph, columnar, and key value 

Dynamo is key value store with document support and it's fully managed by AWS

Networking
- It doesn't run in the VPC. Only accessible via the AWS API which requires internet access 
- One approach is using NAT gateway
- Better approach is to set up a VPC endpoint for DynamoDB and use that to access DynamoDB from private subnets without needing a NAT gateway 



## DynamoDB Structure
DynamoDB is a key-value store that organizes your data into tables. For example, you
can have a table to store your users and another table to store tasks. The items contained
in the table are identified by a primary key. An item could be a user or a task;
think of an item as a row in a relational database. A table can also maintain secondary
indexes for data lookup in addition to the primary key, which is also similar to relational
databases.

Each DynamoDB table has a name and organizes a collection of items. An item is a collection
of attributes, and an attribute is a name-value pair. The attribute value can be
scalar (number, string, binary, Boolean), multivalued (number set, string set, binary
set), or a JSON document (object, array). Items in a table aren’t required to have the
same attributes; there is no enforced schema.

Primary Key
- unique within a table and identifies an item
- can use a single attribute as the primary key 
- termed partition key in Dynamo 
- if having two attributes the primary key, one is partition key another is sort key 
    - The partition key can only be queried using exact matches (=). 
    - The sort key can be queried using =, >, <, >=, <=, and BETWEEN x AND y operators


## Creating DynamoDB Tables
Required Properties:
- table-name
- attribute-definitions: name and type of attributes used as the primary key 
- key-schema: name of attributes that are part of the primary key
- provisioned-throughput: performance settings for this table

An example todo user table with user_id as primary key (partition key)
```
$ aws dynamodb create-table --table-name todo-user \
--attribute-definitions AttributeName=uid,AttributeType=S \ (items must have at least one attribute uid of type string)
--key-schema AttributeName=uid,KeyType=HASH \ (the parition key type HASH uses the uid attribute)
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

An example todo task table with user_id as partition key and task_id as sort key
$ aws dynamodb create-table --table-name todo-task \
--attribute-definitions AttributeName=uid,AttributeType=S \
AttributeName=tid,AttributeType=N \
--key-schema AttributeName=uid,KeyType=HASH \
AttributeName=tid,KeyType=RANGE \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

Global Secondary Index
A global secondary index is a projection of your original table that is automatically maintained by DynamoDB. Items in an index don’t have a primary key, just a key. This key is not necessarily unique within the index. Imagine a table of users where each user has a country attribute. You then create a global secondary index where the country is the new partition key. 

As you can see, many users can live in the same country, so that key is not unique in the index.You can query a global secondary index like you would query the table. You can imagine a global secondary index as a read-only DynamoDB table that is automatically maintained by DynamoDB: whenever you change the parent table, all indexes are asynchronously (eventually consistent) updated as well.

