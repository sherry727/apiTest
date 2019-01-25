# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Env,Project
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def env_index(request):
    return render(request, 'main/env.html')

@login_required
def getEvnList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    projects = Project.objects.filter(status=1).values('id')
    if key == '':
        p = Env.objects.filter(project_id__in=projects)
        resultdict = {}
        total = p.count()
        p = p[i:j]
        dict = []
        resultdict['total'] = total
        for a in p:
            dic = {}
            dic['id'] = a.id
            dic['project_id'] = a.project_id
            r=Project.objects.get(id=a.project_id)
            dic['projectName'] =r.name
            dic['name'] = a.env_name
            dic['url'] = a.env_url
            dic['port'] = a.evn_port
            dic['createTime'] = a.env_createTime.strftime("%Y-%m-%d %H:%M:%S")
            dic['desc'] = a.env_desc
            dic['user'] = a.user
            dict.append(dic)
        resultdict['code'] = 0
        resultdict['msg'] = ''
        resultdict['count'] = total
        resultdict['data'] = dict
        # print resultdict
        return JsonResponse(resultdict, safe=False)
    else:
        p = Env.objects.filter(env_name__contains=key, project_id__in=projects)
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
            dic['name'] = a.env_name
            dic['url'] = a.env_url
            dic['port'] = a.evn_port
            dic['createTime'] = a.env_createTime.strftime("%Y-%m-%d %H:%M:%S")
            dic['desc'] = a.env_desc
            dic['user'] = a.user
            dict.append(dic)
        resultdict['code'] = 0
        resultdict['msg'] = ''
        resultdict['count'] = total
        resultdict['data'] = dict
        # print resultdict
        return JsonResponse(resultdict, safe=False)
@login_required
def evnAdd(request):
    return render(request, 'main/env-add.html')

# 下拉选择框
@login_required
def selectProjectName(request):
    p = Project.objects.filter(status=1)
    dict=[]
    z=0
    for a in p:
        dic={}
        dic['projectName'] = a.name
        dic['id'] = a.id
        z=z+1
        dict.append(dic)
    return JsonResponse(dict, safe=False)

@login_required
def envAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        projectid = u.get('projectid')
        name = u.get('name')
        user = u.get('user')
        port= u.get('port')
        url = u.get('url')
        desc =u.get('desc')
        un = Env.objects.filter(env_url=url, evn_port=port)
        if not un:
            p = Env.objects.create(env_name=name, user=user, evn_port=port, env_url=url, env_desc=desc, project_id=projectid,env_createTime=timezone.now())
            p.save()
            resultdict = {
                'code': 0,
                'msg': 'success',
                'data': {'name': name}
            }
            return JsonResponse(resultdict, safe=False)
        else:
            resultdict = {
                'code': 2,
                'msg': '访问地址重复，请检查！',
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

@login_required
def envEdit(request,eid):
    u = Env.objects.get(id=eid)
    r = Project.objects.get(id=u.project_id)
    data = {
        'id': eid,
        'name': u.env_name,
        'url': u.env_url,
        'port': u.evn_port,
        'desc': u.env_desc,
        'projectName': r.name,
        'projectid':u.project_id,
        'user': u.user
    }
    return render(request, 'main/env-edit.html', data)

@login_required
def envEditPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        id=u.get('id')
        name = u.get('name')
        user = u.get('user')
        port = u.get('port')
        projectid = u.get('projectid')
        desc = u.get('desc')
        url = u.get('url')
        un = Env.objects.filter(env_url=url, evn_port=port).exclude(id=id).values_list()#排除id值的记录
        if len(un)==0:
            Env.objects.filter(id=id).update(env_name=name, user=user, env_url=url, evn_port=port, env_desc=desc, project_id=projectid)
            resultdict = {
                'code': 0,
                'msg': 'success',
                'data': {'id': id}
            }
            return JsonResponse(resultdict, safe=False)
        else:
            resultdict = {
                'code': 2,
                'msg': '同一个项目版本号重复',
                'data': {'name': name}

            }
            return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': '编辑失败',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

@login_required
def envDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        # u = request.body
        id=u.get('id')
        Env.objects.filter(id=id).delete()
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
