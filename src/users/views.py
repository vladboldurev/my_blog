from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView, DeleteView
from .forms import MyBlogUserCreationForm, MyBlogUserChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib import messages

from .utilities import signer


class RegisterUserView(CreateView):

    form_class = MyBlogUserCreationForm
    model = get_user_model()
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'


class RegisterActivateView(TemplateView):

    def get(self, request, *args, **kwargs):
        sign = kwargs.get('sign')

        try:
            email = signer.unsign(sign)
        except BadSignature:
            return render(request, 'registration/bad_signature.html')

        user = get_object_or_404(get_user_model(), email=email)

        if user.is_activated:
            template = 'registration/user_is_activated.html'
        else:
            template = 'registration/activation_done.html'
            user.is_activated = True
            user.is_active = True
            user.save()

        return render(request, template)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):

    model = get_user_model()
    template_name = 'users/change_user_info.html'
    form_class = MyBlogUserChangeForm
    succes_url = reverse_lazy('home')
    success_message = 'Личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserProfile(LoginRequiredMixin, DetailView):

    model = get_user_model()
    template_name = 'users/profile.html'
    login_url = 'account_login'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)



