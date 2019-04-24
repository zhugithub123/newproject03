import aiohttp
import asyncio
import json
from lxml import etree

result=[]
loop=asyncio.get_event_loop()
async def main(url, method, params=None, data=None, json=None, headers=None, cookies=None, proxy=None, timeout=None):
    async with aiohttp.ClientSession() as s:
        async with s.request(url=url,method=method,params=params,data=data,json=json,headers=headers,cookies=cookies,proxy=proxy,timeout=timeout) as resp:
            result.append(AI153Response(await resp.read(),resp))

# 发送一个get请求
def get(url,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    return __requests([url], 'GET', params=data, data=None, json=json, headers=headers, cookies=cookies, proxy=proxy, timeout=timeout)[0]

def __requests(urls,method,params=None,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    tasks=[]
    for url in urls:
        tasks.append(asyncio.ensure_future(main(url=url, method=method, params=params, data=data, json=json, headers=headers, cookies=cookies, proxy=proxy, timeout=timeout)))
    loop.run_until_complete(asyncio.wait(tasks))
    return result

# # 发送一个post请求
def post(url,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    return __requests([url], 'POST', params=None, data=data, json=json, headers=headers, cookies=cookies, proxy=proxy, timeout=timeout)[0]

# # 发送一堆get请求
def gets(urls,data=None,json=None,headers=None,cookies=None,proxy=None,timeout=None):
    return __requests(urls, 'GET', params=None, data=None, json=None, headers=None, cookies=None, proxy=None, timeout=None)

# 参数,headers抽取工具
def get_data_from_str(s):
    hehe={}
    for i in s.split('\n'):
        s2=i.strip()
        if s2:
            resultList = s2.split(':')  #两个元素，键，值
            if len(resultList)==2:
                hehe[resultList[0].strip()]=resultList[1].strip()
            else:
                hehe[resultList[0].strip()] = resultList[1].strip()+resultList[2].strip()
    return hehe
# # cookies 抽取工具
def get_cookies_from_str(s):
    hehe={}
    for i in s.split(';'):
        s2=i.strip()
        if s2:
            resultList = s2.split('=')  #两个元素，键，值
            hehe[resultList[0].strip()]=resultList[1].strip()
    return hehe

# 根据json，key获取value
def get_values_from_key(json,result,key):
# 如何递归解析json？result = []
# Vaule =’’
    value=''
# 判断json对象的类型
    if isinstance(json,dict):
# 是字典：
# 判断key是否在json的keys里面
        if key in json.keys():
        # 在，直接通过键取值
        # vaule = json[key]
            value=json.get(key)
        # 不在
        else:
        # 遍历当前json的values，继续这个操作
            for v in json.values():
                get_values_from_key(v,result,key)
# 是列表：遍历，再进行这个操作
    elif isinstance(json,list):
        for v in json:
            get_values_from_key(v,result,key)
# 判断value是否为空：
    # 不为空
    if value:
        # 添加到result中
        result.append(value)
    # 返回result
    return result


class AI153Response():
    def __init__(self,content,resp):
        self.content=content
        self.resp=resp
# # 响应的处理
# # 获得一个节点
    def get_node_from_xpath(self,str):
        return etree.HTML(self.content).xpath(str)[0]
# # 获得多个节点
    def get_nodes_from_xpath(self, str):
        return etree.HTML(self.content).xpath(str)
    # # 根据key获得json中的一个value
    def get_value_from_key(self,key):
        return get_values_from_key(json.loads(self.text()),[],key)[0]
# # 根据key获得json中的多个value
    def get_values_from_key(self,key):
        return get_values_from_key(json.loads(self.text()),[],key)
#  保存二进制
# resp.save(filename)
    def save(self,filepath):
        with open(filepath,'wb')as w:
            w.write(self.content)
# # 返回二进制
# resp.body
    @property
    def body(self):
        return self.content
# # 返回字符串
# resp.text
    def text(self,encoding=None):
        try:
            return self.content.decode('utf-8')
        except:
            return self.content.decode('gbk')
# # 返回的cookies
    @property
    def cookies(self):
        return self.resp.cookies
# # 返回的heades
    @property
    def headers(self):
        return self.resp.headers
# # 请求的url
    @property
    def url(self):
        return self.resp.url

