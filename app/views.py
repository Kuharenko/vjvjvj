from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate

from app.forms import *
from app.models import *

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from django_facebook.models import FacebookProfile
from open_facebook import OpenFacebook
from django_facebook.decorators import facebook_required
from django.contrib import messages
from django_facebook.utils import next_redirect
from django_facebook.api import get_persistent_graph
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


def home(request):
    quests = Quests.objects.all()
    return render(request, 'home.html', {'quests': quests})


def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def log_in(request):
    if not request.user.is_authenticated():
        form = LogInForm(request.POST or None)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                return render(request, 'login.html', {'form': form, 'incorrect': True})
        return render(request, 'login.html', {'form': form})
    return HttpResponseRedirect('/')


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


@facebook_required(scope='publish_actions,user_photos')
def send_post(request):
    if request.POST:
        user = FacebookProfile.objects.get(user_id=request.user.id)
        access_token = user.access_token

        facebook = OpenFacebook(access_token)
       # facebook.get('me') # info about me

        message = request.POST.get('post_text')
        #facebook.set('me/feed', message=message, picture='http://neutr10.com/wp-content/uploads/2016/02/python-snake.jpg') # posted message for me

        photo_urls = [
            'http://neutr10.com/wp-content/uploads/2016/02/python-snake.jpg',
            'http://neutr10.com/wp-content/uploads/2016/02/python-snake.jpg',
        ]
        for photo in photo_urls:
            print facebook.set('me/feed', message=message,
                               picture=photo, url='http://www.me.com', link=photo, caption="")

        return render(request, 'send_post.html', {'message':'Success'})
    return render(request, 'send_post.html')


@facebook_required(scope='publish_stream,user_photos')
def image_upload(request):
    fb = get_persistent_graph(request)
    print request
    if request.FILES:
        print "123"
        pictures = request.POST.getlist('images')
        print pictures
        for picture in pictures:
            fb.set('me/photos', url="http://asdasd.asd", message='the writing is one The '
                                                     'wall image %s' % picture)

        messages.info(request, 'The images have been added to your profile!')

        return next_redirect(request)
    return render(request, 'send_images.html')


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def adminka(request):
    quests = Quests.objects.all()
    tasks = Tasks.objects.all()

    return render(request, 'adminka.html', {'quests': quests, 'tasks': tasks})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_quest(request):
    form = CreateQuestForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_tasks(request):
    form = CreateTaskForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_tasks_category(request):
    form = CreateTaskCategoryForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def delete_task(request, id):
    Tasks.objects.get(id=id).delete()
    return redirect('/adminka/')


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def delete_quest(request, id):
    Quests.objects.get(id=id).delete()
    return redirect('/adminka/')


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def delete_category(request, id):
    TaskCategory.objects.get(id=id).delete()
    return redirect('/adminka/')


def view_quest(request, id):
    quest = Quests.objects.get(pk=id)
    return render(request, 'view_quest.html', {'quest': quest})


def view_task(request, id):
    task = Tasks.objects.get(pk=id)
    return render(request, 'view_quest.html', {'task': task})







