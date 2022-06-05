"""property URL Configuration

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
from django.urls import path, include
from good import good_url
from pay import pay_url
from logistics import logistics_url
from account import account_url
from proprietor import proprietor_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('good/', include(good_url)),
    path('pay/', include(pay_url)),
    path('logistics/', include(logistics_url)),
    path('account/', include(account_url)),
    path('proprietor/', include(proprietor_url)),
]
