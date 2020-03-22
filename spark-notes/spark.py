
##################################################
# Spark Basics
##################################################

'''
spark components
'''
# large-scale data processing 
# - driver program (spark context)
# - cluster manager (Spark, YARN) will split the tasks to Executors (nodes)
# - faster and more efficient than Hadoop

# additional libraries
# - spark streaming
# - spark SQL 
# - MLLib
# - GraphX

'''
run spark
'''
# $ brew install apache-spark 
# $ spark-submit examples/ratings-counter.py 

# spark context
# - created by the driver program
# - responsible for making RDD resilient and distributied 

# the spark shell creates a "sc" object for you 

# sets the process as local box 
# doesn't run distributed nodes yet 
conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)



##################################################
# RDD
##################################################
'''
RDD basics
'''
# Resilient Distributed Dataset 

# Create RDD
# - from SC
#   - sc.textFile("file:/")
#   - sc.textFile("s3:")
# - from JDBC
# - from HBase
# - JSON, CSV, etc.

'''
Transform RDD
'''

# - map 
rdd.map(lambda x: x*x)

# - flatmap (create multiple values for each input value)
# - filter
# - distinct
# - sample
# - union, intersection

# RDD Actions
# collect 
# count 
# countByValue 
# take
# top 
# reduce 

'''
key value RDD
'''

# combine values with the same key using some function
rdd.reduceByKey(lambda x,y: x+y) # adds values up 

# group values with the same key 
groupByKey() 

# sort RDD by key values
sortByKey()

# mapping just the values (more efficient)
# keys not modified
mapValues()
flatMapValues()

# filtering 
# filter() removes data from the RDD
minTemps = parsedLines.filter(lambda x: "TMIN" in x[1])

'''
map vs. flatmap
'''
# map() transforms each element of an RDD into one new element 
lines.map(lambda x: x.upper())

# flatmap() can create many new elements from each one 
lines.flatMap(lambda x: x.split())

'''
sorting
'''
wordCounts = words.map(lambda x: (x,1)).reduceByKey(lambda x: x+y)
# flip around key and value to sort 
wordCountsSorted = wordCounts.map(lambda (x,y): (y,x)).sortByKey()
results = wordCountsSorted.collect()

'''
partition
'''
# use .partitionBy() on an RDD before running a large operation 
# operations which will preserve the partitioning in the results
# join(), cogroup(), groupWith(), leftOuterJoin(), groupByKey(), reduceByKey(), combineByKey(), lookup()


'''
resources
'''
# https://towardsdatascience.com/a-neanderthals-guide-to-apache-spark-in-python-9ef1f156d427


##################################################
# Running Spark on AWS (EMR)
##################################################

# Get the scripts and the data on S3 where EMR can access easily 
# Spin up EMR cluster 
# SSH into the master node
# Copy the driver program and any files it needs
# Run spark-submit

# logging
# distirbuted
# collec them using
# yarn logs --aplicationID <app ID>


##################################################
# Spark SQL
##################################################

# DataFrame is like RDD for row objects
# Can read/write JSON files and JDBC connections 

'''
dataframe operations
'''
df.show()
df.select('samplefield')
df.filter(df('samplefield'>100))
df.groupBy(df('samplefield')).mean()
df.rdd().map(mapperFunction)


'''
spark sql example
'''
# Spark SQL
from pyspark.sql import SparkSession
from pyspark.sql import Row

import collections

# Create a SparkSession 
spark = SparkSession.builder.appName("SparkSQL").getOrCreate()

def mapper(line):
    fields = line.split(',')
    # gives us row objects 
    return Row(ID=int(fields[0]), name=str(fields[1].encode("utf-8")), age=int(fields[2]), numFriends=int(fields[3]))

lines = spark.sparkContext.textFile("fakefriends.csv")
people = lines.map(mapper)

# Infer the schema, and register the DataFrame as a table.
schemaPeople = spark.createDataFrame(people).cache()
# create a temparary sql table in memory
schemaPeople.createOrReplaceTempView("people")

# SQL can be run over DataFrames that have been registered as a table.
teenagers = spark.sql("SELECT * FROM people WHERE age >= 13 AND age <= 19")

# The results of SQL queries are RDDs and support all the normal RDD operations.
for teen in teenagers.collect():
  print(teen)

# We can also use functions instead of SQL queries:
schemaPeople.groupBy("age").count().orderBy("age").show()

spark.stop()


'''
register user defined functions
'''