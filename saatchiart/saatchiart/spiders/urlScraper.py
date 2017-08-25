import scrapy
from functools import reduce
from operator import mul
from saatchiart.items import SaatchiartItem   
from scrapy.http import Request


class urlScraper(scrapy.Spider):
    name = 'urlSpider'
 
    def start_requests(self):
        urls = ["https://www.saatchiart.com/paintings/fine-art?page="+str(i) for i in range(1,1500)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to paintings pages
        for href in response.css('div.list-art-image-wrapper a::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_painting)
    
    def parse_painting(self, response):
        item=SaatchiartItem()
        def size_calculcation():
            h=response.xpath('/*/*/meta[@property="bt:dimensions"]/@content').extract_first().split('x')[0].replace('H',"")
            w=response.xpath('/*/*/meta[@property="bt:dimensions"]/@content').extract_first().split('x')[1].replace('W',"")    
            return float(h)*float(w)   
        
        item["title"]=  response.xpath('/*/*/meta[@property="og:title"]/@content').extract_first().split(':')[1].replace('"',"").replace(",","").replace("'","")
        item["creator"]=response.xpath('/*/*/meta[@property="bt:artist"]/@content').extract_first().replace('"',"").replace(",","").replace("'","")
        item["artistCountry"]= response.xpath('/*/*/meta[@property="bt:artistCountry"]/@content').extract_first().replace('"',"").replace(",","").replace("'","")
        item["price"]= float(response.xpath('/*/*/meta[@property="og:price:amount"]/@content').extract_first())
        item["size"]= size_calculcation()
        item["favoriteCount"]= int(response.css("ul.inline-list div::text").extract_first().strip())
        item["views"]= int(response.css("div.art-detail-stats ul li::text").extract_first().strip())
        item["painting"]=  response.xpath('/*/*/*/*/*/section[@itemprop="description"]/*/*/*/span/text()').extract()[0].strip().split(',')[0]
        item["medium"]= response.xpath('/*/*/meta[@property="bt:mediums"]/@content').extract_first().replace('"',"").replace(",","").replace("'","")
        item["materials"]= response.xpath('/*/*/meta[@property="bt:materials"]/@content').extract_first().replace('"',"").replace(",","").replace("'","")
        item["subject"]= response.xpath('/*/*/meta[@property="bt:subject"]/@content').extract_first().replace('"',"").replace(",","").replace("'","")
        item["pubDate"]= int(response.xpath('/*/*/meta[@property="bt:pubDate"]/@content').extract_first())
        
        urlss = response.xpath('//div[@class="row-layout content"]/article[@class="art-detail"]/div[@class="row"]/div[@class="row art-detail-body"]/div[@class="small-12 large-4 columns art-detail-description"]/div[@class="row"]/div[@class="small-12 medium-6 large-12 columns art-meta"]/p[1]/a/@href').extract()

        link = 'https://www.saatchiart.com' + urlss[0]
        request = Request(link, callback=self.parse_artist)
        request.meta['item'] = item
        yield request
        

    def parse_artist(self, response):
        item = response.meta['item']
        item["artist_followers"] = response.xpath('//div[@class="row row-layout profile-content"]/article/div[@class="profile-about small-12 medium-6 large-4 columns"]/div[@class="about-follow-nav"]/a[2]/span/text()').extract_first()
        item["artist_NoOfArts"] = response.xpath('//div[@class="row row-layout profile-content"]/article[@class="profile"]/aside[@class="aside-portfolio small-12 medium-6 large-8 columns"]/h5/a/span/text()').extract_first().replace('"',"").replace(")","").replace("(","")
        yield item
        

