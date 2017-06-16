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
    url(r'^adminka/quest/create/$', my_views.create_quest, name="create-quest"),
    url(r'^adminka/quest/(?P<id>[0-9]+)/edit/$', my_views.create_quest, name="edit-quest"),
    url(r'^adminka/create/category/$', my_views.create_tasks_category, name="create-category"),
    url(r'^adminka/delete/quest/(?P<id>[0-9]+)$', my_views.delete_quest, name="delete-quest"),
    url(r'^adminka/delete/category/(?P<id>[0-9]+)$', my_views.delete_category, name="delete-category"),
    url(r'^adminka/task/(?P<id>[0-9]+)/(?P<task_type>[0-3])/edit/$', my_views.edit_task, name="edit-task"),
    url(r'^quest/(?P<id>[0-9]+)$', my_views.view_quest, name='quest'),
    url(r'^task/(?P<id>[0-9]+)-(?P<task_type>[0-2])-(?P<q_id>[0-9]+)/$', my_views.view_task, name='view-task'),
    url(r'^start/(?P<task_id>[0-9]+)/(?P<task_type>[0-2])/(?P<q_id>[0-9]+)/$', my_views.start_task, name='start'),
    url(r'^finish/(?P<task_id>[0-9]+)/(?P<task_type>[0-2])/(?P<q_id>[0-9]+)/$', my_views.finish_task, name='finish'),
    url(r'^admin/task/(?P<id>[0-9]+)-(?P<task_type>[0-2])/delete/$', my_views.delete_task, name='delete-task'),
    url(r'^admin/task/(?P<task_type>[0-2])/create/$', my_views.edit_task, name='create-task'),
    url(r'^finish/quest/(?P<q_id>[0-9]+)/$', my_views.finish_quest, name='finish-quest'),
    url(r'^admin/moderate/$', my_views.ImageModerate, name='moderate'),
    url(r'^admin/moderate/accept/(?P<q_id>[0-9]+)-(?P<task_id>[0-9]+)-(?P<user_id>[0-9]+)/$', my_views.image_accept, name='accept'),
    url(r'^admin/moderate/decline/(?P<q_id>[0-9]+)-(?P<task_id>[0-9]+)-(?P<user_id>[0-9]+)/$', my_views.image_decline, name='decline')

]
