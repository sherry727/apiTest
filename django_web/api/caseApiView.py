# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project,Case,AutoApiCase,autoApiHead,autoAPIParameter,ApiCase,ApiHead,APIParameter,TestResult
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.db.models import Q
from django_web.api import Public
import requests
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers

#用例下的接口列表
def getCaseApiList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    caseId = request.GET.get('caseId')
    case = Case.objects.get(id=caseId)
    projectid =case.project_id
    q1 = Q()
    q1.connector = 'AND'
    q1.children.append(('case_id', caseId))
    if len(key)>0:
        q1.children.append(('name__contains', key))
    p = AutoApiCase.objects.filter(q1).order_by('sort')
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    resultdict['total'] = total
    z=1
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['project_id'] = a.project_id
        r = Project.objects.get(id=a.project_id)
        dic['projectName'] = r.name
        dic['caseId'] = caseId
        dic['sort'] = a.sort
        dic['name'] = a.name
        dic['method'] = a.method
        dic['apiAddress'] = a.apiAddress
        dic['createTime'] = a.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['desc'] = a.desc
        dic['user'] = a.user
        dic['status'] = a.status
        dict.append(dic)
        z = z+1
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


def caseApi(request, id):
    user = Case.objects.get(id=id).user
    data = {
        'id': id,
        'user': user
    }
    return render(request, 'main/caseApi.html', data)

def caseApiAdd(request,caseId):
    data = {
        'caseId': caseId,
    }
    return render(request, 'main/caseApi-add.html', data)

#新增接口
def caseApiAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        projectid = u.get('projectid')
        caseId = u.get('caseId')
        name = u.get('name')
        user = u.get('user')
        method = u.get('method')
        requestParameterType = u.get('requestParameterType')
        url = u.get('url')
        desc = u.get('desc')
        httptype = u.get('httptype')
        headers = u.get('headers')
        params = u.get('params')
        p = AutoApiCase.objects.create(project_id=projectid, name=name, user=user, method=method,
                                       requestParameterType=requestParameterType,
                                       httpType=httptype, desc=desc, apiAddress=url, case_id=caseId, CreateTime=timezone.now(),status=1)
        p.save()
        ap = AutoApiCase.objects.last()
        headersList = []
        for h in headers:
            nm = h.get('head_name')
            key = h.get('head_key')
            headersList.append(autoApiHead(name=nm, api_id=ap.id, value=key))
        autoApiHead.objects.bulk_create(headersList)
        paramsList = []
        for h in params:
            nm = h.get('param_name')
            key = h.get('param_key')
            paramType = h.get('paramType')
            paramsList.append(autoAPIParameter(name=nm, api_id=ap.id, value=key, paramType=paramType))
        autoAPIParameter.objects.bulk_create(paramsList)
        resultdict = {
            'code': 0,
            'msg': 'success',
            'data': {'id': ap.id}
        }
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

def caseApiAddOld(request,caseId):
    data = {
        'caseId': caseId,
    }
    return render(request, 'main/caseApi-addOld.html', data)

