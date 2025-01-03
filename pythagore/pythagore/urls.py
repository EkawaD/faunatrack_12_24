"""
URL configuration for pythagore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
import faunatrack.views as faunatrack_views
from django.urls import include, path

urlpatterns = [
    path("", faunatrack_views.bonjour, name="home"),
    path("admin/", admin.site.urls, name="admin_django_faunatrack"),
    path("accounts/", include("django.contrib.auth.urls"), name="auth"),
    path("faunatrack/", include('faunatrack.urls'), name="faunatrack" ),
    path('api/auth/', include('dj_rest_auth.urls')),
]
