# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PTS.models import sceneManager
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db.models import Q


def report_index(request):
    return render(request, 'pts/Report_index.html')

def report_samplerLog(request):
    return render(request, 'pts/Report_samplerLog.html')

def overView(request):
    return render(request, 'pts/overView.html')



def samplerList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    q1 = Q()
    q1.connector = 'AND'
    if len(key) > 0:
        q1.children.append(('name__contains', key))
    p = sceneManager.objects.filter(q1).order_by('-CreateTime')
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['sceneType'] = a.sceneType
        dic['status'] = a.status
        dic['name'] = a.name
        dic['verbTime'] = a.verbTime
        dic['createTime'] = a.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['updateTime'] = a.updateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['user'] = a.user
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    # print resultdict
    return JsonResponse(resultdict, safe=False)

def logDetail(request):
    return render(request, 'pts/Report_logDetail.html')