import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup



sjtuentryurl = 'http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx'
sjtunewurl = 'http://www.sjtuce.net/xxpt/jrJxpjMainNew.aspx'
reqcookielist = []
user = 'FY14220063'
password = 'a19910912'


def url_transfer(str):
    str = urllib.quote_plus(str)
    return str


def get_viewstate(soup):

    if soup:
        view_input = soup.find(id="__VIEWSTATE")
        if view_input:
            return (view_input['value'])
    print "The function %s args soup is empty" % 'get_ViewState'


def get_eventvalidation(soup):

    if soup:
        event_input = soup.find(id="__EVENTVALIDATION")
        if event_input:
            return event_input['value']
    print "The function %s args soup is empty" % 'get_EventValidation'


def get_reqcookie(url):

    url = url
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)

    response = opener.open(url)
    contents = response.read()
    soup = BeautifulSoup(contents, 'lxml')
    viewstatestr = get_viewstate(soup)
    for item in cookie:
        tmpstr = item.name + '=' + item.value
        reqcookielist.append(tmpstr)
    reqcookielist.append(viewstatestr)
    return reqcookielist


def get_logincookie(user, password):
    postdirc = {}
    reqcookielist = get_reqcookie(sjtuentryurl)
    cookiestr = "".join(reqcookielist[0])
    user = user
    password = password
    button2 = '.%E7%99%BB++%E5%BD%95.'
    student_cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookiestr)
    opener = urllib2.build_opener(handler)
    viewstate = reqcookielist[-1]
    data = ('__VIEWSTATE=%s&user=%s&Password=%s&Button2=%s\
    ') % (viewstate, user, password, button2)
    login_request = urllib2.Request(sjtuentryurl, data)
    req = opener.open(login_request, data)
    contents = req.read()
    soup = BeautifulSoup(contents, 'lxml')
    viewstatestr = get_viewstate(soup)
    postdirc['cookie'] = student_cookie
    postdirc['viewstate'] = viewstatestr
    return postdirc


aa = get_logincookie(user, password)
print aa
