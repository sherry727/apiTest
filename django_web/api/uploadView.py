# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Project,uploadFile
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db.models import Q
import json,os
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def file_index(request):
    return render(request, 'main/file_index.html')

def fileList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    key = request.GET.get('keyword')
    q1 = Q()
    q1.connector = 'AND'
    if len(key) > 0:
        q1.children.append(('name__contains', key))
    p = uploadFile.objects.filter(q1).order_by('-CreateTime')
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
        dic['path'] = a.path
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

def fileAdd(request):
    return render(request, 'main/file-add.html')

def fileAddPost(request):
    if request.method == "POST":
        u = json.loads(request.body)
        loginName = request.session.get('Username', '')
        print u
        filename = u.get('filename')
        projectid = u.get('projectid')
        desc = u.get('desc')
        fpath = u.get('fpath')
        p=uploadFile.objects.create(user=loginName, name=filename, project_id=projectid, desc=desc, path=fpath,CreateTime=timezone.now())
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

def upload(request):
    File = request.FILES.get("upFile", None)
    resultdict = {}
    resultdict['code'] = 0
    resultdict['msg'] = ''
    if File is None:
        return HttpResponse("没有需要上传的文件")
        resultdict['name'] = ''
        resultdict['path'] = ''
    else:
        # 打开特定的文件进行二进制的写操作
        # print(os.path.exists('/temp_file/'))
        with open("./django_web/temp_file/%s" % File.name, 'wb+') as f:
            # 分块写入文件
            for chunk in File.chunks():
                f.write(chunk)
        resultdict['name'] = File.name
        resultdict['path'] = "./django_web/temp_file/%s" % File.name
    print resultdict
    return JsonResponse(resultdict, safe=False)

def fileDelete(request):
    if request.method == "POST":
        u = json.loads(request.body)
        id=u.get('id')
        p = uploadFile.objects.get(id=id)
        if os.path.exists(p.path):
            os.remove(p.path)
        uploadFile.objects.filter(id=id).delete()
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