def formatParameter(s):
    paramets={}
    for i in s.split('\n'):
        s2=i.strip()
        if s2:
            resultList = s2.split(':')  # 两个元素，键，值
            paramets[resultList[0].strip()]=resultList[1].strip()
    return paramets

if __name__ == '__main__':
    for i in formatParameter('''
    pageSize: 90
    cityId: 538
    workExperience: -1
    education: -1
    companyType: -1
    employmentType: -1
    jobWelfareTag: -1
    kw: python
    kt: 3
    at: ef96cd6f372245bc91638c9f7e3ba25f
    rt: 0cee8f638c7143628e8e8433a6722768
    _v: 0.32698880
    userCode: 691215620
    x-zp-page-request-id: 08472e9e781a46d88a01ef466cfe87b4-1553742569882-447139
    ''').items():
        print(i)