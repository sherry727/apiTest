# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project,ApiCase,ApiHead,APIParameter
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
import requests
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core import serializers


@login_required
def api_index(request):
    return render(request, 'main/api.html')

@login_required
def getApiList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    projectid=request.GET.get('projectid')
    projects = Project.objects.filter(status=1).values('id')
    if key == ''and projectid == '':
        p = ApiCase.objects.filter(status=1, project_id__in=projects).order_by('-CreateTime')
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
    elif projectid:
        p = ApiCase.objects.filter(name__contains=key, project_id=projectid, status=1).order_by('-CreateTime')
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
        # print resultdict
        return JsonResponse(resultdict, safe=False)
    else:
        p = ApiCase.objects.filter(name__contains=key, status=1,project_id__in=projects).order_by('-CreateTime')
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
        # print resultdict
        return JsonResponse(resultdict, safe=False)

@login_required
def apiAdd(request):
    return render(request, 'main/api-add.html')

@login_required
def apiAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        projectid = u.get('projectid')
        name = u.get('name')
        user = u.get('user')
        method= u.get('method')
        requestParameterType = u.get('requestParameterType')
        url = u.get('url')
        desc =u.get('desc')
        httptype =u.get('httptype')
        headers = u.get('headers')
        params = u.get('params')
        p=ApiCase.objects.create(project_id=projectid, name=name, user=user, method=method, requestParameterType=requestParameterType,
                                 httpType=httptype, desc=desc, apiAddress=url, CreateTime=timezone.now())
        p.save()
        ap = ApiCase.objects.last()
        headersList=[]
        for h in headers:
            nm= h.get('head_name')
            key = h.get('head_key')
            headersList.append(ApiHead(name=nm, api_id=p.id, value=key))
        ApiHead.objects.bulk_create(headersList)
        paramsList = []
        for h in params:
            nm = h.get('param_name')
            key = h.get('param_key')
            paramType = h.get('paramType')
            paramsList.append(APIParameter(name=nm, api_id=p.id, value=key, paramType=paramType))
        APIParameter.objects.bulk_create(paramsList)
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

@login_required
def apiEdit(request,aid):
    u = ApiCase.objects.get(id=aid)#接口表
    h = ApiHead.objects.filter(api_id=aid)#请求头
    m = APIParameter.objects.filter(api_id=aid)#请求参数
    p = Project.objects.get(id=u.project_id)#项目表
    params =[]
    for i in m:
        dic={}
        dic['param_name']=i.name
        dic['param_key'] =i.value
        dic['paramType'] =i.paramType
        params.append(dic)
    headers = []
    for i in h:
        dic = {}
        dic['head_name'] = i.name
        dic['head_key'] = i.value
        headers.append(dic)
    data = {
        'id': aid,
        'name': u.name,
        'url': u.apiAddress,
        'requestParameterType': u.requestParameterType,
        'httptype': u.httpType,
        'method': u.method,
        'projectName': p.name,
        'projectid': u.project_id,
        'user': u.user,
        'params':params,
        'headers':headers,
        'desc': u.desc
    }
    return render(request, 'main/api-edit.html', data)

def apiDetail(request,pid):
    u = ApiCase.objects.get(id=pid)  # 接口表
    h = ApiHead.objects.filter(api_id=pid)  # 请求头
    m = APIParameter.objects.filter(api_id=pid)  # 请求参数
    p = Project.objects.get(id=u.project_id)  # 项目表
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
        'id': pid,
        'name': u.name,
        'url': u.apiAddress,
        'requestParameterType': u.requestParameterType,
        'httptype': u.httpType,
        'method': u.method,
        'projectName': p.name,
        'projectid': u.project_id,
        'user': u.user,
        'LastUpdateTime': u.LastUpdateTime.strftime("%Y-%m-%d %H:%M:%S"),
        'CreateTime': u.CreateTime.strftime("%Y-%m-%d %H:%M:%S"),
        'params': params,
        'headers': headers
    }
    return render(request, 'main/api-detail.html', data)

@login_required
def apiDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        # u = request.body
        id=u.get('id')
        ApiCase.objects.filter(id=id).delete()
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

def apiEditPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
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
        ApiCase.objects.filter(id=id).update(project_id=projectid, name=name, user=user, method=method,
                                             requestParameterType=requestParameterType,
                                             httpType=httptype, desc=desc, apiAddress=url, LastUpdateTime=timezone.now())
        ApiHead.objects.filter(api_id=id).delete()
        APIParameter.objects.filter(api_id=id).delete()
        headersList = []
        for h in headers:
            nm = h.get('head_name')
            key = h.get('head_key')
            headersList.append(ApiHead(name=nm, api_id=id, value=key))
        ApiHead.objects.bulk_create(headersList)
        paramsList = []
        for h in params:
            nm = h.get('param_name')
            key = h.get('param_key')
            type = h.get('paramType')
            paramsList.append(APIParameter(name=nm, api_id=id, value=key,paramType=type))
        APIParameter.objects.bulk_create(paramsList)
        # api_headers_old = ApiHead.objects.filter(api_id=id).values_list("head_name", flat=True)
        # api_params_old = APIParameter.objects.filter(api_id=id).values_list("param_name", flat=True)
        # api_headers_list = []
        # api_params_list = []
        # for head in headers:
        #     if head['head_key'] in api_headers_old:
        #         ApiHead.objects.filter(head_name=head['head_key']).update(head_value=head['head_value'])
        #     elif head['head_key'] is not None and head['head_key'] != '':
        #         api_headers_list.append(
        #             ApiHead(api_id=id, head_name=head['head_key'], head_value=head['head_value']))
        #  ApiHead.objects.bulk_create(api_headers_list)
        # for header_old in api_headers_old:
        #     if header_old not in [x['head_key'] for x in headers]:
        #         ApiHead.objects.get(head_name=header_old).delete()
        # for param in params:
        #     if param['param_name'] in api_params_old:
        #         APIParameter.objects.filter(param_name=param['param_name']).update(param_key=param['param_key'])
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

