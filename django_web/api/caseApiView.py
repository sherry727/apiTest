# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project,Case,AutoApiCase,autoApiHead,autoAPIParameter,ApiCase,ApiHead,APIParameter,TestResult,globalVariable
from django_web.models import uploadFile,fuctionLib
from django_web.models import asserts
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json,re
from django.db.models import Q
from django_web.api import Public, fuctionView
import traceback,os
from django.utils import timezone
from django.conf import settings
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
    p = AutoApiCase.objects.filter(q1).order_by('CreateTime')
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
        print(u)
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
        selectFuction = u.get('selectFuction')
        galobalValues = u.get('galobalValues')
        loginName = request.session.get('Username', '')
        p = AutoApiCase.objects.create(project_id=projectid, name=name, user=user, method=method,
                                       requestParameterType=requestParameterType,
                                       httpType=httptype, desc=desc, apiAddress=url, case_id=caseId,
                                       CreateTime=timezone.now(), status=1, fuctionLib_id=selectFuction)
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
            headersList.append(autoApiHead(name=nm, autoApi_id=p.id, value=key))
        autoApiHead.objects.bulk_create(headersList)
        paramsList = []
        for h in params:
            nm = h.get('param_name')
            key = h.get('param_key')
            paramType = h.get('paramType')
            paramsList.append(autoAPIParameter(name=nm, autoApi_id=p.id, value=key, paramType=paramType))
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
    loginName = request.session.get('Username', '')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    projectid = request.GET.get('projectId')
    projects = Project.objects.filter(status=1).values('id')
    q1 = Q()
    q1.connector = 'AND'
    if len(projectid) > 0:
        q1.children.append(('project_id', projectid))
    p = ApiCase.objects.filter(q1, user=loginName).order_by('-CreateTime')
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
        loginName = request.session.get('Username', '')
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
            params = APIParameter.objects.filter(Q(api_id=apiId), ~Q(paramType='File'))
            files = APIParameter.objects.filter(api_id=apiId, paramType='File')
            p = AutoApiCase.objects.create(project_id=projectid, name=name, user=loginName, method=method,
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
            f=[]
            for h in files:
                fi = uploadFile.objects.get(id=h.file_id)
                nm =fi.name
                key = h.value
                fname = fi.fname
                fparamType = 'File'
                e = uploadFile.objects.create(name=nm, path=key, user=loginName, CreateTime=timezone.now(),
                                              project_id=projectid,
                                              api_id=p.id, typeApi=2, fname=fname)
                e.save()
                f.append(autoAPIParameter(name=nm, autoApi_id=p.id, value=key, paramType=fparamType, file_id=e.id))
            autoAPIParameter.objects.bulk_create(f)
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
    m = autoAPIParameter.objects.filter(Q(autoApi_id=eid), ~Q(paramType='File'))  # 请求参数
    fi = autoAPIParameter.objects.filter(autoApi_id=eid, paramType='File')  # 请求参数
    p = Project.objects.get(id=u.project_id)  # 项目表
    g = globalVariable.objects.filter(autoApi_id=eid)
    a = asserts.objects.filter(autoApi_id=eid)
    try:
        fc = fuctionLib.objects.get(id=u.fuctionLib_id)
        fcname=fc.name
        fcid=fc.id
    except:
        fcname = ''
        fcid = ''
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
    files = []
    for j in fi:
        dic = {}
        dic['param_name'] = j.name
        dic['param_key'] = j.value
        dic['paramType'] = j.paramType
        f = uploadFile.objects.get(id=j.file_id)
        dic['fname'] = f.fname
        files.append(dic)
    data = {
        'id': eid,
        'name': u.name,
        'url': u.apiAddress,
        'fuctionName': fcname,
        'fuctionId': fcid,
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
        'files': files,
        'sort': u.sort
    }
    return render(request, 'main/caseApi-edit.html', data)


def caseApiDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        # u = request.body
        id=u.get('id')
        AutoApiCase.objects.filter(id=id).delete()
        uploadFile.objects.filter(api_id=id, typeApi=2).delete()
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
        fu = u.get('selectFuction')
        loginName = request.session.get('Username', '')
        sort = u.get('sort')
        files = u.get('files')
        uploadFile.objects.filter(api_id=id).delete()
        gv=[]
        asert=[]
        try:
            ul=Public.global_variable(key=url)
        except:
            resultdict = {
                'code': 2,
                'msg': '全局变量不存在，请检查！',
                'data': {}
            }
            return JsonResponse(resultdict, safe=False)
        if len(galobalValues) > 0:
            for h in galobalValues:
                try:
                    o = globalVariable.objects.get(name=h.get('gv_name'), user=loginName)
                    globalVariable.objects.filter(name=o.name).update(path=h.get('gv_path'), gType=2)
                except:
                    globalVariable.objects.create(name=h.get('gv_name'), path=h.get('gv_path'), autoApi_id=id, user=loginName,
                                                  gType=2).save()
        at= asserts.objects.filter(autoApi_id=id)
        if at:
            at.delete()
        if len(ase) > 0:
            for h in ase:
                nm = h.get('a_path')
                key = h.get('a_value')
                asert.append(asserts(value=key, autoApi_id=id, path=nm, user=loginName, CreateTime=timezone.now()))
            asserts.objects.bulk_create(asert)
        if len(fu)>0:
            fuction_id = int(fu)
        else:
            fuction_id = 0

        AutoApiCase.objects.filter(id=id).update(project_id=projectid, name=name, user=user, method=method,
                                                 requestParameterType=requestParameterType, httpType=httptype, desc=desc,
                                                 apiAddress=url, LastUpdateTime=timezone.now(), fuctionLib_id=fuction_id)
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
        filesList = []
        for h in files:
            nm = h.get('file_name')
            key = h.get('fpath')
            fname = h.get('fname')
            paramType = h.get('pType')
            e = uploadFile.objects.create(name=nm, path=key, user=loginName, CreateTime=timezone.now(),
                                          project_id=projectid,
                                          api_id=id, typeApi=2, fname=fname)
            e.save()
            filesList.append(autoAPIParameter(name=nm, autoApi_id=id, value=key, paramType=paramType, file_id=e.id))
        autoAPIParameter.objects.bulk_create(filesList)
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
        loginName = request.session.get('Username', '')
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
            pa =autoAPIParameter.objects.filter(Q(autoApi_id=s.get('id')), ~Q(paramType='File'))
            galobalValues =globalVariable.objects.filter(autoApi_id=s.get('id'))
            duanyan = asserts.objects.filter(autoApi_id=s.get('id'))
            files = autoAPIParameter.objects.filter(Q(autoApi_id=s.get('id')), Q(paramType='File')).values('name', 'value', 'file_id')
            headers = {}
            params = {}
            fi = {}

            for p in he:
                name = p.name
                value = p.value
                headers[name] = value
            for p in pa:
                if re.match(r'^\$\{(.+?)\}$', p.value) != None:
                    w = re.sub('[${}]', '', p.value)
                    try:
                        value = globalVariable.objects.get(name=w).value
                    except:
                        resultdict = {
                            'code': 1,
                            'msg': '请输入正确的全局变量',
                            'data': {}
                        }
                        return JsonResponse(resultdict, safe=False)
                else:
                    value = p.value
                name = p.name
                params[name] = value
            for f in files:
                if re.match(r'^\$\{(.+?)\}$', f.get('value')) != None:
                    w = re.sub('[${}]', '', f.get('value'))
                    try:
                        value = globalVariable.objects.get(name=w).value
                    except:
                        resultdict = {
                            'code': 1,
                            'msg': '请输入正确的全局变量',
                            'data': {}
                        }
                        return JsonResponse(resultdict, safe=False)
                else:
                    value = f.get('value')
                name = f.get('name')
                e = uploadFile.objects.get(id=f.get('file_id'))
                fi[name] = ((e.fname, open(os.path.join(settings.FILE_PATH, e.fname), 'rb'), 'file'))

            if caseApi.fuctionLib_id:
                fu = fuctionView.qianming(fu_id=int(caseApi.fuctionLib_id), appKey=env.appKey, app_secret=env.app_secret,
                                          jdata=params)
                params = fu
            address = Public.global_variable(key=caseApi.apiAddress)
            url1 =url+address
            # ur = url1.encode('unicode-escape').decode('string_escape')
            method = caseApi.method
            sort = s.get('sort')
            try:
                # r = Public.execute(url=ur, params=params, method=method, heads=headers)
                if fi:
                    r = Public.execute(url=url1, params=params, method=method, heads=headers, files=fi)
                else:
                    r = Public.execute(url=url1, params=params, method=method, heads=headers)
                if len(galobalValues) > 0:
                    for g in galobalValues:
                        # va = Public.get_value_from_response(response=r.text, json_path=g.get('gv_path'))
                        va = Public.get_value_from_response(response=r.text, json_path='data.accessToken')
                        try:
                            o = globalVariable.objects.get(name=g.name, user=loginName)
                            globalVariable.objects.filter(name=o.name).update(path=g.path, value=va)
                        except Exception as result:
                            print("未知错误 %s" % result)
                print(r.text)
                dy = []
                if len(duanyan) > 0:
                    for a in duanyan:
                        nm = a.path
                        key = a.value
                        real_value = Public.get_value_from_response(response=r.text, json_path=nm)
                        print(real_value)
                        if key == str(real_value):
                            AutoApiCase.objects.filter(id=s.get('id')).update(status='成功')
                        else:
                            AutoApiCase.objects.filter(id=s.get('id')).update(status='失败')
                        ast = asserts.objects.filter(autoApi_id=s.get('id'), path=nm)
                        if len(ast) > 2:
                            dy.append(
                                asserts(path=nm, autoApi_id=s.get('id'), value=key, user=loginName, real_value=real_value,
                                        CreateTime=timezone.now()))
                        else:
                            asserts.objects.filter(autoApi_id=s.get('id'), path=nm).update(value=key, real_value=real_value)
                    asserts.objects.bulk_create(dy)
                else:
                    AutoApiCase.objects.filter(id=s.get('id')).update(status='成功')
            except Exception as result:
                print("未知错误 %s" % result)
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
    api_id = u.get('id')
    api = AutoApiCase.objects.get(id=api_id)
    env_id = u.get('envid')
    address = u.get('url')
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
    files= u.get('files')
    fuction_id= u.get('selectFuction')
    loginName= request.session.get('Username', '')
    gv = []
    i =0
    address=Public.global_variable(key=address)
    if env_id=='请选择':
        data = {
            'code': 1,
            'msg': "请选择执行环境！"
        }
        return JsonResponse(data, safe=False)
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
    fi = {}
    for f in files:
        if re.match(r'^\$\{(.+?)\}$', f.get('fpath')) != None:
            w = re.sub('[${}]', '', f.get('fpath'))
            value= globalVariable.objects.get(name=w).value
        else:
            value = f.get('fpath')
        name = f.get('file_name')
        fi[name] = ((f.get('fname'), open(os.path.join(settings.FILE_PATH, f.get('fname')), 'rb'), 'file'))
    params = {}
    for p in pa:
        if re.match(r'^\$\{(.+?)\}$', p.get('param_key')) != None:
            w = re.sub('[${}]', '', p.get('param_key'))
            try:
                value= globalVariable.objects.get(name=w).value
            except Exception as result:
                print("未知错误 %s" % result)
                data = {
                    'code':1,
                    'msg' :"请检查全局变量参数！"
                }
                return JsonResponse(data, safe=False)
        else:
            value = p.get('param_key')
        name = p.get('param_name')
        params[name] = value
    headers = {}
    for p in he:
        name = p.get('head_name')
        value = p.get('head_key')
        headers[name] = value
    env = Env.objects.get(id=env_id)
    if env.evn_port:
        url = env.env_url + ':' + env.evn_port + address
    else:
        url = env.env_url + address
    # ur = url.encode('unicode-escape').decode('string_escape')
    if len(fuction_id) > 0:
        fu=fuctionView.qianming(fu_id=int(fuction_id), appKey=env.appKey, app_secret=env.app_secret, jdata=params)
        params= fu
    try:
        if fi:
            r = Public.execute(url=url, params=params, method=method, heads=headers, files=fi)
        else:
            r = Public.execute(url=url, params=params, method=method, heads=headers)
        if len(galobalValues)>0:
            for g in galobalValues:
                va = Public.get_value_from_response(response=r.text, json_path=g.get('gv_path'))
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
                real_value = Public.get_value_from_response(response=r.text, json_path=nm)
                if key==str(real_value):
                    AutoApiCase.objects.filter(id=api_id).update(status='成功')
                    data = {
                        'code': 0,
                        'msg': r.text
                    }
                else:
                    AutoApiCase.objects.filter(id=api_id).update(status='失败')
                    data = {
                        'code': 1,
                        'msg': "断言失败："+r.text
                    }
                ast = asserts.objects.filter(autoApi_id=api_id, path=nm)
                if len(ast)> 2:
                    dy.append(asserts(path=nm, autoApi_id=api_id, value=key, user=loginName, real_value=real_value, CreateTime=timezone.now()))
                else:
                    asserts.objects.filter(autoApi_id=api_id, path=nm).update(value=key, real_value=real_value)
            asserts.objects.bulk_create(dy)
        else:
            AutoApiCase.objects.filter(id=api_id).update(status='成功')
            data = {
                'code': 0,
                'msg': r.text
            }
        return JsonResponse(data, safe=False)
    except Exception as e:
        print('traceback.format_exc():\n%s' % traceback.format_exc())
        data = {
            'code': 1,
            'msg': '没有该接口，请检查接口信息'
        }
        return JsonResponse(data, safe=False)


def selectFuction(request):
    p = fuctionLib.objects.filter(ftype=0)
    dict = []
    for a in p:
        dic = {}
        dic['id'] = a.id
        dic['name'] = a.name
        dict.append(dic)
    return JsonResponse(dict, safe=False)


