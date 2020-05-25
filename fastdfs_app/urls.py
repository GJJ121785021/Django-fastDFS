from django.urls import path

from fastdfs_app import views

app_name = 'fdfs_app'

urlpatterns = [
    path('index/', views.index),
    path('delete/', views.delete),
    path('get/', views.get),
]


