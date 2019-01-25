# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project,Case,AutoApiCase,autoApiHead,autoAPIParameter,task,taskCase,AutoTaskRunTime
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json,re
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django_web.api import Public
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED,EVENT_JOB_ERROR,EVENT_SCHEDULER_PAUSED,EVENT_SCHEDULER_SHUTDOWN
import apscheduler.events





@login_required
def apiCase_index(request):
    return render(request, 'main/case.html')

def getCaseList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    projectid = request.GET.get('projectid')
    projects = Project.objects.filter(status=1).values('id')
    q1 = Q()
    q1.connector = 'AND'
    if projectid:
        q1.children.append(('project_id', projectid))
    if len(key)>0:
        q1.children.append(('name__contains', key))
    p = Case.objects.filter(q1).order_by('-CreateTime')
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['project_id'] = a.project_id
        r = Project.objects.get(id=a.project_id)
        dic['projectName'] = r.name
        dic['name'] = a.name
        dic['createTime'] = a.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['desc'] = a.desc
        dic['user'] = a.user
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    # print resultdict
    return JsonResponse(resultdict, safe=False)

def caseAdd(request):
    return render(request, 'main/case-add.html')

def caseAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        projectid = u.get('projectid')
        name = u.get('name')
        user = u.get('user')
        desc =u.get('desc')
        p = Case.objects.create(name=name, user=user,  desc=desc, project_id=projectid, CreateTime=timezone.now())
        p.save()
        resultdict = {
            'code': 0,
            'msg': 'success',
            'data': {'name': name}
        }
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

def caseEdit(request,eid):
    case = Case.objects.get(id=eid)
    name = case.name
    user = case.user
    desc = case.desc
    projectId = case.project_id
    r = Project.objects.get(id=projectId)
    data={
        'caseId': eid,
        'name': name,
        'desc': desc,
        'projectId': projectId,
        'user': user,
        'projectName': r.name
    }
    return render(request,'main/case-edit.html', data)

def caseEditPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        name = u.get('name')
        user = u.get('user')
        projectid = u.get('projectid')
        desc = u.get('desc')
        caseId = u.get('caseId')
        Case.objects.filter(id=caseId).update(name=name, desc=desc,project_id= projectid,LastUpdateTime=timezone.now())
        resultdict = {
            'code': 0,
            'msg': '编辑成功',
            'data': {
                'caseId': caseId
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

def caseDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        id=u.get('id')
        Case.objects.filter(id=id).delete()
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

def caseTask(request, caseData):
    c = caseData.encode('utf-8')
    caseData = json.loads(c)
    resultdict = {
        'code': 0,
        'msg': '成功',
        'data': caseData
    }
    return render(request, 'main/addCaseTask.html', resultdict)
    # return JsonResponse(resultdict, safe=False)





