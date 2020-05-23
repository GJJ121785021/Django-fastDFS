from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, Http404
from .models import Question, Choice
from django.views import generic

from django.contrib import messages

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        messages.info(self.request, 'This is a message')
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        if self.request.headers.get('Referer'):
            context['refer'] = self.request.headers.get('Referer')
        return context


    # def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     refer = request.META.get('HTTP_REFERER')
#     context = dict()
#     context['refer'] = refer
#     context['question'] = question
#     return render(request, 'polls/detail.html', context)


def vote(request, question_id):
    if request.POST:
        try:
            choice = Choice.objects.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            raise Http404('请至少选择一项')
        return HttpResponse('你选择了{}'.format(choice.choice_text))
    question = get_object_or_404(Question, pk=question_id)
    context = dict()
    error_message = '没有错误'
    context['question'] = question
    context['error_message'] = error_message
    return render(request, 'polls/vote.html', context)
