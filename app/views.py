from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from app.forms import *

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from django_facebook.models import FacebookProfile
from open_facebook import OpenFacebook


# Create your views here.


def home(request):
    return render(request, 'home.html')


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
                return redirect('/')
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
                               picture=photo, url='http://www.me.com', link=photo)

        return render(request, 'send_post.html', {'message':'Success'})
    return render(request, 'send_post.html')