
from pyspark import SparkConf, SparkContext
import collections

conf = SparkConf().setMaster("local").setAppName("RatingsHistogram")
sc = SparkContext(conf = conf)

# read in file 
lines = sc.textFile("file:/Users/tianyougu/spark/spark_course/ml-100k/u.data")

# get the rating data from text file
ratings = lines.map(lambda x: x.split()[2])
result = ratings.countByValue()

# sorting values 
sortedResults = collections.OrderedDict(sorted(result.items()))
for key, value in sortedResults.items():
    print("%s %i" % (key, value))

