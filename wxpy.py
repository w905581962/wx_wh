from wxpy import *
import requests
import re
import datetime
import time

#登录并缓存
bot = Bot(console_qr=True,cache_path=True)

'''获取URL页面信息'''
def get_html(url):
    kv = {'user-agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=kv)
    r.encoding='utf-8'
    html = r.text
    pattern = re.compile('全国天气预报</a>.*?</a>&nbsp;&gt;&nbsp;(.*?)</h1>.*?class="dname">(.*?)</p><br>'
    +'<p>(.*?)</p> </td>.*?class="wdesc">(.*?)</td>.*?class="temp">(.*?)</td>.*?class="direct">(.*?)</td>'
    +'.*?class="power">(.*?)</td>',re.S)
    didian = re.findall(pattern,html)#得到的是列表，都在一项里
    tianqi = didian[0]
    daishan = tianqi[0]
    today = tianqi[1]+tianqi[2]
    C = tianqi[3]+tianqi[4]
    feng = tianqi[5]+tianqi[6]
    sms = "来源：王雨秋为您抓取中央气象台数据"
    fasong = '\t%s\t\n\t%s\t\n\t%s\t\n\t%s\t\n%s'%(daishan,today,C,feng,sms)
    return fasong

def main():
    url = "http://www.nmc.cn/publish/forecast/AZJ/hangzhou.html"
    url1 = "http://www.nmc.cn/publish/forecast/AZJ/daishan.html"
    url2 = "http://www.nmc.cn/publish/forecast/ABJ/beijing.html"
    while 1:
        now = datetime.datetime.now() #获取当前时间
        now_str = now.strftime('%Y/%m/%d %H:%M:%S')[11:] #把时间转换成str类型并切片
        if now_str == '06:30:00': #if判断
            #获取天气信息str
            string_one = get_html(url) 
            string_two = get_html(url1)
            string_three = get_html(url2)
            #发送
            my_frend = bot.friends().search(u'谈谈')[0]
            my_frend.send(string_one)
            my_frend = bot.friends().search(u'妈')[0]
            my_frend.send(string_two)
            my_frend = bot.friends().search(u'爸')[0]
            my_frend.send(string_three)
        time.sleep(1)#延迟

if __name__ == '__main__':
    main()
                  