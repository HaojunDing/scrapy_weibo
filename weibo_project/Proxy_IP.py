import requests
import time
# 定义一个获取IP的类
class ip_gather(object):
    def __init__(self):
        # 初始化进行调用类的操作
        self.ip_proxy_str = get_ip()
    #  如果遇到不好使的情况自动更换IP
    def update_ip_proxy(self):
        try:
            # 请求频繁会获取不到IP 这里睡眠一秒
            time.sleep(1)
            self.ip_proxy_str = get_ip()
            print('已获取到IP:'+self.ip_proxy_str)
            # 调用API接口在每次更新的时候显示余额
            jifen_url = ''
            print('当前余额还剩:', requests.get(jifen_url).json()['data'])
        except Exception as e :
            # 如果错误,走这里, 返回错误信息
            print('错误异常,请求次数频繁',e)

# 获取IP
def get_ip():
    time.sleep(1)
    url = ''
    html = requests.get(url).json()
    try:
        # 这里为获取IP的代码, 且返回STR格式IP:port
        response = html['data'][0]['IP']
        # print(type(response))
        # print(response)
        return response

    except Exception as e:
        # 如果错误 错误信息是非白名单的话,则自动添加到白名单里
        add_ip = html['msg'].split('登')[0]
        get_addip_url = 'http://http.zhiliandaili.cn/Users-whiteIpAddNew.html?appid=1527&appkey=24f2588817df6d461e3237e0ab32f1c7&whiteip={}&index='.format(add_ip)
        ok = requests.get(get_addip_url)
        time.sleep(1)
        # 睡眠一秒,防止频繁请求频繁
        # print(ok.json()['msg'])
        # 重新调用自己
        return get_ip()





if __name__ == '__main__':
    get = ip_gather()
    get.update_ip_proxy()