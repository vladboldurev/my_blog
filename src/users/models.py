from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import MyBlogUserManager
from django.contrib.auth.models import Group
from django.urls import reverse
from django.dispatch import Signal

from .utilities import send_activation_notification

class MyBlogUsers(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='is activated?')
    send_messages = models.BooleanField(default=True, verbose_name='send messages?')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyBlogUserManager()

    def save(self, *args, **kwargs):
        super(MyBlogUsers, self).save(*args, **kwargs)
        self.groups.add(Group.objects.get(name='user_group'))

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])

    def get_update_url(self):
        return reverse('change_user_info', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('delete_user', kwargs={'pk': self.id})

    def __str__(self):
        return self.email


user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)



