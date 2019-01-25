# -*- coding: utf-8 -*-
from django.shortcuts import render
from bugStatistics.models import ZtBug,ZtProduct,ZtUser
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from bugStatistics.models import ZtBug
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import unicodedata
import json



def statistics(request):
    return render(request, 'bugStatistics/projectStatistics.html')

def pbList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    pname = request.GET.get('keyword')
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    pb=[]
    resultdict = {}
    q1 = Q()
    q1.connector = 'AND'
    q1.children.append(('deleted', 0))
    if len(pname)>2:
        pbList = json.loads(pname)
        for a in pbList:
            name = a.get('name')
            pb.append(name)
        q1.children.append(('name__in', pb))
    p = ZtProduct.objects.using('chandao').filter(q1).order_by('-createddate')
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['projectId'] = a.id
        dic['projectName'] = a.name
        q2 = Q()
        q2.connector = 'AND'
        q2.children.append(('product', a.id))
        if date1 and date2 == '':
            q2.children.append(('openeddate__gte', date1))
        if date1 == '' and date2:
            q2.children.append(('openeddate__lte', date2))
        if date1 and date2:
            # q2.children.append(('openeddate__range', (date1, date2)))
            q2.children.append(('openeddate__gte', date1))
            q2.children.append(('openeddate__lte', date2))
        bugs = ZtBug.objects.using('chandao').filter(q2).count()
        bugs1 = ZtBug.objects.using('chandao').filter(q2, Q(severity=1)).count()
        bugs2 = ZtBug.objects.using('chandao').filter(q2, Q(severity=2)).count()
        bugs3 = ZtBug.objects.using('chandao').filter(q2, Q(severity=3)).count()
        bugs4 = ZtBug.objects.using('chandao').filter(q2, Q(severity=4)).count()
        dic['bugs'] = bugs
        dic['bugs1'] = bugs1
        dic['bugs2'] = bugs2
        dic['bugs3'] = bugs3
        dic['bugs4'] = bugs4
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


def testerStatistics(request):
    return render(request, 'bugStatistics/testerStatistics.html')

#测试人员bug统计
def testerList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    pname = request.GET.get('keyword')
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    resultdict = {}
    q1 = Q()
    q1.connector = 'AND'
    q1.children.append(('deleted', 0))
    q1.children.append(('role', 'qa'))
    if pname:
        q1.children.append(('realname', pname))
    p = ZtUser.objects.using('chandao').filter(q1)
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['userId'] = a.id
        dic['realName'] = a.realname
        dic['account'] = a.account
        q2 = Q()
        q2.connector = 'AND'
        q2.children.append(('openedby', a.account))
        if date1 and date2 == '':
            q2.children.append(('openeddate__gte', date1))
        if date1 == '' and date2:
            q2.children.append(('openeddate__lte', date2))
        if date1 and date2:
            # q2.children.append(('openeddate__range', (date1, date2)))
            q2.children.append(('openeddate__gte', date1))
            q2.children.append(('openeddate__lte', date2))
        bugs = ZtBug.objects.using('chandao').filter(q2).count()
        bugs1 = ZtBug.objects.using('chandao').filter(q2, Q(severity=1)).count()
        bugs2 = ZtBug.objects.using('chandao').filter(q2, Q(severity=2)).count()
        bugs3 = ZtBug.objects.using('chandao').filter(q2, Q(severity=3)).count()
        bugs4 = ZtBug.objects.using('chandao').filter(q2, Q(severity=4)).count()
        dic['bugs'] = bugs
        dic['bugs1'] = bugs1
        dic['bugs2'] = bugs2
        dic['bugs3'] = bugs3
        dic['bugs4'] = bugs4
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


def devStatistics(request):
    return render(request, 'bugStatistics/devStatistics.html')

def devList(request):
    page = request.GET.get('page', '1')
    rows = request.GET.get('limit', '10')
    i = (int(page) - 1) * int(rows)
    j = (int(page) - 1) * int(rows) + int(rows)
    # keyword = request.GET.get('keyword')
    date1 = request.GET.get('date1')
    date2 = request.GET.get('date2')
    pname = request.GET.get('pname')
    resultdict = {}
    q1 = Q()
    q1.connector = 'AND'
    q1.children.append(('deleted', 0))
    q1.children.append(('role__in', ['dev', 'others']))
    # pb = pname.encode('unicode-escape').decode('string_escape')
    # pbList = eval(pb)
    if len(pname) >2:
        pb = []
        pbList = json.loads(pname)
        for a in pbList:
            name = a.get('name')
            pb.append(name)
        q1.children.append(('realname__in', pb))
    # if keyword:
    #     q1.children.append(('realname', keyword))
    p = ZtUser.objects.using('chandao').filter(q1).order_by('role')
    total = p.count()
    p = p[i:j]
    dict = []
    for a in p:
        dic = {}
        dic['userId'] = a.id
        dic['realName'] = a.realname
        dic['account'] = a.account
        q2 = Q()
        q2.connector = 'AND'
        if date1 and date2 == '':
            q2.children.append(('openeddate__gte', date1))
        if date1 == '' and date2:
            q2.children.append(('openeddate__lte', date2))
        if date1 and date2:
            # q2.children.append(('openeddate__range', (date1, date2)))
            q2.children.append(('openeddate__gte', date1))
            q2.children.append(('openeddate__lte', date2))
        q2.children.append(('resolvedby', a.account))
        bugs = ZtBug.objects.using('chandao').filter(q2).count()
        bugs1 = ZtBug.objects.using('chandao').filter(q2, Q(severity=1)).count()
        bugs2 = ZtBug.objects.using('chandao').filter(q2, Q(severity=2)).count()
        bugs3 = ZtBug.objects.using('chandao').filter(q2, Q(severity=3)).count()
        bugs4 = ZtBug.objects.using('chandao').filter(q2, Q(severity=4)).count()
        dic['bugs'] = bugs
        dic['bugs1'] = bugs1
        dic['bugs2'] = bugs2
        dic['bugs3'] = bugs3
        dic['bugs4'] = bugs4
        dict.append(dic)
    resultdict['code'] = 0
    resultdict['msg'] = ''
    resultdict['count'] = total
    resultdict['data'] = dict
    return JsonResponse(resultdict, safe=False)


@login_required
def bugProjectName(request):
    p = ZtProduct.objects.filter(deleted=0).order_by('-createddate')
    dict=[]
    for a in p:
        dic={}
        dic['projectName'] = a.name
        dic['id'] = a.id
        dict.append(dic)
    return JsonResponse(dict, safe=False)

@login_required
def bugDevName(request):
    p = ZtUser.objects.filter(deleted=0, role__in=['dev', 'others']).order_by('-id')
    dict=[]
    for a in p:
        dic={}
        dic['devame'] = a.realname
        dic['account'] = a.account
        dic['id'] = a.id
        dict.append(dic)
    return JsonResponse(dict, safe=False)







