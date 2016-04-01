#!/usr/bin/env python
# coding:utf-8

import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup

SjtuEntryUrl = 'http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx'
SjtuNewUrl = 'http://www.sjtuce.net/xxpt/jrJxpjMainNew.aspx'
reqcookielist = []
user = ''
password = ''


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
    soup = BeautifulSoup(contents, 'lxml')
    ViewStateStr = get_ViewState(soup)
    for item in cookie:
        tmpstr = item.name + '=' + item.value
        reqcookielist.append(tmpstr)
    reqcookielist.append(ViewStateStr)
    return reqcookielist


def getlogincookie(user, password):
    postdirc = {}
    reqcookielist = getreqcookie(SjtuEntryUrl)
    cookiestr = "".join(reqcookielist[0])
    user = user
    password = password
    button2 = '.%E7%99%BB++%E5%BD%95.'
    student_cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(student_cookie)
    opener = urllib2.build_opener(handler)
    agent = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
             'Connection': 'keep-alive',
             'Cookie': cookiestr,
             'Host': 'www.sjtuce.net',
             'Referer': 'http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx',
             'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
             }
    viewstate = reqcookielist[-1]
    data = '__VIEWSTATE=' + viewstate + '&user=' + user + \
        '&Password=' + password + '&Button2=' + button2
    login_request = urllib2.Request(SjtuEntryUrl, data)
    req = opener.open(login_request, data)
    contents = req.read()
    soup = BeautifulSoup(contents, 'lxml')
    ViewStateStr = get_ViewState(soup)
    postdirc['cookie'] = student_cookie
    postdirc['viewstate'] = ViewStateStr
    return postdirc


def GetTerminfo():
    '''
   获取学期信息，返回一个tuple
    '''
    url = 'http://www.sjtuce.net/xxpt/jrJxpjStuKb.aspx'
    cookie = getlogincookie(user, password)['cookie']
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url)
    contents = req.read()
    soup = BeautifulSoup(contents, 'lxml')
    tmp = soup.find_all('table', {'title': '上海交通大学继续教育学院上课安排'})
    lessons = {}
    for tr in tmp[0].find_all('tr'):
        lesson = tr.find_all('td')[1].string.strip().encode('utf-8')
        teacher = tr.find_all('td')[2].string.strip().encode('utf-8')
        lessons[lesson] = teacher
    term_regexp = re.compile(".*")
    term = soup.find_all(selected=term_regexp)[0].string.strip()
    return (term, lessons)


def CheckingAttendance():
    postdirc = getlogincookie(user, password)
    viewstate = urllib.quote_plus(postdicr['viewstate'])
    cookie = postdicr['cookie']
    postdata = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=' + viewstate + \
        '&_ctl0%3AMainContent%3Am_cbxXueqi=2015-2016.1&_ctl0%3AMainContent%3AdplKc=15161039++%7C29680&_ctl0%3AMainContent%3AButton4=%E6%98%BE%E7%A4%BA&_ctl0%3Ahid='
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url, postdata)
    contents = req.read()
    print contents
    '''
    soup = BeautifulSoup(contents,'lxml')
    tmp = soup.find_all('select',{'name':'_ctl0:MainContent:dplKc'})
    lessons = []
    xueqi = soup.find('select',{'name':'_ctl0:MainContent:m_cbxXueqi'}).find('option').attrs.get('value')
    for option in tmp[0].find_all('option'):
        lm = option.attrs.get('value')
        lessons.append({xueqi:lm})
    return lessons
    '''


