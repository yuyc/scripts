#!/usr/bin/env python
#coding:utf-8

import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
import re
import logging
import os
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


SjtuEntryUrl = 'http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx'
SjtuNewUrl = 'http://www.sjtuce.net/xxpt/jrJxpjMainNew.aspx'
reqcookielist = []
user='FY14220063'
password='a19910912'

def UrlTransfer(str):
    str = urllib.quote_plus(str)
    return str

def get_ViewState(soup):
    if soup:      
        view_input = soup.find(id="__VIEWSTATE")
        if view_input:
            return (view_input['value'])     
    print "The function %s args soup is empty" % 'get_ViewState'
  
def get_EventValidation(soup):
    if soup:        
        event_input = soup.find(id="__EVENTVALIDATION")
        if event_input:
            return event_input['value']
    print "The function %s args soup is empty" % 'get_EventValidation'

def getreqcookie(url):
    url = url 
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)

    response = opener.open(url)
    contents = response.read()
    soup = BeautifulSoup(contents,'lxml')
    ViewStateStr = get_ViewState(soup)
    for item in cookie:
        tmpstr = item.name+'='+item.value
        reqcookielist.append(tmpstr)
    reqcookielist.append(ViewStateStr)
    return reqcookielist
def getlogincookie(user,password):
    postdirc = {}
    reqcookielist = getreqcookie(SjtuEntryUrl)
    cookiestr = "".join(reqcookielist[0])
    user = user
    password = password
    button2 = '.%E7%99%BB++%E5%BD%95.'
    student_cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(student_cookie)
    opener = urllib2.build_opener(handler)
    viewstate = reqcookielist[-1] 
    data = '__VIEWSTATE='+viewstate+'&user='+user+'&Password='+password+'&Button2='+button2   
    login_request = urllib2.Request(SjtuEntryUrl,data)
    req = opener.open(login_request,data)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    ViewStateStr = get_ViewState(soup)
    postdirc['cookie'] = student_cookie
    postdirc['viewstate'] = ViewStateStr
    return postdirc

def GetTerminfo():
    '''
   获取学期信息，返回一个tuple
    '''
    url = 'http://www.sjtuce.net/xxpt/jrJxpjStuKb.aspx'
    cookie = getlogincookie(user,password)['cookie']
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
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

def CheckingAttendance():
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    cookie = getlogincookie(user,password)['cookie']
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    tmp = soup.find_all('select',{'name':'_ctl0:MainContent:dplKc'})
    lessons = []
    xueqi = soup.find('select',{'name':'_ctl0:MainContent:m_cbxXueqi'}).find('option').attrs.get('value')
    for option in tmp[0].find_all('option'):
        lm = option.attrs.get('value')
        lessons.append({xueqi:lm})
    return lessons

def Click(Eventtarget,Lessiondate,LessionMark,ViewStateStr):
    jsclick = urllib.quote_plus(Eventtarget)
    xueqi = urllib.quote_plus(Lessiondate)
    dplKc = urllib.quote_plus(LessionMark)
    cookie = getlogincookie(user,password)['cookie']
    viewstatestr = urllib.quote_plus(ViewStateStr)
    postdata = '__EVENTTARGET='+jsclick+'&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+viewstatestr+'&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3Ahid='
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.add_handler = urllib2.FTPHandler()
    opener.add_handler = urllib2.HTTPHandler(debuglevel=logging.DEBUG)
    opener.add_handler = urllib2.HTTPSHandler(debuglevel=logging.DEBUG)
    opener.add_handler = urllib2.HTTPRedirectHandler()
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url,postdata)
    print req.geturl()
    print req.headers
    print dir(req)
    print req.fp.read(1024)
    print '打卡完毕'
"""    import sys
    sys.exit()"""


def GetDownloadUrls(Lessiondate,LessionMark):
    xueqi = urllib.quote_plus(Lessiondate)
    dplKc = urllib.quote_plus(LessionMark)
    postdata = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKMTkyNDkzMjQ0NQ9kFgJmD2QWBAIDDw8WAh4EVGV4dAUURlkxNDIyMDA2Myzkuo7popzlt51kZAIFD2QWBgIBD2QWBgICDxBkDxYBZhYBEAULMjAxNS0yMDE2LjEFCzIwMTUtMjAxNi4xZ2RkAgYPEGQQFQQT5b6Q5oWn5aifLee7j%2Ba1juWtpivmnLHmuIXmnqst5oCd5oOz6YGT5b635L%2Bu5YW75LiO5rOV5b6L5Z%2B656GAFOeOi%2BW5sy3lpKflraboi7Hor60yHOi1teS%2FiuWSjC3kurrlipvotYTmupDnrqHnkIYVBBAxNTE2MTAzOSAgfDI5NjgwEDE1MTYxMDE0ICB8Mjk2ODcQMTUxNjEwMDIgIHwyOTY3ORAxNTE2MTAzNSAgfDI5NjcwFCsDBGdnZ2dkZAIKDzwrAAsAZAIFDw8WAh8ABQEwZGQCBg8PFgIfAAWOAeW9k%2BWJjeWtpuacnzoyMDE1LTIwMTYuMSgyMDE1LTA5LTA36IezMjAxNi0wMS0xNynmnKzlkajkuLrnrKwxMyAg5ZGoICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfOePreS4u%2BS7uzrpq5jmhacoNjQ0ODAwMjItMTEwNSlkZGSlzRtROgp16LU1R6%2FtV0u08rLywtXF7LkYnohnoz%2F4VQ%3D%3D&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3AMainContent%3AButton4=%E6%98%BE%E7%A4%BA&_ctl0%3Ahid='
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    cookie = getlogincookie(user,password)['cookie']
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url,postdata)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    viewstatestr = get_ViewState(soup)
    tmp = soup.find_all(name='a',text='点击下载')
    for a in tmp:
        Eventtarget = a.attrs.get('href').split('\'')[1]
        Click(Eventtarget,Lessiondate,LessionMark,viewstatestr)
    print LessionMark+' 任务完成' 


