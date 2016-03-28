#!/usr/bin/env python
#coding:utf-8
import os
import sys
import base64
import xml.etree.ElementTree as ET

tree = ET.parse(r'D:\pycharm\read.xml')
root = tree.getroot()

#find the item to list
item = root.find('Database').find('Sys_User').findall('Item')
UserDetail = root.find('Database').find('RTX_UserDetail').findall('Item')
dept = root.find('Database').find('RTX_Dept').findall('Item')
deptuser = root.find('Database').find('RTX_DeptUser').findall('Item')

#create a empty list to save the users' info
userlist = []
#create tmp list to save the users' tmp info
itemlist = []
userdelist = []
deptlist = []
deptuserlist = []



for itemlisttmp in item:
    itemlist.append(itemlisttmp.attrib)

for userdelisttmp in UserDetail:
    userdelist.append(userdelisttmp.attrib)
    
for deptlisttmp in dept:
    deptlist.append(deptlisttmp.attrib)
    
for deptuserlisttmp in deptuser:
    deptuserlist.append(deptuserlisttmp.attrib)
    
#����list��ȡ������洢��dic��������dic��key�����ֵ�ϲ������洢��userlist��  
for itemdic in itemlist:
    for userdedic in userdelist:
        if itemdic.get('ID') == userdedic.get('ID'):
            dictuser = dict(itemdic.items() + userdedic.items())
            userlist.append(dictuser)

temp = {}
for v in deptlist:
    #print v.get('DeptID')
    temp[v.get('DeptID')] = v   
 
def GetParentList(deptId):
#����һ�����б�
    deptList = []
    i = 20
    #�Ѳ���id��ֵ��tDeptId
    tDeptId = str(deptId)
    while i>0:
        i-=1
        #���ݲ���id��ȡ�����ŵ���Ϣ
        deptInfo = temp.get(tDeptId)
        if deptInfo is None:
            break
        deptList.append(deptInfo.get('DeptName'))
        tDeptId = deptInfo.get('PDeptID')
        if tDeptId is None:
            break
        if int(tDeptId)<=0:
            break
    deptdict = {'DeptID':deptId,'dn':deptList}
    return deptdict

#temp4 = [v for v in deptlist if int(v.get('DeptID'))==0]
#����deptlist��ȡ��PDeptID����ֵ��Ȼ����Ϊ����
deptParentIdList = set([int(v.get('PDeptID')) for v in deptlist])
#����deptilist��ȡDeptID������PDeptID��ֵ��Ȼ����Ϊ�б�
temp5 = [v for v in deptlist if int(v.get('DeptID')) not in deptParentIdList]


result = []
for v in temp.values():
    result.append(GetParentList(v.get('DeptID')))
    
#�û�����Ķ�Ӧ��ϵͬdn�ֵ�ϲ�
group = []
for deptuser in deptuserlist:
    for v in result:
        if deptuser.get('DeptID') == v.get('DeptID'):
           group.append(dict(deptuser,**v)) 

userslist = []
def lineou(list):
        return ',ou='.join(list)
for user in userlist:
    for deptuser in group:
        if user.get('ID') == deptuser.get('UserID'):
            UserName = user.get('UserName')
            dn = 'cn='+UserName+','+'ou='+lineou(deptuser.get('dn'))+',dc=boqii-inc,dc=com'
            users=dict(user.items())
            users['dn'] = dn
            userslist.append(users)  
            
            


for i in userslist:
    samid = i.get('UserName')
    ou = i.get('dn')
    upn = samid+"@boqii-inc.com"
    pwd = "boqii123!"
    display = i.get('Name')
    email = i.get('Email')
    mobile = i.get('Mobile')
    print 'dsadd user','\"'+ou+'\"','-samid',samid,'-upn',upn,'-display',display,'-mobile',mobile,'-pwd',pwd       

