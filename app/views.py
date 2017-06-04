from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

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


@login_required()
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
    tasks_upload = TaskUploadImage.objects.all()
    tasks_checkin = TaskCheckIn.objects.all()
    tasks_choice = TaskChoiceRightVariant.objects.all()

    return render(request, 'adminka.html', {'quests': quests, 'tasks1': tasks_upload,
                                            'tasks2':tasks_checkin, 'tasks3':tasks_choice })


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_quest(request):
    form = CreateQuestForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_choice_task(request):
    form = CreateTaskChoiceForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_checkin_task(request):
    form = CreateTaskCheckInForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_image_task(request):
    form = CreateTaskImageForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
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
def edit_quest(request, id):
    quest = Quests.objects.get(id=id)
    form = CreateQuestForm(instance=quest)
    if request.POST:
        form = CreateQuestForm(request.POST, request.FILES, instance=quest)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def edit_task(request, id, type):
    if type == 0:
        task = TaskUploadImage.objects.get(pk=id)
        form = CreateTaskImageForm(instance=task)
    elif type == 1:
        task = TaskCheckIn.objects.get(pk=id)
        form = CreateTaskCheckInForm(instance=task)
    else:
        task = TaskChoiceRightVariant.objects.get(pk=id)
        form = CreateTaskChoiceForm(instance=task)

    if request.POST:
        if type == 0:
            form = CreateTaskImageForm(request.POST, request.FILES, instance=task)
        elif type == 1:
            form = CreateTaskCheckInForm(request.POST, request.FILES, instance=task)
        else:
            form = CreateTaskChoiceForm(request.POST, request.FILES, instance=task)

        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            #form.save_m2m()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


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


def view_task_choice(request, id):
    task = TaskChoiceRightVariant.objects.get(id=id)
    print task
    return render(request, 'view_task.html', {'task': task})


def view_task_checkin(request, id):
    task = TaskCheckIn.objects.get(id=id)
    return render(request, 'view_task.html', {'task': task})


def view_task_image(request, id):
    task = TaskUploadImage.objects.get(id=id)
    return render(request, 'view_task.html', {'task': task})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def delete_task_image(request, id):
    TaskUploadImage.objects.get(pk=id).delete()
    return redirect('/adminka/')


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def delete_task_choice(request, id):
    TaskChoiceRightVariant.objects.get(pk=id).delete()
    return redirect('/adminka/')


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def delete_task_checkin(request, id):
    TaskCheckIn.objects.get(pk=id).delete()
    return redirect('/adminka/')