def GetUrlViewstate(url,postdata=None):
    cookie = getlogincookie(user,password)['cookie']
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    if postdata:
        req = urllib2.urlopen(url,postdata)
    else:
        req = urllib2.urlopen(url)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    viewstatestr = get_ViewState(soup)
    return viewstatestr

def GetVideosUrls(Lessiondate,LessionMark):
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    xueqi = urllib.quote_plus(Lessiondate)
    dplKc = urllib.quote_plus(LessionMark)
    cookie = getlogincookie(user,password)['cookie']
    viewstatestr = urllib.quote_plus(GetUrlViewstate(url))
    postdata = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+viewstatestr+'&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3AMainContent%3AButton4=%E6%98%BE%E7%A4%BA&_ctl0%3Ahid='
    req = urllib2.urlopen(url,postdata)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    tmp = soup.find_all(name='a',text='点击下载')
    viewstatestr = urllib.quote_plus(get_ViewState(soup))
    for a in tmp:
        Eventtarget = a.attrs.get('href').split('\'')[1]
        DownVideos(Eventtarget,Lessiondate,LessionMark,viewstatestr)
    print LessionMark+' 任务完成' 


def DownVideos(Eventtarget,Lessiondate,LessonMark,viewstatestr):
    jsclick = urllib.quote_plus(Eventtarget)
    xueqi = urllib.quote_plus(Lessiondate)
    dplKc = urllib.quote_plus(LessonMark)
    cookie = getlogincookie(user,password)['cookie']
    postdataA = '__EVENTTARGET='+jsclick+'&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+viewstatestr+'&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3Ahid='
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.add_handler = urllib2.FTPHandler()
    opener.add_handler = urllib2.HTTPHandler(debuglevel=logging.DEBUG)
    opener.add_handler = urllib2.HTTPSHandler(debuglevel=logging.DEBUG)
    opener.add_handler = urllib2.HTTPRedirectHandler()
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url,postdataA)
    filename = os.path.basename(req.geturl())
    file_buffer = ""
    lessonname = get_download_directory_name(Lessiondate,LessonMark)
    print("开始下载:%s" % (lessonname,))
    while True:
        data = req.fp.read(20480000)
        
        if not data:
            break
        else:
            file_buffer += data
    try:
        if os.path.isdir(lessonname):
            pass
        else:
            os.mkdir(lessonname)
        file_descriptor = open("%s/%s" % (lessonname,filename),"wb")
        file_descriptor.write(file_buffer)
        file_descriptor.close()
        print("下载成功!")
    except:
        print("Error")


    # contents = req.read()

    # soup = BeautifulSoup(contents,'lxml')
    # viewstatestr = get_ViewState(soup)
    #print viewstatestr
    # print req.code
    # print contents

    #print viewstatestr
    # postdataB = '__EVENTTARGET='+jsclick+'&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+viewstatestr+'&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3Ahid='
    # req = urllib2.urlopen(url,postdataA)
    #print req.read()
    # print req.headers
    # print req.geturl()
    # print req.headers
    # print dir(req)
    # print req.fp.read(1024)
    # print '打卡完毕'

def get_lessons_info():
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    cookie = getlogincookie(user,password)['cookie']
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url)
    contents = req.read()
    soup = BeautifulSoup(contents,'lxml')
    tmp = soup.find_all('select',{'name':'_ctl0:MainContent:dplKc'})
    xueqi = soup.find('select',{'name':'_ctl0:MainContent:m_cbxXueqi'}).find('option').attrs.get('value')
    lessonsinfo = {xueqi:{}}
    for option in tmp[0].find_all('option'):
        lessonmask = option.attrs.get('value')
        lessonname = option.string.split("-")[1]
        lessontecher = option.string.split("-")[0]
        lessonsinfo[xueqi].update({lessonmask:{lessontecher:lessonname}})
    return lessonsinfo

def get_download_directory_name(Lessiondate,lessonmask):
    lessonsinfo = get_lessons_info()
    dirname = []
    if lessonsinfo.has_key(Lessiondate):
        data = lessonsinfo.get(Lessiondate).get(lessonmask,'Not data')
        for k,v in data.items():
            dirname.append(k)
            dirname.append(v)
    else:
        data = "Not found"
    name = ''.join(dirname)
    return name






if __name__ == '__main__':
    
    # msg = GetTerminfo()
    # for i in msg[1]:
    #     print i
    
    # lessons = CheckingAttendance()
    # for i in lessons:
    #     for xueqi,lm in i.items():
    #         down_videos_main(xueqi,lm)
    # print get_download_directory_name("2015-2016.2","15162007  |30490")
    GetVideosUrls("2015-2016.2","15162002  |29667")