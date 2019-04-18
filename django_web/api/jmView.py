# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_web.models import Project
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def jm_index(request):
    return render(request, 'main/jm_index.html')