"""analytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path
from java_developer_analytic import views


urlpatterns = [
    re_path(r'^demand', views.demand),
    re_path('^geography', views.geography),
    re_path('^skills', views.skills),
    re_path('^latest_vacancies', views.latest_vacancies),
    re_path('^description', views.index),
    path(r'admin/', admin.site.urls),
    # path(r'get_vacancies', views.get_vacancies, name='get_vacancies'),
    path('', views.index),
]
