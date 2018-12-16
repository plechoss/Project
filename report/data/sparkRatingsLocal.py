import sys

import subprocess
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.functions import *
from pyspark.sql.functions import min
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

import urllib2
import json

import string
from os import environ
environ['PYSPARK_SUBMIT_ARGS'] = '--packages com.databricks:spark-xml_2.10:0.4.0 pyspark-shell'

alphabet = list(string.ascii_lowercase)

stopWords = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

spark = SparkSession.builder.config("spark.jars", "spark-xml_2.10-0.4.0.jar").getOrCreate()
sc = spark.sparkContext

sqlContext = SQLContext(sc)

years = range(1940, 2019)
result = []

count = 0

def isAWord(x):
    if(x == None):
        return False
    if(len(x)==0 or x.lower() in stopWords or any(not c.isalpha() for c in x)):
        return None
    else:
        return x

#returns 5 words related to the word
def topic(word):
    call = 'https://api.datamuse.com/words?topics=%s'%word
    contents = urllib2.urlopen(call).read()
    data = json.loads(contents)
    result = []
    for row in data[:5]:
        result.append(row['word'])
    return result

def getCleanData(filePath):
    print("getThemes filepath is: ")
    print(filePath)
    df = sqlContext.read.format('com.databricks.spark.xml').options(rootTag='document',rowTag='s').option("valueTag", "content").load(filePath)
    data = df.select(col('time._value').alias('time'),explode('w.content').alias('word'))
    clean_data = data.withColumn('startingTime',data['time'].getItem(0)).select(col('word'))
    newData = clean_data.select(udf_is_a_word('word').alias('word'))
    cleanData = newData.na.drop(subset=["word"])
    cleanData.show()
    return cleanData

udf_is_a_word = udf(isAWord, StringType())

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
            folders = moviePath.split('/')
            movieId = 'tt' + folders[-1]
            
            xmlCommand = 'hadoop fs -ls ' + moviePath + ' |  awk \'{print $8}\''
            
            q = subprocess.Popen(xmlCommand,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
            print("folder path: ")
            print(moviePath)
            files = q.stdout.readlines()
            if len(files)>0:
                firstSubPath = files[1].split(' ')
                #open and work on the xml
                print("subPath: ")
                filePath = firstSubPath[-1]
                filePath = filePath[:-1]
                print(filePath)
                movieCleanData = getCleanData(filePath)
                sparkRdd = movieCleanData.rdd
                print(sparkRdd.take(1))
                topTopics = sparkRdd.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b).flatMap(lambda (a, b): [(w, b) for w in topic(a)]).reduceByKey(lambda a, b: a + b).sortBy(lambda a,b: b).take(20).map(lambda (a,b): a)
                #add result to the table
                result.append((movieId, topTopics))
                count = count + 1

dfResult = sc.parallelize(result)
dfResult.write.parquet("titlesAndRatings.parquet")
spark.stop()

