from __future__ import print_function
import sys
import pymongo as pm
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

def saveRecordToMongoDB(iter):
    #链接mongodb
    client = pm.MongoClient("localhost",27017)
    db = client["PersonStatisticDB"]
    col = db["ProvinceStatistic"]
    for record in iter:
        cnt = 0
        docs = col.find({"province":record[0]})
        for doc in docs:
            cnt += doc["cnt"]
            col.update({"province":record[0]},{'$set':{"cnt":cnt + record[1]}},upsert = True)
    client.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:SparkStreamExe.py <hostname> <port>",file = sys.stderr)
        exit(-1)
    sc = SparkContext("local[2]",appName = 'SparkStreamExe')
    #定义监听周期
    ssc = StreamingContext(sc,1)
    #监听目录 hdfs:///namenode:****/log/
    lines = ssc.textFileStream(sys.argv[len(sys.argv) - 1])
    #控制台打印数据
    lines.count().pprint()
    lines.pprint()
    #windows下需要重新进行字符编码
    #statistic = lines.map(lambda line : \ 
    # ((line.encode('utf-8').decode('ansi')).split(" ")[0],1))\ 
    # .reduceByKey(lambda a,b : a + b)
    statistic = lines.map(lambda line : \ 
        (line.split(" ")[0],1))\ 
        .reduceByKey(lambda a,b : a + b)
    #写入mongodb
    statistic.foreachRDD(lambda rdd : rdd.foreachPartition(saveRecordToMongoDB))
    #控制台输出
    statistic.pprint()
    #等待执行
    ssc.start()
    ssc.awaitTermination()