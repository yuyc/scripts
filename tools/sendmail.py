#!/usr/bin/python 
#coding:utf-8 

import smtplib 
from email.mime.text import MIMEText 
import sys 
mail_host = 'smtp.exmail.qq.com' 
mail_user = 'user' 
mail_login_user = 'user@test.net'
mail_pass = 'pass' 
mail_postfix = 'test.net' 

def send_mail(to_list,subject,content): 
    me = mail_user+"<"+mail_user+"@"+mail_postfix+">" 
    msg = MIMEText(content) 
    msg['Subject'] = subject 
    msg['From'] = me 
    msg['to'] = to_list 
    try: 
        s = smtplib.SMTP() 
        s.connect(mail_host) 
        s.login(mail_login_user,mail_pass) 
        s.sendmail(me,to_list,msg.as_string()) 
        s.close() 
        return True
    except Exception,e: 
        print str(e)
        return False 

if __name__ == "__main__": 
    send_mail(sys.argv[1],sys.argv[2],sys.argv[3])
