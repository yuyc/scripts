#!/usr/bin/env python
#coding:utf-8

import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import lxml
import re



sjtuentryurl = 'http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx'
user='FY14220063'
password='a19910912'

def get_view_state(soup):
    if soup:      
        view_input = soup.find(id="__VIEWSTATE")
        if view_input:
            return (view_input['value'])     
    print "The function %s args soup is empty" % 'get_ViewState'

cj = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)
response = opener.open(sjtuentryurl)
soup = BeautifulSoup(response.read(),'lxml')
viewstate = get_view_state(soup)
#
button2 = '.%E7%99%BB++%E5%BD%95.'
data = '__VIEWSTATE='+viewstate+'&user='+user+'&Password='+password+'&Button2='+button2   
login_request = urllib2.Request(sjtuentryurl,data)
req = opener.open(login_request)
def get_terminfo():
    '''
   获取学期信息，返回一个tuple
    '''
    url = 'http://www.sjtuce.net/xxpt/jrJxpjStuKb.aspx'
    req = urllib2.urlopen(url)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    tmp = soup.find_all('table',{'title':'上海交通大学继续教育学院上课安排'})
    lessons = {}
    for tr in tmp[0].find_all('tr'):
        lesson = tr.find_all('td')[1].string.strip().encode('utf-8')
        teacher = tr.find_all('td')[2].string.strip().encode('utf-8')
        lessons[lesson] = teacher
    term_regexp = re.compile(".*") 
    term = soup.find_all(selected=term_regexp)[0].string.strip()
    return (term,lessons)


def get_wkq():
    '''
    '''
    tmpurl = 'http://www.sjtuce.net/xxpt/jrJxpjStuCj.aspx'
    req = urllib2.urlopen(tmpurl)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    viewstate = get_view_state(soup)
    post = {'__EVENTTARGET':'',
            '__EVENTARGUMENT':'', 
            '__VIEWSTATE':viewstate,
            'button4':'显示所有成绩',
            '_ctl0:hid':''
            }
    postdata = urllib.urlencode(post)
    score_base_url = 'http://www.sjtuce.net/xxpt/jrJxpjStuCj.aspx'
    req = urllib2.urlopen(score_base_url,postdata)
    contents = response.read()
    print contents

get_wkq()
