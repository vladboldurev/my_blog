from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
import datetime

from .utilities import send_activation_notification
from .forms import MyBlogUserChangeForm, MyBlogUserCreationForm


def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Mail sent')


send_activation_notifications.short_description = 'sending activation' + \
                                                  'notification emails'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Is activated?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return  (
                    ('activated', 'Прошли'),
                    ('threedays', 'Не прошли более 3 дней'),
                    ('week', 'Не прошли более недели')
                )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=1)
            return queryset.filter(is_active=False, is_activated=False,
                                   date_joined__date__lt=d)


class MyBlogUserAdmin(UserAdmin):
    add_form = MyBlogUserCreationForm
    form = MyBlogUserChangeForm
    model = get_user_model()
    list_display = ('__str__', 'email', 'is_activated', 'date_joined', 'is_staff', 'is_active')
    list_filter = (NonactivatedFilter,)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    actions = (send_activation_notifications,)

admin.site.register(get_user_model(), MyBlogUserAdmin)