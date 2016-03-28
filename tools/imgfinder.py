#coding:utf-8
import web
import os
import sys
from subprocess import *
reload(sys)
sys.setdefaultencoding('utf-8')

urls = (
    '/', 'index',
    '/find', 'find'

)

class index:


    def GET(self):

        return """
    <html>
            <head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head>
        <body>
            <form action="/find" method="post">
                <p>要查找的文件名: <input type="text" name="u" /></p>
                <input type="radio" name="type" value="str" /> 以路径形式显示
                <input type="radio" name="type" value="img" /> 以图片形式显示<br>
                <input type="submit" value="查找" />
            </form>
        </body>
    </html>
    """
def findpstr(var):
    list = []
    head = '<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head>'
    for x in var:
        x = x.replace('/data','\\\\172.16.19.2')
        x = x.replace('/','\\')
        list.append(x)
    tmp = "<br>".join(list)
        result = head + tmp
    return result
def findp(var):

    list = []
        for x in var:
            x = x.replace('/data', 'http://172.16.19.2')
            list.append(x)
    return list
def resulttohtml(result):

    html_head = '<html><head><meta http-equiv="content-type" content="text/html;charset=utf-8"></head><body>'
    html_tail = '</body></html>'
    html_body_list = []
    for img in result:
        img = '<img src="%s" width="200" height="200" />' % img
        html_body_list.append(img)
    html_body_str = " ".join(html_body_list)
    resulthtml = html_head + html_body_str + html_tail
    return resulthtml
class find:
    def POST(self):
    i = web.input()
    filename = i['u'].split(" ")[0].strip()
    print filename
    try:
        if not i['type'] is None:
            if i['type'] == 'str':
                findcmd = 'find /data -iname *%s*' % (filename)
                    var = Popen(findcmd, shell=True, stdout=PIPE, stderr=PIPE).stdout.readlines()
                result = findpstr(var)
                return result
            findcmd = 'find /data -type f -iname *%s*' % (filename)
            var = Popen(findcmd, shell=True, stdout=PIPE, stderr=PIPE).stdout.readlines()
            result = findp(var)
            resulthtml = resulttohtml(result)   
            return resulthtml
    except:
        findcmd = 'find /data -iname *%s*' % (filename)
            var = Popen(findcmd, shell=True, stdout=PIPE, stderr=PIPE).stdout.readlines()
            result = findpstr(var)
            return result

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
