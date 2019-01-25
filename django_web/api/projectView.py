# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Project
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def project_index(request):
    return render(request, 'main/project.html')

@login_required
def getProjectList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    if key == '':
        p = Project.objects.all()
        resultdict = {}
        total = p.count()
        p = p[i:j]
        dict = []
        resultdict['total'] = total
        for a in p:
            dic = {}
            dic['id'] = a.id
            dic['name'] = a.name
            dic['type'] = a.type
            dic['description'] = a.description
            dic['version'] = a.version
            dic['status'] = a.status
            dic['LastUpdateTime'] = a.LastUpdateTime.strftime("%Y-%m-%d %H:%M:%S")
            dic['user'] = a.user
            dict.append(dic)
        resultdict['code'] = 0
        resultdict['msg'] = ''
        resultdict['count'] = total
        resultdict['data'] = dict
        # print resultdict
        return JsonResponse(resultdict, safe=False)
    else:
        p = Project.objects.filter(name__contains=key)
        resultdict = {}
        total = p.count()
        p = p[i:j]
        dict = []
        for a in p:
            dic = {}
            dic['id'] = a.id
            dic['name'] = a.name
            dic['type'] = a.type
            dic['description'] = a.description
            dic['version'] = a.version
            dic['status'] = a.status
            dic['LastUpdateTime'] = a.LastUpdateTime.strftime("%Y-%m-%d %H:%M:%S")
            dic['user'] = a.user
            dict.append(dic)
        resultdict['code'] = 0
        resultdict['msg'] = ''
        resultdict['count'] = total
        resultdict['data'] = dict
        # print resultdict
        return JsonResponse(resultdict, safe=False)


def projectAdd(request):
    return render(request, 'main/project-add.html')

def projectAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        name = u.get('name')
        user = u.get('user')
        version = u.get('version')
        type = u.get('ProjectType')
        desc =u.get('desc')
        status =u.get('status')
        if status:
            status=u.get('status')
        else:
            status = 0
        un = Project.objects.filter(name=name, version=version)
        if not un:
            p = Project.objects.create(name=name, user=user, version=version, type=type, description=desc, status=status)
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
                'msg': '项目名称重复',
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

def projectEdit(request,pid):
    u = Project.objects.get(id=pid)
    data={
        'pid': pid,
        'name': u.name,
        'version': u.version,
        'type': u.type,
        'desc': u.description,
        'status': u.status,
        'user': u.user
    }
    return render(request, 'main/project-edit.html', data)

def projectEditPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        id=u.get('id')
        name = u.get('name')
        user = u.get('user')
        version = u.get('version')
        type = u.get('ProjectType')
        desc = u.get('desc')
        status = u.get('status')
        if status:
            status=u.get('status')
        else:
            status = 0
        un = Project.objects.filter(name=name, version=version).exclude(id=id).values_list()
        if len(un)==0:
            Project.objects.filter(id=id).update(name=name, user=user, version=version, type=type, description=desc, status=status, LastUpdateTime=timezone.now())
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

def projectDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        # u = request.body
        id=u.get('id')
        Project.objects.filter(id=id).delete()
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

