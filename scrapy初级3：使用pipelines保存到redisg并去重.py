import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import logging
from ..items import HupuItem


============================================================================

#hupu.py，爬虫spider文件
class MySpider(CrawlSpider):
    name = 'Hupu'
    start_urls = ['https://bbs.hupu.com/topic']

    rules = (
        Rule(LinkExtractor(
            allow=('https://bbs.hupu.com/\d+\.html',)),
             callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        it=HupuItem()
        x=response.xpath(r'//div[@class="j_u"]/@uname').extract_first('没有找到')
        logging.error(response.url+'@'*8+x)
        it['t']=x
        yield it

    
============================================================================

#pipelines.py，用来处理spider yield的items
#打开对应的redis集合，
#如果username的长度大于7且没被保存在redis且这次没被爬取过（其实redis和self.s的检测重复了），则保存
'''
为了启用一个Item Pipeline组件，你必须将它的类添加到 ITEM_PIPELINES 配置，就像下面这个例子:
ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,
    'myproject.pipelines.JsonWriterPipeline': 800,
}
分配给每个类的整型值，确定了他们运行的顺序，item按数字从低到高的顺序，
，数字越小越优先，通过pipeline，通常将这些数字定义在0-1000范围内。
'''


import scrapy,logging,time,datetime
from redis import Redis

class HupuPipeline(object):
    def __init__(self):
        self.s=set()
        self.r=Redis(password='asd123')
        self.r1=self.r.smembers('hupuname')

    def process_item(self, items, spider):
        x=items['t']
        if len(x)>7 and x.encode() not in self.r1 and x not in self.s:
            self.s.add(x)
            self.r.sadd('hupuname',x)
            #logging.error('self.r.scard(hupuname)={}'.format(self.r.scard('hupuname')))
            
            with open('2.txt','a',encoding='utf8') as f:
                f.write(x+'\n')
                
            return items
    
