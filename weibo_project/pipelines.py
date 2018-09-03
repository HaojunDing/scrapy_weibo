# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .Mysql_wb import MysqlIns

class WeiboProjectPipeline(object):
    def process_item(self, item, spider):
        return item


class StorerMysqlScrapyPipeline(object):
    def process_item(self, item, spider):
        print('到下载函数了')
        '''
        :param item:  传来的 item 值
        :param spider:
        :return: 返回给其他函数调用
        '''
        # 存储数据到MySQL里面
        # print('----'*30)
        (inser_sql, data) = item.store()
        # print(data)
        myhelper = MysqlIns()
        myhelper.execute_ins(inser_sql, data)
        # 生成MySQL的类
        return item