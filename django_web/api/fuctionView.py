# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django_web.models import fuctionLib
from django.utils import timezone
import json,time
from django.contrib.auth.decorators import login_required
import hashlib


def fuction_index(request):
    return render(request, 'main/fuction-index.html')


def fuctionList(request):
    loginName = request.session.get('Username', '')
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    ftype = request.GET.get('ftype')
    q1 = Q()
    q1.connector = 'AND'
    if ftype:
        q1.children.append(('ftype', ftype))
    if len(key) > 0:
        q1.children.append(('name__contains', key))
    p = fuctionLib.objects.filter(q1)
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['ftype'] = a.ftype
        dic['name'] = a.name
        dic['desc'] = a.desc
        dic['method'] = a.method
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)

def qianming(fu_id,jdata,appKey,app_secret):
    if appKey==None or app_secret==None:
        re='appKey或app_secret不能为空！'
    else:
        if fu_id == 1:
            re1= ydj_test_qianming(jdata, appKey, app_secret)
            # re = dict(jdata.items()+re1.items())
            re = dict(re1, **jdata)
        else:
            re='签名返回异常'
    return re

def ydj_test_qianming(jdata,appKey,app_secret):
    jdata['timestamp'] = int(time.time())
    sortedParam = sorted(jdata.items(), key=lambda d: d[0])
    paramStr = ''
    for param in sortedParam:
        paramStr = paramStr + str(param[0]) + "=" + str(param[1])+"&"
    rparamStr ="appKey=" +appKey+ "&" + paramStr
    rparamStr = rparamStr[:-1]+app_secret
    sign = hashlib.md5(rparamStr.encode("utf-8")).hexdigest()
    result ={
        'appKey': appKey,
        'timestamp': jdata['timestamp'],
        'sign': sign
    }
    return result


