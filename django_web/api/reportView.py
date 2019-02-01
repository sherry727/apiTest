# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project,task,taskResult,taskCase,AutoApiCase,autoApiHead,autoAPIParameter,Case
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def resuLtList(request,taskId):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    sta = request.GET.get('status')
    w = taskResult.objects.filter(task_id=taskId).order_by('testTime').last()
    q1 = Q()
    q1.connector = 'AND'
    q1.children.append(('task_id', taskId))
    q1.children.append(('testTime', w.testTime))
    status=sta.encode('unicode-escape').decode('string_escape')
    if status=='1':
        q1.children.append(('httpStatus', '200'))
    elif status=='2':
        q1.children.append(('httpStatus', '404'))
    elif status=='3':
        q1.children.append(('httpStatus', '502'))
    p = taskResult.objects.filter(q1)
    t = task.objects.get(id=taskId)
    e =Env.objects.get(id=t.env_id)
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    for c in p:
        case = Case.objects.get(id=c.case_id)
        api = AutoApiCase.objects.get(id=c.autoApi_id)
        dic = {}
        dic['apiName'] = api.name
        dic['url'] = e.env_url+api.apiAddress
        dic['caseName'] = case.name
        dic['caseId'] = c.case_id
        project=Project.objects.get(id=case.project_id)
        dic['projectId'] = case.project_id
        dic['projectName'] = project.name
        dic['projectName'] = project.name
        dic['result'] = c.result
        dic['user'] = c.user
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)