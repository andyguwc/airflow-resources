# Popular Movie

# Dataset User ID, Movie ID, Rating, Timestamp

from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("PopularMovies")
sc = SparkContext(conf = conf)

# sort example - first creating key value map with value 1, then reduce by key then flip count and movie
lines = sc.textFile("file:/Users/tianyougu/spark/spark_course/ml-100k/u.data")
movies = lines.map(lambda x: (int(x.split()[1]), 1))
movieCounts = movies.reduceByKey(lambda x, y: x + y)

sortedMovies = movieCounts.map( lambda (x,y): (y,x)).sortByKey()

results = sortedMovies.collect()

for result in results:
    print(result)