def Click(Eventtarget, Lessiondate, LessionMark):
    jsclick = urllib.quote_plus(Eventtarget)
    xueqi = urllib.quote_plus(Lessiondate)
    dplKc = urllib.quote_plus(LessionMark)
    postdata = '__EVENTTARGET=' + jsclick + '&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKMTkyNDkzMjQ0NQ9kFgJmD2QWBAIDDw8WAh4EVGV4dAUURlkxNDIyMDA2Myzkuo7popzlt51kZAIFD2QWBgIBD2QWBgICDxBkDxYBZhYBEAULMjAxNS0yMDE2LjEFCzIwMTUtMjAxNi4xZ2RkAgYPEGQQFQQT5b6Q5oWn5aifLee7j%2Ba1juWtphTnjovlubMt5aSn5a2m6Iux6K%2BtMivmnLHmuIXmnqst5oCd5oOz6YGT5b635L%2Bu5YW75LiO5rOV5b6L5Z%2B656GAHOi1teS%2FiuWSjC3kurrlipvotYTmupDnrqHnkIYVBBAxNTE2MTAzOSAgfDI5NjgwEDE1MTYxMDAyICB8Mjk2NzkQMTUxNjEwMTQgIHwyOTY4NxAxNTE2MTAzNSAgfDI5NjcwFCsDBGdnZ2dkZAIKDzwrAAsBAA8WCB4IRGF0YUtleXMWAB4LXyFJdGVtQ291bnQCBh4JUGFnZUNvdW50AgEeFV8hRGF0YVNvdXJjZUl0ZW1Db3VudAIGZBYCZg9kFgwCAQ9kFg5mDw8WAh8ABQExZGQCAQ8PFgIfAAURMjAxNS85LzggMTg6MjA6MDBkZAICDw8WAh8ABYkC56ysMSDmrKEx6IqCKOesrDEg6K6yKSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRkAgMPDxYCHwAFETIwMTUvOS84IDIyOjA0OjAwZGQCBA8PFgIfAAX%2FAS53bXYgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRkAgcPDxYCHwAFG2t4bC8xMzE0MTAwMC8xNTE2MTAwMl8xLm1wNGRkAggPDxYCHwAFBTI2OTgyZGQCAg9kFg5mDw8WAh8ABQEyZGQCAQ8PFgIfAAUSMjAxNS85LzE1IDE4OjIwOjAwZGQCAg8PFgIfAAWJAuesrDIg5qyhMeiKgijnrKwyIOiusikgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZAIDDw8WAh8ABRIyMDE1LzkvMTUgMjM6MDA6MDBkZAIEDw8WAh8ABf8BLndtdiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGQCBw8PFgIfAAUba3hsLzEzMTQxMDAwLzE1MTYxMDAyXzIubXA0ZGQCCA8PFgIfAAUFMjcwMjZkZAIDD2QWDmYPDxYCHwAFATNkZAIBDw8WAh8ABRIyMDE1LzkvMjIgMTg6MjA6MDBkZAICDw8WAh8ABYkC56ysMyDmrKEx6IqCKOesrDMg6K6yKSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRkAgMPDxYCHwAFEjIwMTUvOS8yMiAyMjo1MTowMGRkAgQPDxYCHwAF%2FwEud212ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZAIHDw8WAh8ABRtreGwvMTMxNDEwMDAvMTUxNjEwMDJfMy5tcDRkZAIIDw8WAh8ABQUyNzA3MWRkAgQPZBYOZg8PFgIfAAUBNGRkAgEPDxYCHwAFEjIwMTUvOS8yOSAxODoyMDowMGRkAgIPDxYCHwAFiQLnrKw0IOasoTHoioIo56ysNCDorrIpICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGQCAw8PFgIfAAUSMjAxNS85LzI5IDIyOjAwOjAwZGQCBA8PFgIfAAX%2FAS53bXYgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRkAgcPDxYCHwAFG2t4bC8xMzE0MTAwMC8xNTE2MTAwMl80Lm1wNGRkAggPDxYCHwAFBTI3MTA0ZGQCBQ9kFg5mDw8WAh8ABQE1ZGQCAQ8PFgIfAAUTMjAxNS8xMC8xMyAxODoyMDowMGRkAgIPDxYCHwAFiQLnrKw2IOasoTHoioIo56ysNSDorrIpICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGQCAw8PFgIfAAUTMjAxNS8xMC8xNCAxMDowNzowMGRkAgQPDxYCHwAF%2FwEud212ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZAIHDw8WAh8ABRtreGwvMTMxNDEwMDAvMTUxNjEwMDJfNS5tcDRkZAIIDw8WAh8ABQUyNzE1MWRkAgYPZBYOZg8PFgIfAAUBNmRkAgEPDxYCHwAFEzIwMTUvMTAvMjAgMTg6MjA6MDBkZAICDw8WAh8ABYkC56ysNyDmrKEx6IqCKOesrDYg6K6yKSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRkAgMPDxYCHwAFEzIwMTUvMTAvMjAgMjI6NTQ6MDBkZAIEDw8WAh8ABf8BLndtdiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGQCBw8PFgIfAAUba3hsLzEzMTQxMDAwLzE1MTYxMDAyXzYubXA0ZGQCCA8PFgIfAAUFMjcxOThkZAIFDw8WAh8ABQEwZGQCBg8PFgIfAAWOAeW9k%2BWJjeWtpuacnzoyMDE1LTIwMTYuMSgyMDE1LTA5LTA36IezMjAxNi0wMS0xNynmnKzlkajkuLrnrKw3ICAg5ZGoICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfOePreS4u%2BS7uzrpq5jmhacoNjQ0ODAwMjItMTEwNSlkZGTpD1G8cmVMc%2BwpDYUD1hEll5QCgR%2FZneI78vpW8MGraw%3D%3D&_ctl0%3AMainContent%3Am_cbxXueqi=' + xueqi + '&_ctl0%3AMainContent%3AdplKc=' + dplKc + '&_ctl0%3Ahid='
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    cookie = getlogincookie(user, password)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url, postdata)
    print '打卡完毕'


