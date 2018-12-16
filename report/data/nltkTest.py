import sys
egg_path='nltk-3.0.0-py2.6.egg'
sys.path.append(egg_path)

import subprocess

import string
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stopWords = set(stopwords.words('english'))
alphabet = list(string.ascii_lowercase)

years = range(1940, 2019)
result = []

text = 'GENERAL STANDARDIZATION THEORY Try building a tower by piling irregular stones on top of each other. It can be done, eight, nine, sometimes ten stones high. You need a stable hand and a good eye to spot each rock’s surface features. You find such man-made “Zen stone towers” on riverbanks and mountaintops. They last for a while until the wind blows them over. What is the relationship here between skill and height? Take relatively round stones from a riverbank. A child of two can build a tower two stones high. A child of three with improved hand-eye-coordination can manage three stones. You need experience to get to eight stones. And you need tremendous skill and a lot of trial and error to go higher than ten. Dexterity, patience and experience can get you only so far. Now, try with a set of interlocking toy bricks as your stones. You can build much higher. More importantly: your three-year-old can build as high as you can. Why? Standardization. The stability comes from the standardized geometry of the parts. The advantage of skill is vastly diminished. The geometry of the interlocking bricks corrects the errors in hand-movement. But structural stability is standardization’s least impressive feat. Its advantages for collaboration are much more significant. We have long appreciated the advantages of standardization in business. In 1840, the USA had more than 300 railroad companies, many with different gauges (the width between the inner sides of the rails). Many companies refused to agree on a standard gauge because of heavy sunk costs and the need for barriers to competition. Where two rail lines connected, men had to offload the cargo, sometimes store it and then load it onto new cars. In a series of steps, some by top-down enactment, but mostly by bottom-up coordination, the industry finally standardized gauges by 1886. Other countries saw similar \“gauge wars.\” England ended them by legislation in 1856. In the last hundred years, every national government and supranational organization, and virtually every industry has created bodies to deal with standardization. They range from the International Organization for Standardization (ISO) to the World Wide Web Consortium (W3C) to bodies like the \“Bluetooth Special Interest Group.\” Their goals are always a combination of improved product quality, reputation, safety and interoperability.'

f = open("output3.txt", "w")
text2 = text.split(',. \"()')
text3 = list(filter(lambda s: isAWord(s), text2))

def isAWord(x):
    if(len(x)==0 or x.lower() in stopWords or not any(c.isalpha() for c in x)):
        return true
    else:
        return false
f.write(text3)
f.close()

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
    topTopics = sparkRdd.map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b).flatMap(lambda a, b: [(w, b) for w in topic(a)]).reduceByKey(lambda a, b: a + b).sortBy(lambda a,b: b).take(20).map(lambda a: a[0])
    return topTopics

