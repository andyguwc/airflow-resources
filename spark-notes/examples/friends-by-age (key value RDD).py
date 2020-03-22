
# key value RDD
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("FriendsByAge")
sc = SparkContext(conf = conf)

# output is key/value pairs of (age, numFriends)
def parseLine(line):
    fields = line.split(',') # parse the lines
    age = int(fields[2]) # cast to integer values
    numFriends = int(fields[3])
    return (age, numFriends)

lines = sc.textFile("file:/Users/tianyougu/spark/spark_course/fakefriends.csv")
rdd = lines.map(parseLine)

# key value RDD 
# (33,350) => (33, (350,1)) 
# count sum of freinds and number of entries by age
totalsByAge = rdd.mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
averagesByAge = totalsByAge.mapValues(lambda x: x[0] / x[1])
results = averagesByAge.collect()
for result in results:
    print(result)


