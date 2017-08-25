# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SaatchiartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title= scrapy.Field()
    creator= scrapy.Field()
    artistCountry= scrapy.Field()
    price= scrapy.Field()
    size= scrapy.Field()
    favoriteCount= scrapy.Field()
    views= scrapy.Field()
    painting= scrapy.Field()
    medium= scrapy.Field()
    materials= scrapy.Field()
    subject= scrapy.Field()
    pubDate= scrapy.Field()
    artist_followers= scrapy.Field()
    artist_NoOfArts= scrapy.Field()
    
    pass
