from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *


class ProfileInline(admin.TabularInline):
	model = Profile


class UserAdmin(UserAdmin):
	inlines = (ProfileInline, )


class UserCharacterInline(admin.TabularInline):
	model = Profile.character.through
	extra = 1


class UserWeaponInline(admin.TabularInline):
	model = Profile.weapon.through
	extra = 1


# Don't use now, has a huge bug with user adding itself to friends
class UserFriendsInline(admin.TabularInline):
	model = Profile.friends.through
	fk_name = "friend"
	extra = 0


class ProfileAdmin(admin.ModelAdmin):
	inlines = (UserCharacterInline, UserWeaponInline)
	list_display = ('user', 'karma')
	list_display_links = ("user", )
	list_select_related = True
	ordering = ('-user__date_joined',)
	readonly_fields = ("client_settings_json", )
	search_fields = ("user__username",)
	empty_value_display = '-empty-'
	fieldsets = (
		(None, {
			'fields': (
				'user', ('balance', 'donate'), 'karma'
			)
		}),
	)


class PlayItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'tech_name', 'date_created', 'default', 'hidden')
	list_display_links = ("id", "tech_name")
	list_editable = ('default', 'hidden')
	list_filter = ('date_created', 'default', 'hidden')
	list_select_related = True
	ordering = ('id',)
	date_hierarchy = "date_created"
	readonly_fields = ("date_created",)
	search_fields = ('tech_name',)
	empty_value_display = '-empty-'
	fieldsets = (
		(None, {
			'fields': ('tech_name', 'date_created', ('default', 'hidden'))
		}),
	)

	def save_model(self, request, obj, form, change):
		obj.from_admin_site = True
		super().save_model(request, obj, form, change)


class WeaponAdmin(PlayItemAdmin):
	list_display = ('id', 'tech_name', 'date_created', "start", 'slot', 'hidden')
	list_editable = ('hidden', "start", "slot")
	list_filter = ('date_created', 'slot', 'hidden')
	fieldsets = (
		(None, {
			'fields': ('tech_name', 'date_created', 'slot', ('hidden', 'start'))
		}),
	)


class WeaponAddonsAdmin(admin.ModelAdmin):
	list_display = ("__str__", )
	filter_horizontal = ("stock", "barrel", "muzzle", "mag", "scope", "grip")
	list_select_related = True
	ordering = ("id", )
	search_fields = ("weapon__tech_name", )
	empty_value_display = '-empty-'


class UserWeaponConfigInline(admin.TabularInline):
	model = WeaponConfig
	extra = 0


class UserWeaponAdmin(admin.ModelAdmin):
	inlines = (UserWeaponConfigInline, )
	list_display = ("id", "__str__", "weapon_with_addons", "date_added",)
	list_display_links = ("id", "__str__")
	list_select_related = True
	ordering = ("-date_added", )
	date_hierarchy = "date_added"
	readonly_fields = ("date_added",)
	search_fields = ("profile__user__username", "weapon_with_addons__weapon__tech_name")
	empty_value_display = '-empty-'
	autocomplete_fields = ("profile", "weapon_with_addons")
	fieldsets = (
		(None, {
			"fields": (("profile", "weapon_with_addons"), "date_added", )
		}),
		("Addons available for this user for this weapon", {
			"fields": (
				"user_addon_stock", "user_addon_barrel", "user_addon_muzzle",
				"user_addon_mag", "user_addon_scope", "user_addon_grip"
			)
		})
	)


class UserWeaponConfigAdmin(admin.ModelAdmin):
	list_display = ("id", "profile", "character", "primary", "secondary", "date_created", "current")
	list_display_links = ("id",)
	list_editable = ("current", )
	list_select_related = True
	ordering = ("-date_created", )
	date_hierarchy = "date_created"
	readonly_fields = ("date_created",)
	search_fields = ("profile", "character__tech_name", "primary__weapon__weapon_with_addons__weapon__tech_name")
	empty_value_display = '-empty-'


# For future unique fields 3 classes below created


class CharacterAdmin(PlayItemAdmin):
	pass


class AddonAdmin(PlayItemAdmin):
	pass


admin.site.site_header = _('Cyber Administration')
admin.site.index_title = _('Cyber Administration')
admin.site.site_title = _('Cyber API')
admin.site.unregister(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Character, PlayItemAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Stock, PlayItemAdmin)
admin.site.register(Barrel, PlayItemAdmin)
admin.site.register(Muzzle, PlayItemAdmin)
admin.site.register(Mag, PlayItemAdmin)
admin.site.register(Scope, PlayItemAdmin)
admin.site.register(Grip, PlayItemAdmin)
admin.site.register(WeaponAddons, WeaponAddonsAdmin)
admin.site.register(UserWeapon, UserWeaponAdmin)
admin.site.register(UserWeaponConfig, UserWeaponConfigAdmin)
