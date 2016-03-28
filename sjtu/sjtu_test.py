#!/usr/bin/env python
#coding:utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import requests
import lxml

def get_viewstate(soup):
    if soup:      
        view_input = soup.find(id="__VIEWSTATE")
        if view_input:
            return (view_input['value'])     
    print "The function %s args soup is empty" % 'get_ViewState'

s = requests.session()
url = 'http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx'
user='FY14220044'
password='123456'
button2 = '.登  录.'
before_login_request = s.get('http://www.sjtuce.net/xxpt/jrJxpjLogin.aspx')
before_login_request_soup = BeautifulSoup(before_login_request.text,'lxml')
before_viewstate = get_viewstate(before_login_request_soup)
postdata = {'__VIEWSTATE':before_viewstate,
            'user':user,
            'Password':password,
            'Button2=':button2   
            }
login = s.post(url,data=postdata)
print dir(login)
print '='*30