def simpleRun(request,pid):
    u = ApiCase.objects.get(id=pid)  # 接口表
    h = ApiHead.objects.filter(api_id=pid)  # 请求头
    m = APIParameter.objects.filter(api_id=pid)  # 请求参数
    p = Project.objects.get(id=u.project_id)  # 项目表
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
        'id': pid,
        'name': u.name,
        'url': u.apiAddress,
        'requestParameterType': u.requestParameterType,
        'httptype': u.httpType,
        'method': u.method,
        'projectName': p.name,
        'projectid': u.project_id,
        'user': u.user,
        'LastUpdateTime': u.LastUpdateTime.strftime("%Y-%m-%d %H:%M:%S"),
        'CreateTime': u.CreateTime.strftime("%Y-%m-%d %H:%M:%S"),
        'params': params,
        'headers': headers
    }
    return render(request,'main/testRun.html', data)

def apiSimpleRun(request):
    u = json.loads(request.body)
    api_id = u.get('id')
    api=ApiCase.objects.get(id=api_id)
    env_id = u.get('envid')
    method=u.get('method')
    pa= APIParameter.objects.filter(api_id=api_id).values('name', 'value')
    params = {}
    for p in pa:
        # type=p.get('paramType')
        # if type == 'int':
        #     name= p.get('name')
        #     val = p.get('value')
        #     value=int(val)
        #     params[name] = value
        # else:
        name = p.get('name')
        value = p.get('value')
        params[name] = value
    he =ApiHead.objects.filter(api_id=api_id).values('name', 'value')
    headers = {}
    for p in he:
        name = p.get('name')
        value = p.get('value')
        headers[name] = value
    env = Env.objects.get(id=env_id)
    if env.evn_port:
         url = env.env_url+':'+env.evn_port+api.apiAddress
    else:
        url = env.env_url+api.apiAddress
    ur= url.encode('unicode-escape').decode('string_escape')
    if method =='post':
        r = requests.request('post', json=params, headers=headers, url=url)
    else:
        r = requests.request('get', json=params, headers=headers, url=url)
    print r.content
    return JsonResponse(r.text, safe=False)

#环境下拉
def selectEnvName(request,eid):
    p = Env.objects.filter(project_id=eid)
    dict = []
    for a in p:
        dic = {}
        dic['ename'] = a.env_name
        dic['eid'] = a.id
        dict.append(dic)
    return JsonResponse(dict, safe=False)

@login_required
def copyApi(request,pid):
    u = ApiCase.objects.get(id=pid)#接口表
    h = ApiHead.objects.filter(api_id=pid)#请求头
    m = APIParameter.objects.filter(api_id=pid)#请求参数
    p = Project.objects.get(id=u.project_id)#项目表
    params =[]
    for i in m:
        dic={}
        dic['param_name']=i.name
        dic['param_key'] =i.value
        dic['paramType'] =i.paramType
        params.append(dic)
    headers = []
    for i in h:
        dic = {}
        dic['head_name'] = i.name
        dic['head_key'] = i.value
        headers.append(dic)
    data = {
        'id': pid,
        'name': u.name,
        'url': u.apiAddress,
        'requestParameterType': u.requestParameterType,
        'httptype': u.httpType,
        'method': u.method,
        'projectName': p.name,
        'projectid': u.project_id,
        'user': u.user,
        'params':params,
        'headers':headers,
        'desc': u.desc
    }
    return render(request, 'main/api-copy.html', data)

@login_required
def apiCopyPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        projectname = u.get('projectid')
        p = Project.objects.get(name=projectname)
        projectid = p.id
        name = u.get('name')
        user = u.get('user')
        method= u.get('method')
        requestParameterType = u.get('requestParameterType')
        url = u.get('url')
        desc =u.get('desc')
        httptype =u.get('httptype')
        headers = u.get('headers')
        params = u.get('params')
        p=ApiCase.objects.create(project_id=projectid, name=name, user=user, method=method, requestParameterType=requestParameterType,
                                 httpType=httptype, desc=desc, apiAddress=url, CreateTime=timezone.now(),status=1)
        p.save()
        ap = ApiCase.objects.last()
        headersList=[]
        for h in headers:
            nm= h.get('head_name')
            key = h.get('head_key')
            headersList.append(ApiHead(name=nm, api_id=ap.id, value=key))
        ApiHead.objects.bulk_create(headersList)
        paramsList = []
        for h in params:
            nm = h.get('param_name')
            key = h.get('param_key')
            paramType = h.get('paramType')
            paramsList.append(APIParameter(name=nm, api_id=ap.id, value=key, paramType=paramType))
        APIParameter.objects.bulk_create(paramsList)
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
