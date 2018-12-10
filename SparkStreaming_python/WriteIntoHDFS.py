# -*- coding:utf-8 -*-
import pymongo
import datetime
import time
import re

class MongodbConn(object):
    def __init__(self):
        self.CONN = pymongo.MongoClient("127.0.0.1", 27017)

    def fuzzyFinder(self,home):
        provDic = {".*北京.*":'北京市',".*天津.*":'天津市',".*上海.*":'上海市',".*重庆.*":'重庆市',".*河北.*":'河北省',".*山西.*":'山西省',".*辽宁.*":'辽宁省',".*吉林.*":'吉林省',".*黑龙江.*":'黑龙江省',".*江苏.*":'江苏省',".*浙江.*":'浙江省',".*安徽.*":'安徽省',".*福建.*":'福建省',".*江西.*":'江西省',".*山东.*":'山东省',".*河南.*":'河南省',".*湖北.*":'湖北省',".*湖南.*":'湖南省',".*广东.*":'广东省',".*海南.*":'海南省',".*四川.*":'四川省',".*贵州.*":'贵州省',".*云南.*":'云南省',".*陕西.*":'陕西省',".*甘肃.*":'甘肃省',".*青海.*":'青海省',".*台湾.*":'台湾省',".*内蒙古.*":'内蒙古自治区',".*广西.*":'广西壮族自治区',".*西藏.*":'西藏自治区',".*宁夏.*":'宁夏回族自治区',".*新疆.*":'新疆维吾尔自治区',".*香港.*":'香港特别行政区',".*澳门.*":'澳门特别行政区'}
        for i in provDic.keys():
            regex = re.compile(i)
            match = regex.search(home)
            if match:
                return provDic[i]
        return "null"
    def run(self):
        # database = "database_name"
        database = "PersonStatisticDB"
        db = self.CONN[database]
        # db.authenticate("username", "password")
        col = db["data"]

        start_year = 2010
        end_year = 2018

        currentYear = start_year
        while currentYear <= end_year:
            # query the document
            result = col.find({'reg_time':{'$gte':str(currentYear) + '-01-01','$lte':str(currentYear) + '-12-31'}})
            k = 0
            #写入数据，hdfs:///log/
            file = open("hdfs:///log/" + str(currentYear) + ".log","w",encoding = "utf-8")
            count = 0
            for i in result:
                title = i["title"]
                home = ""
                if title != "null":
                    r = title.rfind("]",0,len(title))
                    l = title.rfind("[",0,len(title)) + 1
                    home = title[l:r]
                else:
                    home = i["home"]
                native = self.fuzzyFinder(home)
                if native != "null":
                    file.write(native)
                    file.write(" ")
                    file.write(i["reg_time"])
                    file.write(" ")
                    file.write(i["sex"])
                    file.write("\n")
            file.close()
            time.sleep(15)
            currentYear += 1

if __name__ == '__main__':
    mongo_obj = MongodbConn()
    mongo_obj.run()