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


admin.site.register(Notification, NotificationAdmin)
