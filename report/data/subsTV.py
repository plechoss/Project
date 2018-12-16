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
    path = 'hdfs:///datasets/opensubtitle/OpenSubtitles2018/xml/en/' + year + '/' + str(int(id[2:])) + '/*'
    try:
        print("Hit path: " + path)
        df = sqlContext.read.format('com.databricks.spark.xml').options(rootTag='document',rowTag='s').option("valueTag", "content").load(path)
        print("DF read")
        data = df.select(explode('w.content').alias('word')).rdd.map(lambda x: x['word']).reduce(lambda x,y: x+ ' ' +y)
        print("DF selected")
        return (id,data)
    except:
        return (id,"")

for year in [2009]:
    print('year: ' + str(year))
    parquetPath = 'titlesAndRatingsAll5000.parquet'
    titlesRatings = sqlContext.read.parquet(parquetPath)
    
    temp = titlesRatings.filter(titlesRatings.startYear == str(year)).select('tconst','startYear').rdd.map(lambda x: (x.tconst,x.startYear)).collect()
    result = [getCleanData(i, year) for i, year in temp]

    output = spark.createDataFrame(result,schema=['tconst','subs'])
    print('output created')
    moviesSubsPath = "moviesSubs" + str(year) + ".parquet"
    output.write.mode('overwrite').parquet(moviesSubsPath)
    print('output written')
    titlesRatingsAndTopics = titlesRatings.join(output, 'tconst')
    print('join performed')
    titlesRatingsAndSubsAllPath = "titlesRatingsAndSubsAll" + str(year) + ".parquet"
    titlesRatingsAndTopics.write.mode('overwrite').parquet(titlesRatingsAndSubsAllPath)
    print('titlesRatingsAndTopics written to titlesRatingsAndSubsAll.parquet')

spark.stop()

