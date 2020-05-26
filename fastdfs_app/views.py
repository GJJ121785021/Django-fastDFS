from django import forms
from django.http import HttpResponse
from django.shortcuts import render

from fastdfs_app.models import PersonalImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = PersonalImage
        fields = ['name', 'image']


def index(request):
    if request.method == 'GET':
        form = ImageForm()
        return render(request, 'index.html', {'form': form})
    else:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('fail')


def delete(request):
    image = PersonalImage.objects.first()
    image.image.delete()
    image.delete()
    return HttpResponse('deleted')


def get(request):
    image = PersonalImage.objects.first()
    return HttpResponse(f'url--------{image.image.url}')