#添加已有接口页面的list
def apiListForProject(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    projectid = request.GET.get('projectId')
    projects = Project.objects.filter(status=1).values('id')
    q1 = Q()
    q1.connector = 'AND'
    if len(projectid) > 0:
        q1.children.append(('project_id', projectid))
    p = ApiCase.objects.filter(q1).order_by('-CreateTime')
    resultdict = {}
    total = p.count()
    p = p[i:j]
    dict = []
    resultdict['total'] = total
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['project_id'] = a.project_id
        r = Project.objects.get(id=a.project_id)
        dic['projectName'] = r.name
        dic['name'] = a.name
        dic['method'] = a.method
        dic['apiAddress'] = a.apiAddress
        dic['createTime'] = a.CreateTime.strftime("%Y-%m-%d %H:%M:%S")
        dic['desc'] = a.desc
        dic['user'] = a.user
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


def caseApiAddOldPost(request,caseId):
    if request.method == "POST":
        o = json.loads(request.body)
        for u in o:
            apiId = u.get('id')
            projectid = u.get('project_id')
            name = u.get('name')
            user = u.get('user')
            method = u.get('method')
            url = u.get('apiAddress')
            requestParameterType = 1
            desc = u.get('desc')
            headers = ApiHead.objects.filter(api_id=apiId)
            params = APIParameter.objects.filter(api_id=apiId)
            p = AutoApiCase.objects.create(project_id=projectid, name=name, user=user, method=method,
                                           desc=desc, apiAddress=url, case_id=caseId, requestParameterType=requestParameterType,
                                           CreateTime=timezone.now())
            p.save()
            headersList = []
            for h in headers:
                nm = h.name
                key = h.value
                headersList.append(autoApiHead(name=nm, autoApi_id=p.id, value=key))
            autoApiHead.objects.bulk_create(headersList)
            paramsList = []
            for h in params:
                nm = h.name
                key = h.value
                paramType = h.paramType
                paramsList.append(autoAPIParameter(name=nm, autoApi_id=p.id, value=key, paramType=paramType))
            autoAPIParameter.objects.bulk_create(paramsList)
        resultdict = {
            'code': 0,
            'msg': 'success',
            'data': {'caseId': caseId}
        }
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

def caseApiEdit(request,eid):
    u = AutoApiCase.objects.get(id=eid)  # 接口表
    h = autoApiHead.objects.filter(autoApi_id=eid)  # 请求头
    m = autoAPIParameter.objects.filter(autoApi_id=eid)  # 请求参数
    p = Project.objects.get(id=u.project_id)  # 项目表
    params = []
    for i in m:
        dic = {}
        dic['param_name'] = i.name
        dic['param_key'] = i.value
        dic['paramType'] = i.paramType
        params.append(dic)
    headers = []
    for i in h:
        dic = {}
        dic['head_name'] = i.name
        dic['head_key'] = i.value
        headers.append(dic)
    data = {
        'id': eid,
        'name': u.name,
        'url': u.apiAddress,
        'requestParameterType': u.requestParameterType,
        'httptype': u.httpType,
        'method': u.method,
        'projectName': p.name,
        'projectid': u.project_id,
        'user': u.user,
        'params': params,
        'headers': headers,
        'desc': u.desc,
        'sort': u.sort
    }
    return render(request, 'main/caseApi-edit.html', data)


def caseApiDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        # u = request.body
        id=u.get('id')
        AutoApiCase.objects.filter(id=id).delete()
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

def caseApiEditPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        # print u
        projectname = u.get('projectid')
        p = Project.objects.get(name=projectname)
        projectid=p.id
        id = u.get('id')
        name = u.get('name')
        user = u.get('user')
        method = u.get('method')
        requestParameterType = u.get('requestParameterType')
        url = u.get('url')
        desc = u.get('desc')
        httptype = u.get('httptype')
        headers = u.get('headers')
        params = u.get('params')
        asserts = u.get('asserts')
        galobalValues = u.get('galobalValues')
        sort = u.get('sort')
        AutoApiCase.objects.filter(id=id).update(project_id=projectid, name=name, user=user, method=method,
                                                 requestParameterType=requestParameterType,
                                                 httpType=httptype, desc=desc, apiAddress=url, LastUpdateTime=timezone.now())
        h= autoApiHead.objects.filter(autoApi_id=id)
        if h:
            h.delete()
        p = autoAPIParameter.objects.filter(autoApi_id=id)
        if p:
            p.delete()
        headersList = []
        for h in headers:
            nm = h.get('head_name')
            key = h.get('head_key')
            headersList.append(autoApiHead(name=nm, autoApi_id=id, value=key))
        autoApiHead.objects.bulk_create(headersList)
        paramsList = []
        for h in params:
            nm = h.get('param_name')
            key = h.get('param_key')
            type = h.get('paramType')
            paramsList.append(autoAPIParameter(name=nm, autoApi_id=id, value=key, paramType=type))
        autoAPIParameter.objects.bulk_create(paramsList)
        resultdict = {
            'code': 0,
            'msg': 'success',
            'data': {'id': id}
        }
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

def caseApiMultRun(request,eid):
    if request.method == "POST":
        u = json.loads(request.body)
        env = Env.objects.get(id=eid)
        # print u
        if env.evn_port:
            url = env.env_url+':'+env.evn_port
        else:
            url = env.env_url
        sorts=[]
        for i in u:
            dict = {}
            sort= i.get('LAY_TABLE_INDEX')
            id = i.get('id')
            dict['id'] = id
            dict['sort'] = sort
            sorts.append(dict)
            AutoApiCase.objects.filter(id=id).update(sort=sort)
        startTime = timezone.now()
        for s in sorts:
            caseApi = AutoApiCase.objects.get(id=s.get('id'))
            he =autoApiHead.objects.filter(autoApi_id=s.get('id'))
            pa =autoAPIParameter.objects.filter(autoApi_id=s.get('id'))
            headers = {}
            params = {}
            for p in he:
                name = p.name
                value = p.value
                headers[name] = value
            for p in pa:
                name = p.name
                value = p.value
                params[name] = value
            url1 =url+caseApi.apiAddress
            ur = url1.encode('unicode-escape').decode('string_escape')
            method = caseApi.method
            sort = s.get('sort')
            try:
                r = Public.execute(url=ur, params=params, method=method, heads=headers)
                print r.text
                if r.status_code == 200:
                    AutoApiCase.objects.filter(id=s.get('id')).update(status='成功')
                    # TestResult.objects.create()
                else:
                    AutoApiCase.objects.filter(id=s.get('id')).update(status='失败')
            except:
                AutoApiCase.objects.filter(id=s.get('id')).update(status='异常')
        endTime = timezone.now()
        resultdict = {
            'code': 0,
            'msg': '运行成功',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

def selectApiEnvName(request):
    p = Env.objects.filter()
    dict = []
    for a in p:
        dic = {}
        dic['ename'] = a.env_name
        dic['eid'] = a.id
        dict.append(dic)
    return JsonResponse(dict, safe=False)

def autoApiSimpleRun(request):
    u = json.loads(request.body)
    print u
    api_id = u.get('id')
    api = AutoApiCase.objects.get(id=api_id)
    env_id = u.get('envid')
    method = u.get('method')
    pa = autoAPIParameter.objects.filter(autoApi_id=api_id).values('name', 'value')
    params = {}
    for p in pa:
        name = p.get('name')
        value = p.get('value')
        params[name] = value
    he = autoApiHead.objects.filter(autoApi_id=api_id).values('name', 'value')
    headers = {}
    for p in he:
        name = p.get('name')
        value = p.get('value')
        headers[name] = value
    env = Env.objects.get(id=env_id)
    if env.evn_port:
        url = env.env_url + ':' + env.evn_port + api.apiAddress
    else:
        url = env.env_url + api.apiAddress
    ur = url.encode('unicode-escape').decode('string_escape')
    try:
        # if method == 'post':
        #     r = requests.request('post', json=params, headers=headers, url=url)
        # else:
        #     r = requests.request('get', json=params, headers=headers, url=url)

        r = Public.execute(url=url, params=params, method=method, heads=headers)
        print r.text
        return JsonResponse(r.text, safe=False)
    except:
        data = '没有该接口，请检查接口信息'
        return JsonResponse(data, safe=False)



