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

from django.urls import path
from django.conf.urls import url
from django.views.static import serve
from django.views.generic.base import TemplateView
from iface import views
from .settings import *


urlpatterns = [
    path('index/', views.testview),
    path('add_header/', views.go_add_header),
    path('save_header/', views.save_header),
    path('get_header/', views.get_headers),

    path('add_suit/', views.go_add_suit),
    path('save_suit/', views.save_suit),
    path('get_suit/', views.get_suit),

    path('add_test/', views.go_add_test),
    path('get_test/', views.get_test_list),
    path('update_test/', views.update_test),
    path('get_test_info/', views.get_test_from_info),
    path('save_test/', views.save_test),
    path('test_test/', views.test_test),

    path('go_run/', views.go_run),
    path('add_run/', views.add_run),
    path('get_run/', views.get_run),
    path('get_run_select/', views.get_run_select),
    path('get_run_report/', views.get_run_report),

    path('run_result/', views.run_result),
    path('get_test_result/', views.get_test_result),

    path('add_timer_job/', views.add_timer_job),
    path('get_timer_jobs/', views.get_timer_jobs),
    path('del_timer_jobs/', views.del_timer_jobs),

    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}, name='static'),

    path(r'', TemplateView.as_view(template_name='index.html')),  #####千万记住，别写东西，要不然只走后端，不走前端路由
]
