# Elastic Cache 

## Caching Basics
Leverage in-memory store like Redis for Caching 
Things requiring heavy reads can be cached freeing the database from heavy read traffic 
Downside is data durability 

Cache Strategy 
- Lazy loading 
    - Application writes to data store
    - If the application needs to read the data, it makes a request to the caching layer 
    - The caching layer does not contain the data. The application reads from the data store directly and puts the value into the cache and return the value to the client 
    - If it wants to read again, it makes a request to the caching layer 
    - Set TTL
        - Make sure data is refreshed 
- Writethrough
    - Application writes data to the data store and the cache (or the cache asyncronoushly via cron, aws lambda, etc.)
    - If the application wants to read the data at a later time, it makes a request to the caching layer which contains the data 
    - The value is returned to the client 

Storing Data in Redis
- Typically key value store 
- In cases of extracting processed data - store the result of the SQL query as a String value and the SQL statement as the key name 
- Key can be a URL, and UserID

## Launch via CloudFormation

Required Properties
- Engine (redis or memcached)
- CacheNodeType (similar to EC2 instance type)
- NumCacheNodes
- CacheSubnetGroup
- VPCSecurityGroups

```
Resources:
  CacheSecurityGroup:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: cache
      VpcId: !Ref VPC
      SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 6379
        ToPort: 6379
        CidrIp: '0.0.0.0/0'
  CacheSubnetGroup:
    Type: 'AWS::ElastiCache::SubnetGroup'
    Properties:
      Description: cache
      SubnetIds:
      - Ref: SubnetA
      - Ref: SubnetB
  Cache:
    Type: 'AWS::ElastiCache::CacheCluster'
    Properties:
      CacheNodeType: 'cache.t2.micro'
      CacheSubnetGroupName: !Ref CacheSubnetGroup
      Engine: redis
      NumCacheNodes: 1
      VpcSecurityGroupIds:
      - !Ref CacheSecurityGroup
```

To test redis, create a virtual machine with ability to SSH into it 


```
  VMSecurityGroup:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: 'vm'
      SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 22
        ToPort: 22
        CidrIp: '0.0.0.0/0'
      VpcId: !Ref VPC
  VMInstance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: !FindInMap [RegionMap, !Ref 'AWS::Region', AMI]
      InstanceType: 't2.micro'
      KeyName: !Ref KeyName
      NetworkInterfaces:
      - AssociatePublicIpAddress: true
        DeleteOnTermination: true
        DeviceIndex: 0
        GroupSet:
        - !Ref VMSecurityGroup
        SubnetId: !Ref SubnetA
Outputs:
  VMInstanceIPAddress:
    Value: !GetAtt 'VMInstance.PublicIp'
    Description: 'EC2 Instance public IP address (connect via SSH as user ec2-user)'
  CacheAddress:
    Value: !GetAtt 'Cache.RedisEndpoint.Address'
    Description: 'Redis DNS name (resolves to a private IP address)'
```

Once connected to the Redis machine, do below 

SSH into the VM
$ ssh -i mykey.pem ec2-user@$VMInstanceIPAddress
Install Redis
$ sudo yum -y install --enablerepo=epel redis
Get the output $CacheAddress from the stack outputs and play with it
$ redis-cli -h $CacheAddress

Then can SET key value and GET key value 

## Cache Deployment Options

Which deployment option you should choose is influenced by four factors:
1 Engine—Memcached or Redis
2 Backup/Restore—Is it possible to back up or restore the data from the cache?
3 Replication—If a single node fails, is the data still available?
4 Sharding—If the data does not fit on a single node, can you add nodes to increase capacity?

Memcached
- Sharding is implemented by the Memcached client, typically utilizing a consistent hashing algorithm
which arranges keys into partitions in a ring distributed across the nodes
- Each node stores a quniue portion of the key-space in-memory. If a node fails, the data is lost. Cannot back up teh data in Memcached
- Use Memcached if you can tolerate data loss and requires a simple in-memory store 

Redis: Single-Node
- Sharding and high availability are not possible with a single node 
- Redis supports creation of backups and allows you to restore those backups 
- Avoid single-node in production systems

Redis: Cluster Mode Disabled
- Supports backups and data replication but no sharding. 
- Just one shard with a primary node and some replica nodes
- Data has to fit into one node

Redis: Cluster 
- Supports backups, data replication, and sharding 


## Access Control 

Should have two security groups one for cluster the other for client
- The client Security Group attached to all EC2 instances communicating with this Redis cluster
- A cluster Security Group allows inbound traffic on port 6379 only for tarffic that comes from the client security group

Resources:
    ClientSecurityGroup:
        Type: 'AWS::EC2::SecurityGroup'
        Properties:
            GroupDescription: 'cache-client'
            VpcId: !Ref VPC
    CacheSecurityGroup:
        Type: 'AWS::EC2::SecurityGroup'
        Properties:
            GroupDescription: cache
            VpcId: !Ref VPC
            SecurityGroupIngress:
            - IpProtocol: tcp
                FromPort: 6379
                ToPort: 6379
                SourceSecurityGroupId: !Ref ClientSecurityGroup


## Monitor a Cache
- CPUUtilization—The percentage of CPU utilization.
- SwapUsage—The amount of swap used on the host, in bytes. Swap is space on disk that is used if the system runs out of physical memory.
- Evictions—The number of non-expired items the cache evicted due to the memory limit.
- ReplicationLag—This metric is only applicable for a Redis node running as a read replica. It represents how far behind, in seconds, the replica is in applying changes from the primary node. Usually this number is very low.

Improve Cache Performance
- Data compression
- Select larger nodes 
- Select the right deployment option (e.g. cluster mode which supports sharding)


