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
from itertools import chain


def home(request):
    quests = Quests.objects.all()
    if request.user.is_authenticated():
        completed = ResultQuestByUser.objects.filter(user=User.objects.get(id=request.user.id), status='1').all()
        completed_list = []
        for q in completed:
            completed_list.append(q.quest.id)
        quests = Quests.objects.filter().all().exclude(id__in=completed_list)
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
        # facebook.set('me/feed', message=message, picture='http://neutr10.com/wp-content/uploads/2016/02/python-snake.jpg') # posted message for me

        photo_urls = [
            'http://neutr10.com/wp-content/uploads/2016/02/python-snake.jpg',
            'http://neutr10.com/wp-content/uploads/2016/02/python-snake.jpg',
        ]
        for photo in photo_urls:
            print facebook.set('me/feed', message=message,
                               picture=photo, url='http://www.me.com', link=photo, caption="")

        return render(request, 'send_post.html', {'message': 'Success'})
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
    result_list = list(chain(tasks_upload, tasks_checkin, tasks_choice))
    return render(request, 'adminka.html', {'quests': quests, 'result': result_list})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def create_quest(request, id=None):
    form = CreateQuestForm(request.POST or None, request.FILES or None)
    if id is not None:
        quest = Quests.objects.get(id=id)
        form = CreateQuestForm(instance=quest)

    if request.POST:
        if id is not None:
            form = CreateQuestForm(request.POST, request.FILES, instance=quest)
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
def edit_task(request, id=None, task_type=None):
    task = None
    if id is not None:
        if '0' in task_type:
            task = TaskUploadImage.objects.get(pk=id)
            form = CreateTaskImageForm(instance=task)
        elif '1' in task_type:
            task = TaskCheckIn.objects.get(pk=id)
            form = CreateTaskCheckInForm(instance=task)
        else:
            task = TaskChoiceRightVariant.objects.get(pk=id)
            form = CreateTaskChoiceForm(instance=task)
    else:
        if '0' in task_type:
            form = CreateTaskImageForm(request.POST or None, request.FILES or None)
        elif '1' in task_type:
            form = CreateTaskCheckInForm(request.POST or None, request.FILES or None)
        else:
            form = CreateTaskChoiceForm(request.POST or None, request.FILES or None)

    if request.POST:
        if '0' in task_type:
            form = CreateTaskImageForm(request.POST or None, request.FILES or None, instance=task or None)
        elif '1' in task_type:
            form = CreateTaskCheckInForm(request.POST or None, request.FILES or None, instance=task or None)
        else:
            form = CreateTaskChoiceForm(request.POST or None, request.FILES or None, instance=task or None)

        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
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
    user = User.objects.get(id=request.user.id)

    if ResultForUserImageTask.objects.filter(quest=quest, user=user).exists():
        accepted1 = ResultForUserImageTask.objects.get(quest=quest, user=user)
    else:
        accepted1 = ''
    if ResultForUserCheckinTask.objects.filter(quest=quest, user=user).exists():
        accepted2 = ResultForUserCheckinTask.objects.get(quest=quest, user=user)
    else:
        accepted2 = ''
    if ResultForUserChoicesTask.objects.filter(quest=quest, user=user).exists():
        accepted3 = ResultForUserChoicesTask.objects.get(quest=quest, user=user)
    else:
        accepted3 = ''

    return render(request, 'view_quest.html',
                  {'quest': quest, 'accepted1': accepted1, 'accepted2': accepted2, 'accepted3': accepted3})


def view_task(request, id, task_type, q_id):
    if '0' in task_type:
        task = TaskUploadImage.objects.get(id=id)
    elif '1' in task_type:
        task = TaskCheckIn.objects.get(id=id)
    else:
        task = TaskChoiceRightVariant.objects.get(id=id)

    user = User.objects.get(id=request.user.id)
    quest = Quests.objects.get(id=q_id)

    try:
        if '0' in task_type:
            accepted = ResultForUserImageTask.objects.get(task_id=task, user=user, quest=quest)
        elif '1' in task_type:
            accepted = ResultForUserCheckinTask.objects.get(task_id=task, user=user, quest=quest)
        else:
            accepted = ResultForUserChoicesTask.objects.get(task_id=task, user=user, quest=quest)
    except:
        accepted = ''
    return render(request, 'view_task.html', {'task': task, 'accepted': accepted, 'quest': quest})


@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def delete_task(request, id, task_type):
    if '0' in task_type:
        TaskUploadImage.objects.get(id=id).delete()
    elif '1' in task_type:
        TaskCheckIn.objects.get(id=id).delete()
    else:
        TaskChoiceRightVariant.objects.get(id=id).delete()
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
        if not ResultForUserCheckinTask.objects.filter(task_id=id, quest=quest, user=user).exists():
            task = ResultForUserCheckinTask(task_id=id, user=user, quest=quest, user_answer='', status='0')
            task.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    else:
        id = TaskChoiceRightVariant.objects.get(id=task_id)
        if not ResultForUserChoicesTask.objects.filter(task_id=id, quest=quest, user=user).exists():
            task = ResultForUserChoicesTask(task_id=id, quest=quest, user=user, user_answer='', status='0')
            task.save()
            return HttpResponse(status=200)
    return HttpResponse(status=400)


