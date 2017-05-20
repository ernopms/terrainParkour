"""terrain URL Configuration

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
from django.contrib import admin
from controllers import security
import controllers

urlpatterns = [
    url(r'^terrain/adminx/', admin.site.urls),
    url(r'terrain/$', security(controllers.test)),
    #gets
    url(r'terrain/user/(-?\d+)/', security(controllers.getRobloxUser)),
    
    #posts
    url(r'terrain/userJoined/(-?\d+)/',security(controllers.robloxUserJoined)),
    url(r'terrain/userLeft/(-?\d+)/',security(controllers.robloxUserLeft)),
    url(r'terrain/userFoundSign/(-?\d+)/(\d+)/',security(controllers.userFoundSign)),
    url(r'terrain/userFinishedRace/(-?\d+)/(\d+)/(\d+)/(\d+)', security(controllers.userFinishedRace)),
]
