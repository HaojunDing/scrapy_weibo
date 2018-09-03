# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from urllib import parse
from weibo_project.items import weiboProjectItem
from scrapy_redis.spiders import RedisSpider

class WeiboSpider(RedisSpider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    # start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0']
    redis_key = "daoun:weibo"


    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={}&containerid=107603{}'

    base_url = 'https://m.weibo.cn/api/container/getIndex?uid={}&containerid=107603{}&page={}'

    base_url_index_page = 'https://m.weibo.cn/api/container/getIndex?containerid=102803&openApp=0&page={}'

    def parse(self, response):
        '''
        :param response: 返回微博热门中的内容
        :return: 返回分页的微博url 进入parse_info 函数处理 获取热门中所有人的ID号
        '''
        html = json.loads(response.text)
        total = html['data']['cardlistInfo']['total']
        pages = total // 10
        # 首页热门分页
        for page in range(1, pages+1):
            url = self.base_url_index_page.format(page)
            yield scrapy.Request(url=url, callback=self.parse_info)

    def parse_info(self, response):
        '''
        :param response: 所有的微博热门内容
        :return: 返回用户微博内容给下一个函数进行处理
        '''
        uesr_list = json.loads(response.text)['data']['cards']
        for uesr in uesr_list[1:]:
            user_id = str(uesr['mblog']['user']['id'])
            user_url = self.user_url.format(user_id, user_id)
            print(user_url)
            yield scrapy.Request(url=user_url, callback=self.user_page_info)
        # print(html_json)

    def user_page_info(self,response):
        '''
        :param response: 接收用户微博信息内容 进行分页处理
        :return: 返回用户所有信息到下一个处理函数
        '''
        html = json.loads(response.text)
        total = html['data']['cardlistInfo']['total']
        pages = total // 10
        uid = html['data']['cards'][0]['mblog']['user']['id']

        name_url = self.base_url.format(uid, uid, 1)
        yield scrapy.Request(name_url, callback=self.name_info)
        for page in range(2, pages+1):
            url = self.base_url.format(uid, uid, page)
            yield scrapy.Request(url, callback=self.date_info)


    def date_info(self, response):
        item = weiboProjectItem()
        info_html = json.loads(response.text)
        info_list = info_html['data']['cards']
        for info in info_list:
            inf = info['mblog']
            date = inf['created_at']
            if date == '分钟' or '小时':
                date = datetime.date.today()
            zhuanfa = inf['reposts_count']
            pinglun = inf['comments_count']
            dianzan = inf['attitudes_count']
            user_id = inf['user']['id']
            user_name = inf['user']['screen_name']
            weibo_auth = inf['user']['description']
            jianjie = inf['user']['description']
            text = inf['text']
            source = inf['source']
            text_url = info['scheme']
            weibo_url = inf['user']['profile_url']
            item['user_name'] = user_name
            item['user_id'] = user_id
            item['weibo_auth'] = weibo_auth
            item['jianjie'] = jianjie
            item['text'] = text
            item['zhuanfa'] = zhuanfa
            item['dianzan'] = dianzan
            item['pinglun'] = pinglun
            item['date'] = date
            item['source'] = source
            item['text_url'] = text_url
            item['weibo_url'] = weibo_url
            # print(user_name,user_id,weibo_auth,jianjie,text,zhuanfa,dianzan,pinglun, date,source, text_url, weibo_url)
            yield item

    def name_info(self,response):
        users = json.loads(response.text)
        # print(users['data']['cards'])
        try:
            users_uid_list = users['data']['cards'][1]['card_group'][1]['elements']
            for users_id in users_uid_list:
                uid = users_id['uid']
                user_url = self.user_url.format(uid, uid)
                print(user_url)
                yield scrapy.Request(url=user_url, callback=self.user_page_info)
        except:
            print('没有推荐用户')