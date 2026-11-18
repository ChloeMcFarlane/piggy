from django.contrib import admin
from django.urls import path, include
from tracker import views

urlpatterns = [
    path('', include('tracker.urls')),
    path('transactions/', views.transactions_list, name='transactions-list'),
    path("admin/", admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('accounts/', include('allauth.urls')),
]