def GetDownloadUrls(Lessiondate, LessionMark):
    xueqi = urllib.quote_plus(Lessiondate)
    dplKc = urllib.quote_plus(LessionMark)
    postdata = '__EVENTTARGET=&__EVENTARGUMENT=&__LASTFOCUS=&__VIEWSTATE=%2FwEPDwUKMTkyNDkzMjQ0NQ9kFgJmD2QWBAIDDw8WAh4EVGV4dAUURlkxNDIyMDA2Myzkuo7popzlt51kZAIFD2QWBgIBD2QWBgICDxBkDxYBZhYBEAULMjAxNS0yMDE2LjEFCzIwMTUtMjAxNi4xZ2RkAgYPEGQQFQQT5b6Q5oWn5aifLee7j%2Ba1juWtpivmnLHmuIXmnqst5oCd5oOz6YGT5b635L%2Bu5YW75LiO5rOV5b6L5Z%2B656GAFOeOi%2BW5sy3lpKflraboi7Hor60yHOi1teS%2FiuWSjC3kurrlipvotYTmupDnrqHnkIYVBBAxNTE2MTAzOSAgfDI5NjgwEDE1MTYxMDE0ICB8Mjk2ODcQMTUxNjEwMDIgIHwyOTY3ORAxNTE2MTAzNSAgfDI5NjcwFCsDBGdnZ2dkZAIKDzwrAAsAZAIFDw8WAh8ABQEwZGQCBg8PFgIfAAWOAeW9k%2BWJjeWtpuacnzoyMDE1LTIwMTYuMSgyMDE1LTA5LTA36IezMjAxNi0wMS0xNynmnKzlkajkuLrnrKwxMyAg5ZGoICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfOePreS4u%2BS7uzrpq5jmhacoNjQ0ODAwMjItMTEwNSlkZGSlzRtROgp16LU1R6%2FtV0u08rLywtXF7LkYnohnoz%2F4VQ%3D%3D&_ctl0%3AMainContent%3Am_cbxXueqi=' + xueqi + '&_ctl0%3AMainContent%3AdplKc=' + dplKc + '&_ctl0%3AMainContent%3AButton4=%E6%98%BE%E7%A4%BA&_ctl0%3Ahid='
    url = 'http://www.sjtuce.net/xxpt/jrJxpjVideoFtp.aspx'
    cookie = getlogincookie(user, password)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    urllib2.install_opener(opener)
    req = urllib2.urlopen(url, postdata)

    contents = req.read()
    soup = BeautifulSoup(contents, 'lxml')
    tmp = soup.find_all(name='a', text='点击下载')
    for a in tmp:
        Eventtarget = a.attrs.get('href').split('\'')[1]
        Click(Eventtarget, Lessiondate, LessionMark)
    print LessionMark + ' 任务完成'
