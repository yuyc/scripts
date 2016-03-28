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
#������ʱlist�������洢������Ϣ
deptlist = []
deptidlist = []
#������ʱlist�������洢�����û���Ϣ
deptuserlist = []
firstoulist = []
oudelist = []
oudeljlist = []
userzjlist = []


#ͨ�������б�ȡ��etree��������ԣ����洢Ϊlist
for itemlisttmp in item:
    itemlist.append(itemlisttmp.attrib)

for userdelisttmp in UserDetail:
    userdelist.append(userdelisttmp.attrib)
    
#ͨ�������б�ȡ��etree��������ԣ��洢��list����������ou
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

#�Ȱ�һ��ouд��list
for dept in deptlist:
    if dept.get('PDeptID') == '0':
        deptname = dept.get('DeptName')
        deptid = dept.get('DeptID')
        base64dept = 'ou='+deptname+',dc=boqii-inc,dc=com'
        firstoulist.append({'DeptID':deptid,'ou':deptname,'dn':base64dept})

#����һ���ֵ䣬���Ѳ��ŵ�id��Ϊkey��Ȼ������Ϣ��Ϊvalues
temp = {}
for v in deptlist:
    #print v.get('DeptID')
    temp[v.get('DeptID')] = v   
 
def GetParentList(deptId):
#����һ�����б�
    deptList = []
    i = 20
    #�Ѳ���id��ֵ��tDeptId
    tDeptId = deptId
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
    return deptList

#temp4 = [v for v in deptlist if int(v.get('DeptID'))==0]
#����deptlist��ȡ��PDeptID����ֵ��Ȼ����Ϊ����
deptParentIdList = set([int(v.get('PDeptID')) for v in deptlist])
#����deptilist��ȡDeptID������PDeptID��ֵ��Ȼ����Ϊ�б�
temp5 = [v for v in deptlist if int(v.get('DeptID')) not in deptParentIdList]
result = []
for v in temp5:
    result.append(GetParentList(v.get('DeptID')))
   
  

#result1 = ['dsadd ou %s,dc=boqii-inc,dc=com'%(','.join(['ou=%s'%(t,) for t in v]),) for v in result]
for v in result:
    v.reverse()
    t = []
    for a in v:
        t.append(a)
        t.reverse()
        print 'dsadd ou %s,dc=boqii-inc,dc=com'%(','.join(['ou=%s'%(x) for x in t]))
        t.reverse()



      
