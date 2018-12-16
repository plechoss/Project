import subprocess
import pyspark

p = subprocess.Popen("hadoop fs -ls /datasets/opensubtitle/OpenSubtitles2018/xml/en/1978/ |  awk '{print $8}",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)

f = open("output.txt", "w")

for line in p.stdout.readlines():
    f.write(line)
    f.write('\n')
