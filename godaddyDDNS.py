import urllib.request
import json
import time
import ssl
import random
################### Modify to your own information ###################
#domain name 域名
DOMAIN_NAME = '{your domain}'

#API Authorization ---Godaddy的API授权密钥，可以在https://developer.godaddy.com/keys中申请
API_KEY= '{your api key}'
API_SECRET = '{your api Secret}'
AuthorKey = f'sso-key {API_KEY}:{API_SECRET}'

#https://api.godaddy.com/v1/domains/{domain}/records   官方接口 
api_url = f'https://api.godaddy.com/v1/domains/{DOMAIN_NAME}/records'
head = {}
head['Accept'] = 'application/json'
head['Content-Type'] = 'application/json'
head['Authorization'] = AuthorKey

#record name 要定时修改的记录名
record_name = "{record name}"

#########################################################################
context = ssl._create_unverified_context()#跳过SSL验证
old_IP = ""

#获取当前IP ifconfig.me
def getIp1():
    try:
        #获取当前ip
        url = 'https://ifconfig.me/ip'
        req = urllib.request.Request(url)
        rsp=urllib.request.urlopen(req)
        html=rsp.read().decode('utf-8',"ignore")
        ip_addr=html.strip()
        print("getIp1:",ip_addr)
        return ip_addr
    except Exception as e:
        print("getIp1 Exception:",e)
        return None

#获取当前IP checkip.amazonaws.com
def getIp2():
    try:
        #获取当前ip
        url = 'https://checkip.amazonaws.com'
        req = urllib.request.Request(url)
        rsp=urllib.request.urlopen(req)
        html=rsp.read().decode('utf-8',"ignore")
        ip_addr=html.strip()

        print("getIp2:",ip_addr)
        return ip_addr
    except Exception as e:
        print("getIp2 Exception:",e)
        return None

#获取当前IP ipv4.icanhazip.com
def getIp3():
    try:
        #获取当前ip
        url = 'https://ipv4.icanhazip.com'
        req = urllib.request.Request(url)
        rsp=urllib.request.urlopen(req)
        html=rsp.read().decode('utf-8',"ignore")
        ip_addr=html.strip()

        print("getIp3:",ip_addr)
        return ip_addr
    except Exception as e:
        print("getIp3 Exception:",e)
        return None

#随机调用getIP站点，避免频繁调用被限流
getIPList = [getIp1, getIp2, getIp3]
def getIp():
    while True:
        funcGetIp = random.choice(getIPList)
        ip_addr = funcGetIp()
        if ip_addr == None:
            time.sleep(30)   
        else:
            return ip_addr

#取回原有的DNS记录
def retrieve():
    global api_url
    global head
    global context
    while True:
        try:
            req = urllib.request.Request(api_url,headers = head,  method = "GET")
            rsp = urllib.request.urlopen(req, context=context)
            html=rsp.read().decode('utf-8',"ignore")

            return eval(html)
        except Exception as e:
            print("retrieve Exception:",e)
            time.sleep(30)

#执行更新流程
def update():
    global api_url
    global head
    global context
    global old_IP

    records = None
    #先取回原有的DNS记录，因为API的PUT接口会覆盖所有DNS记录
    if old_IP == None or old_IP == "":
        records = retrieve()
        for rec in records:
            if rec["name"] == record_name:
                old_IP = rec["data"]

    #获取当前IP
    ip_addr = getIp()
    #IP没有变更则忽略
    if old_IP == ip_addr:
        print('IP无变化，无需提交更新'+ip_addr)
        return
        
    #上面如果取过就不取，降低查询频率
    if records == None:
        records = retrieve()

    # 官方的默认dns信息，如果不带上，会返回422错误
    records_NS01 = {
    "data" : "ns19.domaincontrol.com",
    "name" : "@",
    "ttl" : 3600,
    "type" : "NS",
    }
    records_NS02 = {
    "data" : "ns20.domaincontrol.com",
    "name" : "@",
    "ttl" : 3600,
    "type" : "NS",
    }
    
    #替换掉records中原有的record_name的IP值
    for rec in records:
        if rec["name"] == record_name:
            rec["data"] = ip_addr

    #执行更新请求
    while True:
        try:
            req = urllib.request.Request(api_url,headers = head, data = json.dumps(records).encode(), method = "PUT")
            rsp = urllib.request.urlopen(req, context=context)
            code = rsp.getcode()
            if code == 200:
                old_IP = ip_addr#保存更新后的IP记录
                print('成功更新域名解析：'+ip_addr+time.strftime("  AT  %Y-%m-%d %H:%M:%S", time.localtime()))
                break
            else:
                print('更新失败：'+code)
                time.sleep(30)
        except Exception as e:
            print("update Exception:",e)
            time.sleep(30)


if __name__ == "__main__":
    while True:
        update()
        time.sleep(300)#五分钟检查一次

