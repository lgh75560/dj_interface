"""myinterface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url  # 这行
from iface import views

urlpatterns = [
    path('index/', views.testview),
    path('add_header/', views.go_add_header),
    path('save_header/', views.save_header),
    path('get_header/', views.get_headers),

    path('add_suit/', views.go_add_suit),
    path('save_suit/', views.save_suit),
    path('get_suit/', views.get_suit),

    path('add_test/', views.go_add_test),
    path('get_test/', views.get_test),
    path('save_test/', views.save_test),
    path('test_test/', views.test_test),

    path('go_run/', views.go_run),
    path('add_run/', views.add_run),
    path('get_run/', views.get_run),

    path('run_result/', views.run_result),
    path('get_test_result/', views.get_test_result),
    url(r'^$', views.root),
]
