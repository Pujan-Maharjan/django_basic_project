from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Question, Choice
from .forms import ProfileForm, UploadFile, RegisterForm


# Create your views here.
def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']
            user = User.objects.create_user(username, '', raw_password)
            user.save()
            
            return HttpResponseRedirect(reverse('polls:register'))

    else:
        form = RegisterForm()
        return render(request, 'polls/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('polls:index'))
            else:
                return HttpResponse("Sorry enter correct credentials")
                

    else:
        form = RegisterForm()
        return render(request, 'polls/login.html', {'form': form})
        
           




def get_profile(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProfileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProfileForm()
        return render(request, 'polls/profile.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse("The file was successfully uploaded")
    else:
        form = UploadFile()
    return render(request, 'polls/upload.html', {'form': form})


def handle_uploaded_file(f):
    file_name = f.name
    with open(settings.MEDIA_ROOT+'/'+file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    

def landing_page(request):
    return render(request, 'polls/landing.html')
    

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]



class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        send_mail(
            'Voted successfully',
            'Thanks for your vote.',
            'sender@gmail.com',
            ['receiver@gmail.com'],
            fail_silently=False,
        )
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
