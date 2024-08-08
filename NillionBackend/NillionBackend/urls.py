"""
URL configuration for NillionBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from base.views import *
from base.Router.profile import *
from base.Router.chat import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store-program', store_program_view, name='store-program'),
]

profiles = [
    path('create/', create_profile, name='create_profile'),
    path('all/', get_all_profiles, name='get_all_profiles'),
    path('address/<str:address>/', get_profile_by_address, name='get_profile_by_address'),
    path('match/<str:address>/', get_matching_profiles, name='get_matching_profiles'),
]

chat = [
    path('create_chat/', create_chat, name='create_chat'),
    path('send_message/', send_message, name='send_message'),
]
urlpatterns+=profiles
urlpatterns+=chat
