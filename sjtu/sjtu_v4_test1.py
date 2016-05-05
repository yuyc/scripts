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


class classmate(object):
    """docstring for classmate"""
    def __init__(self, user, password):    
        self.sjtu_login_url = 'http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx'
        self.sjtu_mainnew_url = 'http://www.sjtuce.net/xxpt/jrJxpjMainNew.aspx'
        self.reqcookielist = []
        self.user = user
        self.password = password
        self.cookie = self.get_login_cookie(user,password)['cookie']

    def url_transfer_str(self,str):
        str = urllib.quote_plus(str)
        return str

    def get_viewstate_str(self,soup):
        if soup:      
            view_input = soup.find(id="__VIEWSTATE")
            if view_input:
                return (view_input['value'])     
        print "The function %s args soup is empty" % 'get_ViewState'
  
    def get_eventvalidation_str(self,soup):
        if soup:        
            event_input = soup.find(id="__EVENTVALIDATION")
            if event_input:
                return event_input['value']
        print "The function %s args soup is empty" % 'get_EventValidation'

    def get_request_cookie(self,url):
        cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(handler)

        response = opener.open(url)
        contents = response.read()
        soup = BeautifulSoup(contents,'lxml')
        viewstatestr = self.get_viewstate_str(soup)
        for item in cookie:
            tmpstr = item.name+'='+item.value
            self.reqcookielist.append(tmpstr)
        return self.reqcookielist[0]

    def get_login_cookie(self,user,password):
        postdirc = {}
        reqcookielist = self.get_request_cookie(self.sjtu_login_url)
        cookiestr = "".join(reqcookielist[0])
        user = user
        password = password
        button2 = '.%E7%99%BB++%E5%BD%95.'
        student_cookie = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(student_cookie)
        opener = urllib2.build_opener(handler)
        viewstate = reqcookielist[-1] 
        data = '__VIEWSTATE='+viewstate+'&user='+user+'&Password='+password+'&Button2='+button2   
        login_request = urllib2.Request(self.sjtu_login_url,data)
        req = opener.open(login_request,data)
        contents = req.read()
        soup = BeautifulSoup(contents,'lxml')
        ViewStateStr = self.get_viewstate_str(soup)
        postdirc['cookie'] = student_cookie
        postdirc['viewstate'] = ViewStateStr
        return postdirc

    def GetTerminfo(self):
        '''
       获取学期信息，返回一个tuple
        '''
        url = 'http://www.sjtuce.net/xxpt/jrJxpjStuKb.aspx'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
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

    def CheckingAttendance(self):
        url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
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

    def Click(self,Eventtarget,Lessiondate,LessionMark,ViewStateStr):
        jsclick = urllib.quote_plus(Eventtarget)
        xueqi = urllib.quote_plus(Lessiondate)
        dplKc = urllib.quote_plus(LessionMark)
        viewstatestr = urllib.quote_plus(ViewStateStr)
        postdata = '__EVENTTARGET='+jsclick+'&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+viewstatestr+'&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3Ahid='
        url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
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


    def GetDownloadUrls(self,Lessiondate,LessionMark):
        xueqi = urllib.quote_plus(Lessiondate)
        dplKc = urllib.quote_plus(LessionMark)
        postdata = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKMTkyNDkzMjQ0NQ9kFgJmD2QWBAIDDw8WAh4EVGV4dAUURlkxNDIyMDA2Myzkuo7popzlt51kZAIFD2QWBgIBD2QWBgICDxBkDxYBZhYBEAULMjAxNS0yMDE2LjEFCzIwMTUtMjAxNi4xZ2RkAgYPEGQQFQQT5b6Q5oWn5aifLee7j%2Ba1juWtpivmnLHmuIXmnqst5oCd5oOz6YGT5b635L%2Bu5YW75LiO5rOV5b6L5Z%2B656GAFOeOi%2BW5sy3lpKflraboi7Hor60yHOi1teS%2FiuWSjC3kurrlipvotYTmupDnrqHnkIYVBBAxNTE2MTAzOSAgfDI5NjgwEDE1MTYxMDE0ICB8Mjk2ODcQMTUxNjEwMDIgIHwyOTY3ORAxNTE2MTAzNSAgfDI5NjcwFCsDBGdnZ2dkZAIKDzwrAAsAZAIFDw8WAh8ABQEwZGQCBg8PFgIfAAWOAeW9k%2BWJjeWtpuacnzoyMDE1LTIwMTYuMSgyMDE1LTA5LTA36IezMjAxNi0wMS0xNynmnKzlkajkuLrnrKwxMyAg5ZGoICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfOePreS4u%2BS7uzrpq5jmhacoNjQ0ODAwMjItMTEwNSlkZGSlzRtROgp16LU1R6%2FtV0u08rLywtXF7LkYnohnoz%2F4VQ%3D%3D&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3AMainContent%3AButton4=%E6%98%BE%E7%A4%BA&_ctl0%3Ahid='
        url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        req = urllib2.urlopen(url,postdata)
        contents = req.read()
        soup = BeautifulSoup(contents,'lxml')
        viewstatestr = self.get_viewstate_str(soup)
        tmp = soup.find_all(name='a',text='点击下载')
        for a in tmp:
            Eventtarget = a.attrs.get('href').split('\'')[1]
            self.Click(Eventtarget,Lessiondate,LessionMark,viewstatestr)
        print LessionMark+' 任务完成' 


    def get_urlviewstate_str(self,url,postdata=None):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        if postdata:
            req = urllib2.urlopen(url,postdata)
        else:
            req = urllib2.urlopen(url)
        contents = req.read()
        soup = BeautifulSoup(contents,'lxml')
        viewstatestr = self.get_viewstate_str(soup)
        return viewstatestr

    def down_videos_main(self, Lessiondate, LessionMark,typestr):
        url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
        xueqi = urllib.quote_plus(Lessiondate)
        dplKc = urllib.quote_plus(LessionMark)
        viewstatestr = urllib.quote_plus(self.get_urlviewstate_str(url))
        postdata = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+viewstatestr+'&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3AMainContent%3AButton4=%E6%98%BE%E7%A4%BA&_ctl0%3Ahid='
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        req = urllib2.urlopen(url,postdata)
        contents = req.read()
        soup = BeautifulSoup(contents,'lxml')
        tmp = soup.find_all(name='a',text='点击下载')
        viewstatestr = urllib.quote_plus(self.get_urlviewstate_str(soup))
        for a in tmp:
            Eventtarget = a.attrs.get('href').split('\'')[1]
            typestr = int(typestr)
            if typestr == 0:
                self.Click(Eventtarget,Lessiondate,LessionMark, viewstatestr)
            elif typestr == 1:
                self.down_videos_save_files(Eventtarget, Lessiondate, LessionMark, viewstatestr)
        print LessionMark+' 任务完成' 


    def down_videos_save_files(self, Eventtarget, Lessiondate, LessonMark, viewstatestr):
        jsclick = urllib.quote_plus(Eventtarget)
        xueqi = urllib.quote_plus(Lessiondate)
        dplKc = urllib.quote_plus(LessonMark)
        postdataA = '__EVENTTARGET='+jsclick+'&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE='+viewstatestr+'&_ctl0%3AMainContent%3Am_cbxXueqi='+xueqi+'&_ctl0%3AMainContent%3AdplKc='+dplKc+'&_ctl0%3Ahid='
        url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'    
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        opener.add_handler = urllib2.FTPHandler()
        opener.add_handler = urllib2.HTTPHandler(debuglevel=logging.DEBUG)
        opener.add_handler = urllib2.HTTPSHandler(debuglevel=logging.DEBUG)
        opener.add_handler = urllib2.HTTPRedirectHandler()
        urllib2.install_opener(opener)
        req = urllib2.urlopen(url,postdataA)
        filename = os.path.basename(req.geturl())
        file_buffer = ""
        lessonname = self.get_download_directory_name(Lessiondate,LessonMark)
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

    def get_lessons_info(self):
        url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
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

    def get_download_directory_name(self,Lessiondate,lessonmask):
        lessonsinfo = self.get_lessons_info()
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
        yuyc = classmate()
        lessons = yuyc.CheckingAttendance()
        for i in lessons:
            for xueqi,lm in i.items():
                yuyc.down_videos_main(xueqi, lm, 0)
        # print get_download_directory_name("2015-2016.2","15162007  |30490")
