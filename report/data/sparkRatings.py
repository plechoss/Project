import subprocess
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stopWords = set(stopwords.words('english'))
alphabet = list(string.ascii_lowercase)

sc = pyspark.SparkContext()
sqlContext = SQLContext(sc)

years = range(1940, 2019)
result = []

count = 0


udf_is_a_word = udf(isAWord, StringType())

#Iterate over folders
for year in years:
    command ='hadoop fs -ls /datasets/opensubtitle/OpenSubtitles2018/xml/en/' + str(year) + '/ |  awk \'{print $8}\''
    p = subprocess.Popen(command,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    #for every folder in the folders
    for moviePath in p.stdout.readlines():
        folders = line.split('/')
        movieId = 'tt' + folders[-1]
        
        xmlCommand = 'hadoop fs -ls ' + moviePath + ' |  awk \'{print $8}\''
        
        q = subprocess.Popen(xmlCommand,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

        files = q.stdout.readlines()
        if len(files)>0:
            firstSubPath = files[0]
            #open and work on the xml
            movieThemes = getThemes(firstSubPath)
            #add result to the table
            result.append((movieId, movieThemes))

dfResult = sc.parallelize(result)
dfResult.write.parquet("titlesAndRatings.parquet")

def isAWord(x):
    if(len(x)==0 or x.lower() in stopWords or not any(c.isalpha() for c in x)):
        return None
    else:
        return x

#returns 5 words related to the word
def topic(word):
    call = 'https://api.datamuse.com/words?topics=%s'%word
    response = requests.get(call)
    data = response.json()
    result = []
    for row in data[:5]:
        result.append(row['word'])
    return result

def getThemes(filePath):
    df = sqlContext.read.format('com.databricks.spark.xml').options(rootTag='document',rowTag='s').option("valueTag", "content").load(moviePath)
    data = df.select(col('time._value').alias('time'),explode('w.content').alias('word'))
    clean_data = data.withColumn('startingTime',data['time'].getItem(0)).select(col('startingTime'), col('word'))
    newData = clean_data.select(udf_is_a_word('word').alias('word'))
    cleanData = newData.na.drop(subset=["word"])
    sparkDf = sc.createDataFrame(cleanData)
    sparkRdd = sc.parallelize(sparkDf)
    topTopics = sparkRdd.map(lambda x: (x, 1))
                        .reduceByKey(lambda a, b: a + b).flatMap(lambda a, b: [(w, b) for w in topic(a)])
                        .reduceByKey(lambda a, b: a + b).sortBy(lambda a,b: b).take(20)
                        .map(lambda a: a[0])
    return topTopics
