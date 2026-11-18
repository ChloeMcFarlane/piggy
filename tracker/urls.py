from django.contrib import admin
from django.urls import path
from . import views
from tracker import views


urlpatterns = [
    path("", views.index, name='index'),
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
]
