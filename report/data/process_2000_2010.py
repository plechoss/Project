import sys

import subprocess
import unicodedata
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

import cPickle as pickle

import urllib2
import json

import string
from os import environ
environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.databricks:spark-xml_2.10:0.4.0 pyspark-shell'

spark = SparkSession.builder.config("spark.jars", "spark-xml_2.10-0.4.0.jar").getOrCreate()
sc = spark.sparkContext

sqlContext = SQLContext(sc)

years = range(2000,2011)

titlesRatings = sqlContext.read.parquet('titlesAndRatingsAll5000from2000to2010.parquet')
temp = titlesRatings.select('tconst','startYear').rdd.map(lambda x: (x.tconst,x.startYear))
result = [('tt123123','helloWorld')]
print('text')
#Iterate over folders
for year in years:
    if count>10000:
        break
    command ='hadoop fs -ls /datasets/opensubtitle/OpenSubtitles2018/xml/en/' + str(year) + '/ |  awk \'{print $8}\''
    print("command: ")
    print(command)
    p = subprocess.Popen(command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    #for every folder in the folders
    lines = p.stdout.readlines()
    lines = lines[1:]
    print("lines: ")
    print(lines)
    if(len(lines)>0):
        for moviePath in lines:
            if count>10000:
                break
            folders = moviePath.split('/')
            movieId = 'tt' + folders[-1]
            
            if(rdd.filter(lambda a: ((a[0] == movieId) and (a[1] == str(year)))).count() > 0):
                xmlCommand = 'hadoop fs -ls ' + moviePath + ' |  awk \'{print $8}\''
                
                q = subprocess.Popen(xmlCommand,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
                print("folder path: ")
                print(moviePath)
                files = q.stdout.readlines()
                if len(files)>1:
                    #print("Files1: ")
                    #print(files[1])
                    firstSubPath = files[1].split(' ')
                    #open and work on the xml
                    #print("subPath: ")
                    filePath = firstSubPath[-1]
                    #print(filePath)
                    filePath = filePath[:-1]
                    #print(filePath)
                    try:
                        df = sqlContext.read.format('com.databricks.spark.xml').options(rootTag='document',rowTag='s').option("valueTag", "content").load(filePath)
                        data = df.select(explode('w.content').alias('word')).rdd.map(lambda x: x['word']).reduce(lambda x,y: x+ ' ' +y)
                        print("Adding as a result: ")
                        print((movieId[:-1],data))
                    except:
                        data = ''
                    result.append((movieId[:-1],data))


dfResult = sc.parallelize(result)
dfResult.toDF().write.parquet("processTest.parquet",mode='overwrite')

spark.stop()

