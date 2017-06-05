from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, render_to_response, RequestContext
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt


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
    if request.user.is_authenticated():
        completed = ResultQuestByUser.objects.filter(user=User.objects.get(id=request.user.id)).all()
        return render(request, 'home.html', {'quests': quests, 'completed': completed})
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


@csrf_exempt
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
def edit_image_task(request, id):
    task = TaskUploadImage.objects.get(pk=id)
    form = CreateTaskImageForm(instance=task)
    if request.POST:
        form = CreateTaskImageForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def edit_choice_task(request, id):
    task = TaskChoiceRightVariant.objects.get(pk=id)
    form = CreateTaskChoiceForm(instance=task)
    if request.POST:
        form = CreateTaskChoiceForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            return render(request, 'create_quest.html', {'form': form, 'message': 'Succes'})
    return render(request, 'create_quest.html', {'form': form, 'message': ''})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def edit_checkin_task(request, id):
    task = TaskCheckIn.objects.get(pk=id)
    form = CreateTaskCheckInForm(instance=task)
    if request.POST:
        form = CreateTaskCheckInForm(request.POST, request.FILES, instance=task)
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


def view_task_choice(request, id, q_id):
    task = TaskChoiceRightVariant.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    quest = Quests.objects.get(id=q_id)
    try:
        accepted = ResultForUserChoicesTask.objects.get(task_id=task, user=user)
    except:
        accepted = ''
    return render(request, 'view_task.html', {'task': task, 'accepted': accepted, 'quest': quest})


def view_task_checkin(request, id, q_id):
    task = TaskCheckIn.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    quest = Quests.objects.get(id=q_id)
    try:
        accepted = ResultForUserCheckinTask.objects.get(task_id=task, user=user)
    except:
        accepted = ''
    return render(request, 'view_task.html', {'task': task, 'accepted': accepted, 'quest': quest})


def view_task_image(request, id, q_id):
    task = TaskUploadImage.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    quest = Quests.objects.get(id=q_id)
    try:
        accepted = ResultForUserImageTask.objects.get(task_id=task, user=user)
    except:
        accepted = ''
    return render(request, 'view_task.html', {'task': task, 'accepted': accepted, 'quest': quest})


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


@login_required()
def start_task(request, task_id, task_type, q_id):
    quest = Quests.objects.get(id=q_id)
    user = User.objects.get(id=request.user.id)
    if not ResultQuestByUser.objects.filter(quest=quest, user=user).exists():
        rs = ResultQuestByUser(quest=quest, user=user, status='0')
        rs.save()

    if '0' in task_type:
        id = TaskUploadImage.objects.get(id=task_id)
        if not ResultForUserImageTask.objects.filter(task_id=id, quest=quest, user=user).exists():
            task = ResultForUserImageTask(task_id=id, user=user, quest=quest, user_answer='', status='0')
            task.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    elif '1' in task_type:
        id = TaskCheckIn.objects.get(id=task_id)
        if not ResultForUserCheckinTask.objects.filter(task_id=id,quest=quest, user=user).exists():
            task = ResultForUserCheckinTask(task_id=id, user=user,quest=quest, user_answer='', status='0')
            task.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    else:
        id = TaskChoiceRightVariant.objects.get(id=task_id)
        if not ResultForUserChoicesTask.objects.filter(task_id=id,quest=quest, user=user).exists():
            task = ResultForUserChoicesTask(task_id=id, quest=quest, user=user, user_answer='', status='0')
            task.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)


@login_required()
def finish_task(request, task_id, task_type, q_id):
    user = User.objects.get(id=request.user.id)
    quest = Quests.objects.get(id=q_id)

    def z(quest, user):
        choises = quest.tasks_choice.all().count()
        images = quest.tasks_image.all().count()
        checkin = quest.tasks_checkin.all().count()

        u_choises = ResultForUserChoicesTask.objects.filter(quest=quest, user=user).count()
        u_images = ResultForUserImageTask.objects.filter(quest=quest, user=user).count()
        u_checkin = ResultForUserCheckinTask.objects.filter(quest=quest, user=user).count()

        tasks_in_quest = choises + images + checkin
        tasks_in_user_by_quest = u_choises+u_images+u_checkin

        if tasks_in_quest == tasks_in_user_by_quest:
                quest_by_user = ResultQuestByUser.objects.get(user=user, quest=quest)
                quest_by_user.status ='1'
                quest_by_user.save()

    if '0' in task_type:
        id = TaskUploadImage.objects.get(id=task_id)
        if request.POST and request.FILES:
            task = ResultForUserImageTask.objects.get(task_id=id, user=user)
            task.user_answer = request.FILES.get('img')
            task.status ='1'
            task.save()
            z(quest, user)
            return redirect('/')
    elif '1' in task_type:
        id = TaskCheckIn.objects.get(id=task_id)
        if request.POST:
            task = ResultForUserCheckinTask.objects.get(task_id=id, user=user)
            task.user_location = request.POST.get('location')
            task.status ='1'
            task.save()
            z(quest, user)
            return redirect('/')
    else:
        id = TaskChoiceRightVariant.objects.get(id=task_id)
        right_variant = id.task_variant_right
        if request.POST:
            if right_variant == request.POST.get('choice'):
                task = ResultForUserChoicesTask.objects.get(task_id=id, user=user)
                task.status = '1'
                task.user_answer = request.POST.get('choice')
                task.save()
                z(quest, user)
                return redirect('/')
    return HttpResponse(status=400)

