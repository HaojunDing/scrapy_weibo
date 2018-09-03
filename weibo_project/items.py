# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class weiboProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    print('到items了')
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    weibo_auth = scrapy.Field()
    jianjie = scrapy.Field()
    text = scrapy.Field()
    zhuanfa = scrapy.Field()
    dianzan = scrapy.Field()
    pinglun = scrapy.Field()
    date = scrapy.Field()
    source = scrapy.Field()
    text_url = scrapy.Field()
    weibo_url = scrapy.Field()
    def store(self):
    # pass
        print('进到sql函数了')
        sql = 'insert into weibo (user_name, user_id, weibo_auth, jianjie, context, zhuanfa, dianzan, pinglun, dates, source, text_url, weibo_url) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        print(sql)
        data = (self['user_name'], self['user_id'], self['weibo_auth'], self['jianjie'], self['text'], self['zhuanfa'], self['dianzan'], self['pinglun'], self['date'], self['source'], self['text_url'], self['weibo_url'])
        return (sql, data)