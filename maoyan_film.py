"""
爬取猫眼电影中榜单栏目中Top100的所有电影信息，并将信息写入文件
"""
from urllib import request,error
import re,time,json

def getPage(url):
    """
    爬取指定url页面信息
    :param url: url地址
    :return:
    """
    try:
        #定义请求头信息
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'
        }
        #封装请求对象
        req = request.Request(url, headers=headers)
        #执行爬取
        res = request.urlopen(req)
        #判断响应状态，并响应爬取内容
        if res.code == 200:
            return res.read().decode("utf-8")
        else:
            return None
    except error.URLError:
        return None

def parsePage(html):
    """
    解析爬取网页中的内容，并返回字段结果
    :param html: 网页内容
    :return: 字段结果
    """
    #定义正则表达式
    pat = '<i class="board-index board-index-[0-9]+">([0-9]+)</i>.*?<img data-src="(.*?)" alt="(.*?)" class="board-img" />.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?<i class="integer">([0-9\.]+)</i><i class="fraction">([0-9]+)</i>'
    #执行解析
    items = re.findall(pat, html, re.S)
    #遍历封装数据并返回
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6],
        }

def writefile(content):
    """
    执行文件追加写操作
    :param content:
    :return:
    """
    with open("./result.txt", 'a', encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False)+"\n")

def main():
    """
    主程序函数，负责调度执行爬虫处理
    :param offset:
    :return:
    """
    url = 'http://maoyan.com/board/'
    html = getPage(url)
    #判断是否爬取到数据，并调用解析函数
    if html:
        for item in parsePage(html):
            writefile(item)

if __name__ == '__main__':
    for i in range(10):
        main()
        time.sleep(1)