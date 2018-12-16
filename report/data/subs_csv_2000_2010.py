import sys

from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
import csv
import string
from os import environ
environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.databricks:spark-xml_2.10:0.4.0 pyspark-shell'

spark = SparkSession.builder.config("spark.jars", "spark-xml_2.10-0.4.0.jar").getOrCreate()
sc = spark.sparkContext
sqlContext = SQLContext(sc)

def getCleanData(id, year):
    path = 'hdfs:///datasets/opensubtitle/OpenSubtitles2018/xml/en/' + year + '/' + id[2:] + '/*'
    try:
        df = sqlContext.read.format('com.databricks.spark.xml').options(rootTag='document',rowTag='s').option("valueTag", "content").load(path)
        data = df.select(explode('w.content').alias('word')).rdd.map(lambda x: x['word']).reduce(lambda x,y: x+ ' ' +y)
        return (id,data)
    except:
        return (id,"")


titlesRatings = sqlContext.read.parquet('titlesAndRatingsAll5000.parquet')

temp = titlesRatings.select('tconst','startYear').rdd.map(lambda x: (x.tconst,x.startYear)).collect()
result = [getCleanData(i, year) for i, year in temp]

item_length = len(result)
with open('result.csv', 'wb') as test_file:
    file_writer = csv.writer(test_file)
    for i in range(item_length):
        file_writer.writerow([x[i] for x in result])

output = spark.createDataFrame(result,schema=['tconst','subs'])
output.write.mode('overwrite').parquet("moviesSubs.parquet")
titlesRatingsAndTopics = titlesRatings.join(output, output.tconst == titlesRatings.tconst)
titlesRatingsAndTopics.write.mode('overwrite').parquet("titlesRatingsAndSubsAll.parquet")

spark.stop()

