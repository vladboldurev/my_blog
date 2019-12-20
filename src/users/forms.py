from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import user_registrated


class MyBlogUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             label='E-mail')

    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(label='Password (repeat)',
                                widget=forms.PasswordInput,
                                help_text='re-enter password')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                       'entered passwords do not match'
                     )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(MyBlogUserCreationForm, instance=user)
        return user



    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('email', 'password1', 'password2',
                  'send_messages')


class MyBlogUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True,
                             label='E-mail')

    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'send_messages')

