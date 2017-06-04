from django import forms
from django.contrib.auth.models import User
from models import *


class LogInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            user = User.objects.get(username=username)

            if not user.is_active:
                raise forms.ValidationError("User is inactive!")
            else:
                return username

        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password', 'username']


class CreateTaskCategoryForm(forms.ModelForm):
    class Meta:
        model = TaskCategory
        fields = ['category_name']


class CreateTaskImageForm(forms.ModelForm):
    class Meta:
        model = TaskUploadImage
        fields = ['task_name', 'task_description','task_question' ,'task_type', 'task_category', 'picture',
                  'user_image']


class CreateQuestForm(forms.ModelForm):
    class Meta:
        model = Quests
        fields = ['quest_name', 'tasks_checkin', 'tasks_choice','tasks_image','quest_description', 'picture',
                  'start_date', 'end_date']


class CreateTaskCheckInForm(forms.ModelForm):
    class Meta:
        model = TaskCheckIn
        fields = ['task_name', 'task_description','task_question' ,'task_type', 'task_category', 'picture',
                  'task_location']


class CreateTaskChoiceForm(forms.ModelForm):
    class Meta:
        model = TaskChoiceRightVariant
        fields = ['task_name', 'task_description','task_question',
                  'task_variant1', 'task_variant2', 'task_variant3', 'task_variant4', 'task_variant_right',
                  'task_type', 'task_category', 'picture']

















