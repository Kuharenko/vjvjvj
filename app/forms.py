from django import forms
from django.contrib.auth.models import User


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
