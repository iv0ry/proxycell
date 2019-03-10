import scrapy
import sys
sys.path.append("D:\\workshop\\python\\proxycell")
from proxycell.items import ProxycellInfoItem

class XiciSpider(scrapy.Spider):
    name = 'xici'

    start_urls = ['http://www.xicidaili.com/nn/1']
    # start_urls = []
    # #爬取5页网站的IP
    # for i in range(1,1):
    #     start_urls.append('http://www.xicidaili.com/nn/'+str(i))

    def parse(self, response):

        item = ProxycellInfoItem()
        
        for sel in response.xpath('//tr'):
            ip= sel.xpath('.//td[2]/text()').extract_first()
            port=sel.xpath('.//td[3]/text()').extract_first()
            item['ip']=str(ip)+":"+str(port)

            yield item
