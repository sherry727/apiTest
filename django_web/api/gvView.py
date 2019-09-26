# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django_web.models import globalVariable,sqlManager
from django.utils import timezone
import json
from django.contrib.auth.decorators import login_required



def globalVarables(request):
    return render(request, 'main/gv.html')

def gvList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    user = request.GET.get('user')
    q1 = Q()
    q1.connector = 'AND'
    if len(key) > 0:
        q1.children.append(('name__contains', key))
    q1.children.append(('user', user))
    p = globalVariable.objects.filter(q1).order_by('-CreateTime')
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['name'] = a.name
        dic['createTime'] = a.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['value'] = a.value
        dic['path'] = a.path
        dic['user'] = a.user
        dic['gType'] = a.gType
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)

def gvAdd(request):
    return render(request, 'main/gv-add.html')

def gvAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        print(u)
        name = u.get('name')
        user = u.get('user')
        value =u.get('value')
        try:
            globalVariable.objects.get(name=name, user=user)
            globalVariable.objects.filter(name=name).update(name=name, value=value)
        except:
            p = globalVariable.objects.create(name=name, user=user, value=value, CreateTime=timezone.now())
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

def gvDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        id = u.get('id')
        globalVariable.objects.filter(id=id).delete()
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

def selectDBForSql(request,sid):
    s =sqlManager.objects.filter(sqltype=sid)
    dict=[]
    for i in s:
        dic = {}
        dic['dbName'] = i.name
        dic['dbId'] = i.id
        dict.append(dic)
    return JsonResponse(dict, safe=False)