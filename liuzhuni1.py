# -*- coding: utf-8 -*-
import HTMLParser  
import urlparse  
import urllib  
import urllib2  
import cookielib  
import string  
import re  
import gzip
import sys



def ungzip(data):
    try:        # 尝试解压
        print '正在解压.....'
        data = gzip.decompress(data)
        print '解压完毕!'
    except:
        print '未经压缩, 无需解压'
    return data


def readhtml(posturl,postData,headers,filename):
    #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程  
    request = urllib2.Request(posturl, postData, headers)  

    try: 
        response = urllib2.urlopen(request)
        dir(response)
        print response.geturl()
        print response.getcode()
        print response.info() #返回的报头信息
    except urllib.HTTPError,e: 
        response = e  
        print response
        
    if response.code == 200: 
        text = response.read() 
        print "Data :", response.code 
    else: 
        print "ERRROR", response.code  

    response.close()

    text = text.decode('utf-8','replace').encode(sys.getfilesystemencoding()) 
    #转码:避免输出出现乱码 replace/ignore替换忽略

    text=ungzip(text)


    a=open(filename,'w')
    a.write(text)
    a.close()

    # re1=r'12345'
    # pattern=re.compile(re1)
    # match = pattern.findall(text)
    # print match

    if '削壁' in text:  
        print '登录成功',filename
    else:  
        print '登录失败' ,filename 


    print "="*30
    print "="*30





#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。  
headers = {'host':'www.liuzhuni.com',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
           'Referer':'http://www.liuzhuni.com/login',
           'Accept':'*/*',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           #'Accept-Encoding': 'gzip, deflate',
           'DNT': '1',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest',
           'Connection': 'keep-alive',
           'Pragma': 'no-cache',
           'Cache-Control': 'no-cache'
           }  
#构造Post数据，他也是从抓大的包里分析得出的。  
postData = {'account' : 'liufeisdh@163.com', #你的用户名  
            'password' : '201201'            #你的密码，密码可能是明文传输也可能是密文，如果是密文需要调用相应的加密算法加密  
            }    


#登录的主页面  
hosturl = 'http://www.liuzhuni.com' #自己填写    
  
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie  
cj = cookielib.LWPCookieJar()  
cookie_support = urllib2.HTTPCookieProcessor(cj)  
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
urllib2.install_opener(opener)  
  
#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
print hosturl
h = urllib2.urlopen(hosturl)  

#需要给Post数据编码  
postData = urllib.urlencode(postData)
#aa=urllib.quote("中文")#url编码


print "="*30

readhtml('http://www.liuzhuni.com/ajax/UserLogin',postData,headers,"aa.txt") #从数据包中分析出，处理post请求的url  
readhtml("http://www.liuzhuni.com/ajax/UserSignIn",postData,headers,"cc.txt")
