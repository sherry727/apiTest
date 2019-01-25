# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.contrib.auth.hashers import make_password
import time
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def welcom(request):
    return render(request, 'main/welcome.html')

@login_required
def index(request):
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'main/login.html')

def login_action(request):
    if request.method == "POST":
        Username = request.POST.get("username")
        Password = request.POST.get("password")
        # print Username,Password
        user = auth.authenticate(username=Username, password=Password)
        if user != None:
            auth.login(request,user)
            request.session["Username"]=Username
            return HttpResponseRedirect("/index/")
        else:
            return render(request, 'main/login.html', {"error": "Username and Password is error"})
    # return render(request, 'main/login.html')
    auth.login()


@login_required
def userManager(request):
    return render(request, 'main/user.html')

def getUserList(request):
    User1 = get_user_model()
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    ukey = request.GET.get('keyword')
    if ukey =='':
        User = User1.objects.all()
        print User
        total = User.count()
        resultdict = {}
        User = User[i:j]
        resultdict['total'] = total
        dict = []
        for p in User:
            dic = {}
            dic['id'] = p.id
            dic['username'] = p.username
            dic['email'] = p.email
            dic['date_joined'] = p.date_joined.strftime("%Y-%m-%d %H:%M:%S")
            dict.append(dic)
        resultdict['code'] = 0
        resultdict['msg'] = ''
        resultdict['count'] = total
        resultdict['data'] = dict
        # print resultdict
        return JsonResponse(resultdict, safe=False)
    else:
        User = User1.objects.filter(username__contains=ukey)
        total = User.count()
        resultdict = {}
        User = User[i:j]
        resultdict['total'] = total
        dict = []
        for p in User:
            dic = {}
            dic['id'] = p.id
            dic['username'] = p.username
            dic['email'] = p.email
            dic['date_joined'] = p.date_joined
            dict.append(dic)
        resultdict['code'] = 0
        resultdict['msg'] = ''
        resultdict['count'] = total
        resultdict['data'] = dict
        # print resultdict
        return JsonResponse(resultdict, safe=False)


def userAdd(request):
    return render(request, 'main/user-add.html')

def userPost(request):
    User = get_user_model()
    if request.method == "POST":
        u = json.loads(request.body)
        username = u.get('username')
        email = u.get('email')
        password = u.get('password')
        un = User.objects.filter(username=username)
        if not un:

            # status = request.POST.get('status')
            user = User.objects.create(username=username, email=email, password=make_password(password))
            user.save()
            resultdict={
                'code': 0,
                'msg': 'success',
                'data': {'username': username}

            }
            return JsonResponse(resultdict, safe=False)
        else:
            resultdict = {
                'code': 2,
                'msg': '用户名重复',
                'data': {'username': username}

            }
            return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)

def userEdit(request,uid):
    # print uid
    User = get_user_model()
    u = User.objects.get(id=uid)
    # print u.username
    data={
        'uid': uid,
        'username': u.username,
        'email': u.email,
        'password': u.password
    }
    return render(request, 'main/user-edit.html', data)

def userEditPost(request):
    User = get_user_model()
    if request.method == "POST":
        u = json.loads(request.body)
        uid = u.get('id')
        username = u.get('username')
        email = u.get('email')
        password = u.get('password')
        # print uid
        un = User.objects.filter(username=username).exclude(id=uid).values_list()
        # print len(un)
        if len(un)==0:
            # status = request.POST.get('status')
            user = User.objects.filter(id=uid).update(username=username, email=email, password=make_password(password))
            # user.save()
            resultdict = {
                'code': 0,
                'msg': 'success',
                'data': {'id': uid}
            }
            return JsonResponse(resultdict, safe=False)
        else:
            resultdict = {
                'code': 2,
                'msg': '用户名重复',
                'data': {'username': username}

            }
            return JsonResponse(resultdict, safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': '编辑失败',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)



def userDelete(request):
    User = get_user_model()
    if request.method == "POST":
        u = json.loads(request.body)
        # u = request.body
        id=u.get('id')
        User.objects.filter(id=id).delete()
        resultdict = {
            'code': 0,
            'msg': 'success',
            'data': {'id': id}
        }
        return JsonResponse(resultdict,safe=False)
    else:
        resultdict = {
            'code': 1,
            'msg': 'fail',
            'data': {}
        }
        return JsonResponse(resultdict, safe=False)



def searchUser(request):
    keywords= request.GET.get('keyword')
    print keywords
    User=get_user_model()
    result= User.objects.filter(username__icontains=keywords)
    print result
    return render(request, 'main/user.html', {'keyword': keywords, 'result_list': result})

def loginout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def page_not_found(request):
    return render(request, 'main/404.html')


def page_error(request):
    return render(request, 'main/500.html')


def permission_denied(request):
    return render(request, 'main/403.html')

# def convert_to_dict(obj):
#     dict = {}
#     for i in obj:
#         dic = {}
#         dic.update(i.__dic__)
#         dict.append(dic)
#     return dict
#

