"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app import views as my_views

urlpatterns = [
    url(r'^$', my_views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^logout/$', my_views.log_out, name='logout'),
    url(r'^register/$', my_views.RegisterFormView.as_view(), name='register'),
    url(r'^login/$', my_views.log_in, name='login'),
    url(r'^post/$', my_views.send_post, name='post'),
    url(r'^image_post/$', my_views.image_upload, name="images"),
    url(r'^adminka/$', my_views.adminka, name="adminka"),
    url(r'^adminka/create/quest/$', my_views.create_quest, name="create-quest"),
    #url(r'^adminka/create/task/(?P<task_type>[0-3])/$', my_views.create_task, name="create-task"),
    url(r'^adminka/create/category/$', my_views.create_tasks_category, name="create-category"),
    url(r'^adminka/delete/quest/(?P<id>[0-9]+)$', my_views.delete_quest, name="delete-quest"),
    url(r'^adminka/delete/category/(?P<id>[0-9]+)$', my_views.delete_category, name="delete-category"),
    url(r'^adminka/edit/task/(?P<id>[0-9]+)/(?P<type>[0-3])/$', my_views.edit_task, name="edit-task"),
    url(r'^adminka/edit/quest/(?P<id>[0-9]+)$', my_views.edit_quest, name="edit-quest"),
    url(r'quest/(?P<id>[0-9]+)$', my_views.view_quest, name='quest'),
    url(r'task/view/image/(?P<id>[0-9]+)/$', my_views.view_task_image, name='view-image-task'),
    url(r'task/view/choice/(?P<id>[0-9]+)/$', my_views.view_task_choice, name='view-choice-task'),
    url(r'task/view/checkin/(?P<id>[0-9]+)/$', my_views.view_task_checkin, name='view-checkin-task'),
    url(r'admin/delete/image/(?P<id>[0-9]+)/$', my_views.delete_task_image, name='delete-image-task'),
    url(r'admin/delete/choice/(?P<id>[0-9]+)/$', my_views.delete_task_choice, name='delete-choice-task'),
    url(r'admin/delete/checkin/(?P<id>[0-9]+)/$', my_views.delete_task_checkin, name='delete-checkin-task'),
    url(r'admin/create/checkin/$', my_views.create_checkin_task, name='create-checkin-task'),
    url(r'admin/create/choice/$', my_views.create_choice_task, name='create-choice-task'),
    url(r'admin/create/image/$', my_views.create_image_task, name='create-image-task')
]
