import scrapy
import sys
sys.path.append("D:\\workshop\\python\\proxycell")
from proxycell.items import TestInfoItem

class TestSpider(scrapy.Spider):
    name = 'test'

    start_urls = ['http://www.goddessfantasy.net/bbs/index.php?topic=56571']
    #爬取5页网站的IP
    # for i in range(1,6):
    #     start_urls.append('http://www.xicidaili.com/wt/'+str(i))

    def parse(self, response):

        item = TestInfoItem()
        p=0
        for sel in response.xpath('//tr/td[1]/a'):
            if p>=100:
                break
            else:
                p=p+1
            print('*',end='')
            mname = sel.xpath('text()').extract_first()
            mherf = sel.xpath('@herf').extract()
            item['test']=str(mname)+":"+str(mherf)
            # tmp = mname+'\n'
            # with open('test.txt', 'ab') as f:
            #     f.write(bytes(tmp,encoding='utf-8'))
            yield item

            
        
            
        
