"""my_django URL Configuration

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
from django.urls import path, include, re_path
from django.conf.urls.static import static
from . import view
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mdeditor/', include('mdeditor.urls')),

    path('', view.index, name='index'),
    path('add/', view.add),
    path('del/', view.dele),
    path('polls/', include('polls.urls')),
    path('learnmodelapp/', include('learnmodelapp.urls')),
    re_path(r'^comments/(?:page-(?P<page_number>\d+))/$', view.my_view),
    path('upload_file/', view.upload_file, name='upload_file'),
    path('books/', include('books.urls')),
    path('vue/', include('vue_app.urls')),

]


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
