
# Filtering RDD
# Creating a smaller RDD file 

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("MinTemperatures")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split(',')
    stationID = fields[0]
    entryType = fields[2]
    temperature = float(fields[3]) * 0.1 * (9.0 / 5.0) + 32.0
    # return composite value
    return (stationID, entryType, temperature)

lines = sc.textFile("file:/Users/tianyougu/spark/spark_course/1800.csv")
parsedLines = lines.map(parseLine)
# filter only for those with TMIN entryType
minTemps = parsedLines.filter(lambda x: "TMIN" in x[1])

# key value pair with stationID, temperature 
stationTemps = minTemps.map(lambda x: (x[0], x[2]))
# extract the minimum 
minTemps = stationTemps.reduceByKey(lambda x, y: min(x,y))
results = minTemps.collect()

for result in results:
    print(result[0] + "\t{:.2f}F".format(result[1]))
