# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project,task,taskResult,taskCase,AutoApiCase,autoApiHead,autoAPIParameter,Case,AutoTaskRunTime
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def resuLtList(request,autoRuntimeid):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    sta = request.GET.get('status')
    taskId = AutoTaskRunTime.objects.get(id=autoRuntimeid).task_id
    q1 = Q()
    q1.connector = 'AND'
    q1.children.append(('task_id', taskId))
    q1.children.append(('autoRunTime_id', autoRuntimeid))
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
        dic['result_id'] = c.id
        dic['apiId'] = api.id
        dic['url'] = e.env_url+api.apiAddress
        dic['caseName'] = case.name
        dic['caseId'] = c.case_id
        project=Project.objects.get(id=case.project_id)
        dic['projectId'] = case.project_id
        dic['projectName'] = project.name
        dic['projectName'] = project.name
        dic['result'] = c.result
        dic['user'] = c.user
        dic['taskId'] = taskId
        dic['autoRuntimeid'] = autoRuntimeid
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)

def rDetail(request,apiData):
    c = apiData.encode('utf-8')
    apiData = json.loads(c)
    # u = AutoApiCase.objects.get(id=apiData.get('apiId'))  # 接口表
    h = autoApiHead.objects.filter(autoApi_id=apiData.get('apiId'))  # 请求头
    m = autoAPIParameter.objects.filter(autoApi_id=apiData.get('apiId'))  # 请求参数
    t= task.objects.get(id=apiData.get('taskId'))#任务表
    s = taskResult.objects.get(id=apiData.get('result_id'))
    params = []
    for i in m:
        dic = {}
        dic['param_name'] = i.name
        dic['param_key'] = i.value
        params.append(dic)
    headers = []
    for i in h:
        dic = {}
        dic['head_name'] = i.name
        dic['head_key'] = i.value
        headers.append(dic)
    data = {
        'caseName': apiData.get('caseName'),
        'caseId': apiData.get('caseId'),
        'taskId': apiData.get('taskId'),
        'taskName': t.name,
        'apiId': apiData.get('apiId'),
        'projectId': apiData.get('projectId'),
        'apiName': apiData.get('apiName'),
        'projectName': apiData.get('projectName'),
        'autoRuntimeid': apiData.get('autoRuntimeid'),
        'user': apiData.get('user'),
        'url': apiData.get('url'),
        'headers': headers,
        'params': params,
        'responseData': s.responseData,
        'result': apiData.get('result').encode('utf-8')
    }
    # print type(apiData.get('result').encode('utf-8'))
    return render(request, 'main/report-Detail.html', data)