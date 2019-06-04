# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from PTS.models import scriptManager
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django_web.api import Public
import json,os
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings



def jm_index(request):
    return render(request, 'pts/scene_index.html')

def scriptList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    q1 = Q()
    q1.connector = 'AND'
    if len(key) > 0:
        q1.children.append(('name__contains', key))
    p = scriptManager.objects.filter(q1).order_by('-CreateTime')
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['sType'] = a.sType
        dic['path'] = a.path
        dic['fname'] = a.fname
        dic['createTime'] = a.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['user'] = a.user
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    # print resultdict
    return JsonResponse(resultdict, safe=False)


def scriptAdd(request):
    return render(request, 'pts/script-add.html')

def uploadScript(request):
    loginName = request.session.get('Username', '')
    File = request.FILES.get("file", None)
    resultdict = Public.uploadFileWithPath(File, settings.SCRIPT_PATH)
    s = scriptManager.objects.create(sType=0, user=loginName, fname=resultdict.get('name'), path=resultdict.get('path'),
                                     CreateTime=timezone.now())
    s.save()
    print resultdict
    return JsonResponse(resultdict, safe=False)

def scriptAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        loginName = request.session.get('Username', '')
        print u
        filename = u.get('filename')
        desc = u.get('desc')
        fpath = u.get('fpath')
        fname = u.get('fname')
        p= scriptManager.objects.create(sType=0, user=loginName, fname=fname, desc=desc, path=fpath,
                                       CreateTime=timezone.now())
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