# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django_web.models import Case, taskResult

admin.site.register(Case)
admin.site.register(taskResult)