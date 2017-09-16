"""S17Day20 URL Configuration

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
from hostmanager import views
urlpatterns = [
    url(r'^index.html',views.Index.as_view()),
    url(r'^manager.html',views.Manager.as_view()),
    url(r'^addhost.html',views.AddHost.as_view()),
    url(r'^business.html',views.BusinessManager.as_view()),
    url(r'^addbusiness.html',views.AddBusiness.as_view()),
    url(r'^userlist.html',views.UserInfo.as_view()),
    url(r'^adduser.html',views.AddUser.as_view()),
    url(r'^delhost.html',views.DelHost.as_view()),
    url(r'^modifyhost.html',views.ModifyHost.as_view()),
]
