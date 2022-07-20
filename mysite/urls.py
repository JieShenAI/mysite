"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from app.views import ccgp, account, sql, data

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', ccgp.index),
    # path('data/', views.data),
    path('ccgp/add/', ccgp.ccgp_add),
    path('ccgp/list/', ccgp.ccgp_list),

    # 用户管理
    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),
    path('user/register/', account.register),

    # 数据展示
    path('data/test/', sql.my_custom_sql),
    path('data/nianjian/', data.nianjian)
]
