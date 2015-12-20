from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext,loader
from .models import Question,Choice
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def index(request):
     # return HttpResponse("Hello,world.You're at the polls index.")

    # latest_question_list=Question.objects.order_by('-pub_date')[:5]
    # output=','.join(q.quesiont_text for q in latest_question_list)
    # return HttpResponse(output)

    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    # template=loader.get_template('polls/index.html')
    # context=RequestContext(request,{'latest_question_list':latest_question_list,
    #                                  })
    # return HttpResponse(template.render(context))
    context={'latest_question_list':latest_question_list}
    return render(request,'polls/index.html',context)


def detail(request,question_id):
    # return HttpResponse("You're looking at question %s." % question_id)
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/detail.html',{'question':question})

def results(request,question_id):
    # response="You're looking at the result of quesiont %s."
    # return  HttpResponse(response%question_id)
    question=get_object_or_404(Question,pk=question_id)
    return render(request,'polls/results.html',{'question':question})

def vote(request,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'question':question,
            'error_message':'You did not select a choice',
        })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))

    return HttpResponse("You're voting on quesiont %s." % question_id)