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
from bugStatistics.stViews import bugStView
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^statistics/$', bugStView.statistics, name='statistics'),
    url(r'^pbList/$', bugStView.pbList, name='pbList'),
    url(r'^testerStatistics/$', bugStView.testerStatistics, name='testerStatistics'),
    url(r'^testerList/$', bugStView.testerList, name='testerList'),
    url(r'^devStatistics/$', bugStView.devStatistics, name='devStatistics'),
    url(r'^devList/$', bugStView.devList, name='devList'),
    url(r'^bugProjectName/$', bugStView.bugProjectName, name='bugProjectName'),
    url(r'^bugDevName/$', bugStView.bugDevName, name='bugDevName'),

]