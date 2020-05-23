from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import redirect, reverse, render
from django.views.decorators.http import require_http_methods
from django.views import View


def check_login(func):
    def warp(request, *args, **kwargs):
        if request.session.get('have_login', None):
            return func(request, *args, **kwargs)
        else:
            return HttpResponse('not login<br><a href="/add">点击登录</a>')
    return warp


@check_login
def index(request):
    return HttpResponse('have logined<br><a href="/del">退出登录</a>')

def add(request):
    request.session['have_login'] = '123'
    request.session.set_expiry(10)
    return redirect(reverse(index))


def dele(request):
    if request.session.__contains__('have_login'):
        del request.session['have_login']
    return HttpResponseRedirect('/')

def my_view(request, page_number=1):
    response = HttpResponse()
    response.write('111')
    response.write(response.charset)
    return response


@require_http_methods(['GET', 'POST'])
def upload_file(request):
    if request.method == 'GET':
        return render(request, 'polls/upload_file.html')
    else:
        file = request.FILES.get('file')
        with open('file111.docx', 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return HttpResponse('has post  '+file.name)


