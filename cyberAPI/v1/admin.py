from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile


class ProfileInline(admin.TabularInline):
	model = Profile
	readonly_fields = ('balance', 'donate')


class UserAdmin(UserAdmin):
	inlines = (ProfileInline, )


admin.site.site_header = _('Cyber Administration')
admin.site.index_title = _('Cyber Administration')
admin.site.site_title = _('Cyber API')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
