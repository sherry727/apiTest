# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project,Case,AutoApiCase,autoApiHead,autoAPIParameter,ApiCase,ApiHead,APIParameter,TestResult,globalVariable
from django_web.models import asserts
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json,re
from django.db.models import Q
from django_web.api import Public
import traceback
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
        print u
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
        ase = u.get('asserts')
        galobalValues = u.get('galobalValues')
        loginName = request.session.get('Username', '')
        p = AutoApiCase.objects.create(project_id=projectid, name=name, user=user, method=method,
                                       requestParameterType=requestParameterType,
                                       httpType=httptype, desc=desc, apiAddress=url, case_id=caseId, CreateTime=timezone.now(),status=1)
        p.save()
        if len(galobalValues) > 0:
            for h in galobalValues:
                try:
                    o = globalVariable.objects.get(name=h.get('gv_name'), user=loginName)
                    globalVariable.objects.filter(name=o.name).update(path=h.get('gv_path'), gType=2)
                except:
                    globalVariable.objects.create(name=h.get('gv_name'), path=h.get('gv_path'), autoApi_id=p.id,
                                                  user=loginName, gType=2).save()
        at = asserts.objects.filter(autoApi_id=p.id)
        asert=[]
        if len(ase) > 0:
            at.delete()
            for h in ase:
                nm = h.get('a_path')
                key = h.get('a_value')
                asert.append(asserts(value=key, autoApi_id=p.id, path=nm, user=user, CreateTime=timezone.now()))
            asserts.objects.bulk_create(asert)
        #
        # AutoApiCase.objects.filter(id=id).update(project_id=projectid, name=name, user=user, method=method,
        #                                          requestParameterType=requestParameterType,
        #                                          httpType=httptype, desc=desc, apiAddress=url,
        #                                          LastUpdateTime=timezone.now())
        headersList = []
        for h in headers:
            nm = h.get('head_name')
            key = h.get('head_key')
            headersList.append(autoApiHead(name=nm, api_id=p.id, value=key))
        autoApiHead.objects.bulk_create(headersList)
        paramsList = []
        for h in params:
            nm = h.get('param_name')
            key = h.get('param_key')
            paramType = h.get('paramType')
            paramsList.append(autoAPIParameter(name=nm, api_id=p.id, value=key, paramType=paramType))
        autoAPIParameter.objects.bulk_create(paramsList)
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
    g = globalVariable.objects.filter(autoApi_id=eid)
    a = asserts.objects.filter(autoApi_id=eid)
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

    gv = []
    for i in g:
        dic = {}
        dic['gv_name'] = i.name
        dic['gv_path'] = i.path
        gv.append(dic)
    at = []
    for i in a:
        dic = {}
        dic['a_value'] = i.value
        dic['a_path'] = i.path
        at.append(dic)
    print at
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
        'gv': gv,
        'asserts': at,
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
        ase = u.get('asserts')
        galobalValues = u.get('galobalValues')
        loginName = request.session.get('Username', '')
        sort = u.get('sort')
        gv=[]
        asert=[]
        if len(galobalValues) > 0:
            for h in galobalValues:
                try:
                    o = globalVariable.objects.get(name=h.get('gv_name'), user=loginName)
                    globalVariable.objects.filter(name=o.name).update(path=h.get('gv_path'), gType=2)
                except:
                    globalVariable.objects.create(name=h.get('gv_name'), path=h.get('gv_path'), autoApi_id=id, user=loginName,
                                                  gType=2).save()
        at= asserts.objects.filter(autoApi_id=id)
        if len(ase) > 0:
            at.delete()
            for h in ase:
                nm = h.get('a_path')
                key = h.get('a_value')
                asert.append(asserts(value=key, autoApi_id=id, path=nm, user=user, CreateTime=timezone.now()))
            asserts.objects.bulk_create(asert)

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
        print u
        env = Env.objects.get(id=eid)
        loginName = request.session.get('Username', '')
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
        print sorts
        for s in sorts:
            caseApi = AutoApiCase.objects.get(id=s.get('id'))
            he =autoApiHead.objects.filter(autoApi_id=s.get('id'))
            pa =autoAPIParameter.objects.filter(autoApi_id=s.get('id'))
            galobalValues =globalVariable.objects.filter(autoApi_id=s.get('id'))
            headers = {}
            params = {}
            for p in he:
                name = p.name
                value = p.value
                headers[name] = value
            for p in pa:
                if re.match(r'^\$\{(.+?)\}$', p.get('param_key')) != None:
                    w = re.sub('[${}]', '', p.get('param_key'))
                    value = globalVariable.objects.get(name=w).value
                else:
                    value = p.get('param_key')
                name = p.get('param_name')
                params[name] = value
            url1 =url+caseApi.apiAddress
            ur = url1.encode('unicode-escape').decode('string_escape')
            method = caseApi.method
            sort = s.get('sort')
            try:
                r = Public.execute(url=ur, params=params, method=method, heads=headers)
                if len(galobalValues) > 0:
                    for g in galobalValues:
                        # va = Public.get_value_from_response(response=r.text, json_path=g.get('gv_path').encode("utf-8"))
                        va = Public.get_value_from_response(response=r.text, json_path='data.accessToken')
                        # print va
                        try:
                            o = globalVariable.objects.get(name=g.get('gv_name'), user=loginName)
                            globalVariable.objects.filter(name=o.name).update(path=g.get('gv_path'), value=va)
                        except:
                            globalVariable.objects.create(name=g.get('gv_name'), path=g.get('gv_path'),
                                                          autoApi_id=s.get('id'), value=va, user=loginName,
                                                          gType=1).save()
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
    # print u
    api_id = u.get('id')
    api = AutoApiCase.objects.get(id=api_id)
    env_id = u.get('envid')
    method = u.get('method')
    sqlType = u.get('sqlType')
    sqlId = u.get('sqlId')
    sqlText = u.get('sqlText')
    sqlGlobalname = u.get('sqlGlobalname')
    pa = u.get('params')
    he = u.get('headers')
    user = u.get('user')
    galobalValues = u.get('galobalValues')
    duanyan= u.get('asserts')
    loginName= request.session.get('Username', '')
    gv = []
    i =0
    if sqlId and sqlType:
        for s in sqlText.split(";"):
            if s:
                rSql=Public.excuteSQL(sqlId=sqlId, sql=s)
                try:
                    globalVariable.objects.get(name=sqlGlobalname.split(";")[i])
                    globalVariable.objects.filter(name=sqlGlobalname.split(";")[i]).update(value=rSql, gType=1)
                except:
                    globalVariable.objects.create(name=sqlGlobalname.split(";")[i], autoApi_id=api_id, value=rSql, user=user, gType=1).save()
            i = i+1
    # pa = autoAPIParameter.objects.filter(autoApi_id=api_id).values('name', 'value')
    params = {}
    for p in pa:
        if re.match(r'^\$\{(.+?)\}$', p.get('param_key')) != None:
            w = re.sub('[${}]', '', p.get('param_key'))
            value= globalVariable.objects.get(name=w).value
        else:
            value = p.get('param_key')
        name = p.get('param_name')
        params[name] = value
    # he = autoApiHead.objects.filter(autoApi_id=api_id).values('name', 'value')
    headers = {}
    for p in he:
        name = p.get('head_name')
        value = p.get('head_key')
        headers[name] = value
    env = Env.objects.get(id=env_id)
    if env.evn_port:
        url = env.env_url + ':' + env.evn_port + api.apiAddress
    else:
        url = env.env_url + api.apiAddress
    ur = url.encode('unicode-escape').decode('string_escape')
    try:
        r = Public.execute(url=url, params=params, method=method, heads=headers)
        if len(galobalValues)>0:
            for g in galobalValues:
                va = Public.get_value_from_response(response=r.text, json_path=g.get('gv_path').encode("utf-8"))
                try:
                    o = globalVariable.objects.get(name=g.get('gv_name'), user=loginName)
                    globalVariable.objects.filter(name=o.name).update(path=g.get('gv_path'), value=va, gType=2)
                except:
                    globalVariable.objects.create(name=g.get('gv_name'), path=g.get('gv_path'), autoApi_id=api_id, value=va, user=loginName,
                                                  gType=2).save()
        dy=[]
        if len(duanyan)>0:
            for a in duanyan:
                nm = a.get('a_path')
                key = a.get('a_value')
                real_value = Public.get_value_from_response(response=r.text, json_path=nm.encode("utf-8"))
                if key.encode("utf-8")==str(real_value):
                    AutoApiCase.objects.filter(id=api_id).update(status='成功')
                else:
                    AutoApiCase.objects.filter(id=api_id).update(status='失败')


                ast = asserts.objects.filter(autoApi_id=api_id,path=nm)
                if len(ast)> 2:
                    dy.append(asserts(path=nm, autoApi_id=api_id, value=key, user=user, real_value=real_value, CreateTime=timezone.now()))
                else:
                    asserts.objects.filter(autoApi_id=api_id, path=nm).update(value=key, real_value=real_value)
            asserts.objects.bulk_create(dy)

        return JsonResponse(r.text, safe=False)
    except Exception, e:
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        data = '没有该接口，请检查接口信息'
        return JsonResponse(data, safe=False)



