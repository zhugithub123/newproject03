from zhutool import data_tool as too
import MySQLdb

# 连接mysql库
connt=MySQLdb.connect(
    host="localhost",  # 数据库所在的主机ip
    port=3306,     #数据库的端口号
    user="root",    #数据库用户名
    password="123456",      #数据库密码
    db="eqwewq",  #数据库名
    charset="utf8"   #数据库的编码方式
)
#获取游标
cursor=connt.cursor()

works = ['python','爬虫','大数据']

for work in works:
    # for page in range(10):
    url = 'http://www.neitui.me/'

    headers = too.get_data_from_str('''
    Host: www.neitui.me
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36

    ''')
    page = 0
    while 1:
        print(page)
        data = too.get_data_from_str('''
            name: job
            handle: lists
            keyword: %s
            page: %s
            city:全国
            '''
            % (work, str(page)))
        print(data)
        data = too.get(url=url,data=data,headers=headers)
        # print(resp)

        urls = data.get_nodes_from_xpath('//a[@class="font16 max300"]/@href')

        data_url = ['http://www.neitui.me' + url for url in urls]
        alldata = too.gets(urls=data_url)

        # print(alldata)
        for datail in alldata:
            try:
                demand = datail.get_nodes_from_xpath('//div[@class="font16 mt10 mb10"]/span/text()')
                duties = datail.get_nodes_from_xpath('normalize-space(//div[@class="mb20 jobdetailcon"])')
                jobname = datail.get_nodes_from_xpath('//div[@class="c333 font26"]/text()')
                sql = "insert into neitui values(%s,%s,%s)"
                cursor.execute(sql,(str(demand), str(duties), str(jobname)))
                connt.commit()
            except:
                print('没数据')
        if urls:
            page += 1
        else:
            break

