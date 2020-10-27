from django.contrib import admin
from socket_handler.models import *


class NotificationAdmin(admin.ModelAdmin):
	list_display = ("__str__", "user", "notif_type", "date_created", "status")
	list_display_links = ("__str__", )
	list_filter = ('notif_type', "date_created")
	list_select_related = True
	ordering = ("-date_created",)
	date_hierarchy = "date_created"
	readonly_fields = ("date_created",)
	search_fields = ("id", "user", "friend_id")


class ServerAdmin(admin.ModelAdmin):
	list_display = ("__str__", "game_type", "server_type", "init_user", "status", "date_created")
	list_display_links = ("__str__", )
	list_filter = ("game_type", "server_type", "status")
	list_select_related = True
	ordering = ("-date_created", )
	date_hierarchy = "date_created"
	readonly_fields = ("token", "date_created",)
	filter_horizontal = ("white_list", )
	search_fields = ("id", "host_address", "init_user")
	fieldsets = (
		(None, {
			"fields": (("host_address", "port"), "date_created", "init_user")
		}),
		("Server Properties", {
			"fields": ("status", "game_type", "server_type", "token")
		}),
		("White List", {
			"fields": ("white_list", )
		})
	)


class InviteAdmin(admin.ModelAdmin):
	list_display = ("id", "host_user", "invited_user", "server", "date_created", "expires")
	list_display_links = ("id", )
	list_editable = ("host_user", "invited_user", "expires", "server")
	list_filter = ("date_created",)
	list_select_related = True
	ordering = ("-date_created", )
	date_hierarchy = "date_created"
	search_fields = ("host_user", "invited_user", "server")
	fieldsets = (
		(None, {
			"fields": (("host_user", "invited_user", "server"), )
		}),
		("Invite Properties", {
			"fields": (
				("date_created", "expires"),
			)
		})
	)


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Server, ServerAdmin)
admin.site.register(Invite, InviteAdmin)
