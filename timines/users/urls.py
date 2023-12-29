from django.urls import path 
from . import views
from django.contrib import admin

urlpatterns = [
    path("",views.home,name='homepage'),
    path("register/",views.RegisterView.as_view(),name="users-register"),
    path("profile/",views.profile,name="users-profile"),
    path("profile_overview/",views.profile_overview,name="users-profile_overview"),
    path("commander/",views.commander,name="users-commander"),
    path("info/",views.info,name="user-info"),
    path("planning/",views.planning,name="user-planning"),
    path("notification/",views.notification,name='user-notification')
]