"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from PTS.PTSViews import scriptManage,sceneManage,PTSreport

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # script
    url(r'^jm_index/$', scriptManage.jm_index, name='jm_index'),
    url(r'^scriptList/$', scriptManage.scriptList, name='scriptList'),
    url(r'^scriptAdd/$', scriptManage.scriptAdd, name='scriptAdd'),
    url(r'^uploadScript/$', scriptManage.uploadScript, name='uploadScript'),
    url(r'^scriptAddPost/$', scriptManage.scriptAddPost, name='scriptAddPost'),

    #scene
    url(r'^sceneAdd/$', sceneManage.sceneAdd, name='sceneAdd'),
    url(r'^sceneList/$', sceneManage.sceneList, name='sceneList'),

    #PTSreport
    url(r'^overView/$', PTSreport.overView, name='overView'),
    url(r'^report_index/$', PTSreport.report_index, name='report_index'),
    url(r'^report_samplerLog/$', PTSreport.report_samplerLog, name='report_samplerLog'),
    url(r'^samplerList/$', PTSreport.samplerList, name='samplerList'),
    url(r'^logDetail/$', PTSreport.logDetail, name='logDetail'),


]