@login_required()
def finish_task(request, task_id, task_type, q_id):
    user = User.objects.get(id=request.user.id)
    quest = Quests.objects.get(id=q_id)

    if '0' in task_type:
        id = TaskUploadImage.objects.get(id=task_id)
        if request.POST and request.FILES:
            task = ResultForUserImageTask.objects.get(task_id=id, user=user, quest=quest)
            task.user_answer = request.FILES.get('img')
            task.status = '2'
            task.save()
            if not ImageTaskModerate.objects.filter(quest=quest, task=id, user=user).exists():
                moderate = ImageTaskModerate(quest=quest, task=id, user=user, user_answer=request.FILES.get('img'))
                moderate.save()
            else:
                moderate = ImageTaskModerate.objects.get(quest=quest, task=id, user=user)
                moderate.user_answer = request.FILES.get('img')
                moderate.save()
            return redirect('/quest/' + q_id)
    elif '1' in task_type:
        id = TaskCheckIn.objects.get(id=task_id)
        right_variant = id.task_location

        locationX = float((right_variant.split(',')[0]).strip(' '))
        locationY = float((right_variant.split(',')[1]).strip(' '))
        import math
        precision = 0.0002

        if request.POST:
            task = ResultForUserCheckinTask.objects.get(task_id=id, user=user, quest=quest)
            task.user_answer = request.POST.get('location')

            userlocationX = float((request.POST.get('location').split(',')[0]).strip(' '))
            userlocationY = float((request.POST.get('location').split(',')[1]).strip(' '))

            r_xy = math.sqrt((locationX-userlocationX) ** 2 + (locationY-userlocationY) ** 2)
            if float(r_xy) <= precision:
                task.status = '1'
            else:
                task.status = '0'
            task.save()
            return redirect('/quest/' + q_id)
    else:
        id = TaskChoiceRightVariant.objects.get(id=task_id)
        right_variant = id.task_variant_right
        if request.POST:

            task = ResultForUserChoicesTask.objects.get(task_id=id, user=user, quest=quest)
            if right_variant == request.POST.get('choice'):
                task.status = '1'
            else:
                task.status = '0'
            task.user_answer = request.POST.get('choice')
            task.save()
            return redirect('/quest/' + q_id)
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('/quest/' + q_id)


def finish_quest(request, q_id):
    try:
        result = ResultQuestByUser.objects.get(quest=Quests.objects.get(id=q_id), user=request.user.id)
    except:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user = User.objects.get(id=request.user.id)
    quest = Quests.objects.get(id=q_id)

    choises = quest.tasks_choice.all().count()
    images = quest.tasks_image.all().count()
    checkin = quest.tasks_checkin.all().count()

    u_choises = ResultForUserChoicesTask.objects.filter(quest=quest, user=user, status='1').count()
    u_images = ResultForUserImageTask.objects.filter(quest=quest, user=user, status='1').count()
    u_checkin = ResultForUserCheckinTask.objects.filter(quest=quest, user=user, status='1').count()

    tasks_in_quest = choises + images + checkin
    tasks_in_user_by_quest = u_choises + u_images + u_checkin
    print tasks_in_quest
    print  tasks_in_user_by_quest
    if tasks_in_quest == tasks_in_user_by_quest:
        result.status = '1'
        result.save()
    else:
        result.status = '0'
        result.save()

    return redirect('/')


def ImageModerate(request):
    data = ImageTaskModerate.objects.all()
    return render(request, 'moderate.html', {'data': data})


def image_accept(request, q_id, task_id, user_id):
    task = ResultForUserImageTask.objects.get(quest=Quests.objects.get(id=q_id),
                                              task_id=TaskUploadImage.objects.get(id=task_id),
                                              user=User.objects.get(id=user_id))
    task.status = '1'
    task.save()

    ImageTaskModerate.objects.get(quest=Quests.objects.get(id=q_id),
                                  task=TaskUploadImage.objects.get(id=task_id),
                                              user=User.objects.get(id=user_id)).delete()
    return HttpResponse(200)


def image_decline(request, q_id, task_id, user_id):
    task = ResultForUserImageTask.objects.get(quest=Quests.objects.get(id=q_id),
                                              task_id=TaskUploadImage.objects.get(id=task_id),
                                              user=User.objects.get(id=user_id))
    task.user_answer = ''
    task.status = '0'
    task.save()

    ImageTaskModerate.objects.get(quest=Quests.objects.get(id=q_id),
                                  task=TaskUploadImage.objects.get(id=task_id),
                                  user=User.objects.get(id=user_id)).delete()
    return redirect('/')