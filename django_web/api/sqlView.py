# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django_web.models import Env,Project,Case,AutoApiCase,autoApiHead,autoAPIParameter,task,taskCase,AutoTaskRunTime
from django_web.models import sqlManager
from django.shortcuts import render
import json,re
from django.utils import timezone
import  pymysql
import redis
from django.contrib.auth.decorators import login_required
import logging
import time

def sql_index(request):
    return render(request, 'main/DB_index.html')

def DBList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    q1 = Q()
    q1.connector = 'AND'
    if len(key) > 0:
        q1.children.append(('name__contains', key))
    p = sqlManager.objects.filter(q1).order_by('-CreateTime')
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['name'] = a.name
        dic['createTime'] = a.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['port'] = a.port
        dic['sqlType'] = a.sqltype
        dic['db'] = a.db
        dic['username'] = a.username
        dic['password'] = a.password
        dic['host'] = a.host
        dic['user'] = a.user
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)

def dbAdd(request):
    return render(request, 'main/DB-add.html')

def DBAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        sqlType = u.get('sqlType')
        name = u.get('name')
        user = u.get('user')
        desc =u.get('desc')
        username =u.get('username')
        password =u.get('password')
        hostname =u.get('hostname')
        port =u.get('port')
        DBname =u.get('DBname')
        p = sqlManager.objects.create(name=name, user=user,  desc=desc, sqltype=sqlType, CreateTime=timezone.now(),
                                      username=username, password=password, host=hostname, port=port, db=DBname)
        p.save()
        resultdict = {
            'code': 0,
            'msg': 'success',
            'data': {'id': p.id}
        }
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

def DBEdit(request,DBid):
    d = sqlManager.objects.get(id=DBid)
    data={
        'DBid': DBid,
        'sqlType': d.sqltype,
        'host': d.host,
        'port': d.port,
        'username': d.username,
        'password': d.password,
        'name': d.name,
        'desc': d.desc,
        'db': d.db
    }
    return render(request, 'main/DB-edit.html',data)

def DBEditPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        name = u.get('name')
        user = u.get('user')
        sqlType = u.get('sqlType')
        desc = u.get('desc')
        DBid = u.get('DBid')
        host = u.get('hostname')
        username = u.get('username')
        password = u.get('password')
        port = u.get('port')
        db = u.get('DBname')
        sqlManager.objects.filter(id=DBid).update(name=name, desc=desc, sqltype=sqlType, host=host, username=username,
                                                  password=password, port=port, db=db)
        resultdict = {
            'code': 0,
            'msg': '编辑成功',
            'data': {
                'caseId': DBid
            }
        }
        return JsonResponse(resultdict, safe=False)

    else:
        resultdict = {
            'code': 1,
            'msg': '编辑失败',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)


def DBDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        id=u.get('id')
        sqlManager.objects.filter(id=id).delete()
        resultdict = {
            'code': 0,
            'msg': 'success',
            'data': {'id': id}
        }
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': '删除失败',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)


def testDB(request):
    if request.method == "POST":
        u = json.loads(request.body)
        name = u.get('name')
        user = u.get('user')
        sqlType = u.get('sqlType')
        desc = u.get('desc')
        DBid = u.get('DBid')
        host = u.get('hostname')
        username = u.get('username')
        password = u.get('password')
        port = u.get('port')
        db = u.get('DBname')
        resultdict={}
        if int(sqlType) == 1:
            try:
                d = pymysql.connect(host=host, user=username, passwd=password, db=db, port=int(port), charset='utf8')
                d.close()
                resultdict = {
                    'code': 0,
                    'msg': 'success',
                    'data': {'id': DBid}
                }
            except pymysql.Error as e:
                try:
                    sqlError = "Error %d:%s" % (e.args[0], e.args[1])
                except IndexError:
                    print("MySQL Error:%s" % str(e))
                resultdict = {
                    'code': 2,
                    'msg': '连接失败',
                    'data': {'id': DBid}
                }
        elif int(sqlType) == 2:
            try:
                r = redis.Redis(host=host, port=int(port), password=password)
                # r = redis.Redis(host='192.168.1.20', port=6379, password='123456')
                r.keys(pattern='*')
                resultdict = {
                    'code': 0,
                    'msg': 'success',
                    'data': {'id': DBid}
                }
            except:
                print('连接异常')
                resultdict = {
                    'code': 2,
                    'msg': '连接失败',
                    'data': {'id': DBid}
                }
        else:
            resultdict = {
                'code': 2,
                'msg': '连接失败',
                'data': {'id': DBid}
            }

    else:
        resultdict = {
            'code': 1,
            'msg': '请求失败',
            'data': {}
        }
    return JsonResponse(resultdict, safe=False)
