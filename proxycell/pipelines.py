# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
sys.path.append("D:\\workshop\\python\\proxycell")
from .RedisOperator import RedisOperator
from scrapy.exceptions import DropItem

class ProxycellPipeline(object):
    def process_item(self, item, spider):
        return item
class ProxycellInfoPipeline(object):
    '''主输出pipe 到redis
    '''
    def __init__(self):
        self.tmp=set()


    def process_item(self,item,spider):
        
        
        try:
            conn = RedisOperator()
            # print("try pipe")
            content = item['ip']
            print(content)
            # content = item['test']
            
            with open('test.txt', 'ab') as f:
                print("try w")
                f.write(bytes(content,encoding='utf-8'))
            if content:
                print("try c")
                
                # self.tmp.add(content)
                
                conn.puts([content])
                print(content)

        except Exception as e:
            print(e)
        return item
    # def close_spider(self, spider):
        # print(str(self.tmp))

class ProxycellTestPipeline(object):


    def process_item(self,item,spider):
        print("test")
        
from scrapy.exceptions import DropItem





class DuplicatesPipeline(object):
    '''检测重复ip /替换为使用set数据结构储存
    '''
    def __init__(self):
        self.ips_seen = set()
        self.conn = RedisOperator()

    def open_spider(self, spider):
        self.ips_seen=self.conn.get_all()

    def process_item(self, item, spider):
        if item['ip'] in self.ips_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ips_seen.add(item['ip'])
            return item