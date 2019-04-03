# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django_web.models import manage_permission
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission,ContentType
import time
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def role_index(request):
    return render(request, 'main/role.html')

def setAuthority(request,uid):
    return render(request, 'main/setAuthority.html')

def AuthTree(request):
    resultdict={}
    resultdict['code'] = 0
    resultdict['msg'] = '获取成功'
    mp1 =manage_permission.objects.filter(rank=1)
    trees1=[]

    m2 = manage_permission.objects.filter(rank=2)
    for m in mp1:
        tr = json.loads(m.content_type_id)  # ids
        dict={}
        trees2 = []
        dict['name'] =m.name
        dict['value']=m.id
        dict['checked']=True
        dict['disabled']=False
        for i in m2:
            trees3 = []
            content_type_id= json.loads(i.content_type_id)
            p = manage_permission.objects.get(content_type_id=content_type_id)
            if content_type_id in tr:
                d2={}
                d2['name'] = p.name
                d2['value'] = p.id
                d2['checked'] = True
                d2['disabled'] = False
                m3=Permission.objects.filter(content_type_id=content_type_id)
                for j in m3:
                    d3={}
                    d3['name'] = j.name
                    d3['value'] = j.id
                    d3['checked'] = True
                    d3['disabled'] = False
                    trees3.append(d3)
                d2['list'] =trees3
                trees2.append(d2)
        dict['list']=trees2
        trees1.append(dict)
    # print trees1
    resultdict['data'] = {'trees': trees1}
    # data={
    #       "code": 0,
    #       "msg": "获取成功",
    #       "data": {
    #         "trees":[
    #             {"name": "用户管理", "value": "yhgl", "checked": True, "disabled": False},
    #             {"name": "用户组管理", "value": "yhzgl", "checked": True, "disabled": False, "list": [
    #                 {"name": "角色管理", "value": "yhzgl-jsgl", "checked": True, "disabled": False, "list":[
    #                     {"name": "添加角色", "value": "yhzgl-jsgl-tjjs", "checked": True, "disabled": False},
    #                     {"name": "角色列表", "value": "yhzgl-jsgl-jslb", "checked": False, "disabled": False}
    #                 ]},
    #             {"name": "管理员管理", "value": "glygl", "checked": False, "disabled": False, "list":[
    #               {"name": "添加管理员", "value": "glygl-tjgly", "checked": False, "disabled": False},
    #               {"name": "管理员列表", "value": "glygl-glylb", "checked": False, "disabled": True},
    #               {"name": "管理员管理", "value": "glygl-glylb", "checked": False, "disabled": True}
    #             ]}
    #           ]}
    #         ]
    #       }
    #     }
    return JsonResponse(resultdict, safe=False)

def roleSelect(request):
    data={}
    return JsonResponse(data,safe=False)