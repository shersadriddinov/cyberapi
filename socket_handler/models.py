from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from v1.models import *


NOTIF_TYPES = (
	(1, _("FRIEND_REQUEST")),
	(2, _("MESSAGE")),
)


class Notification(models.Model):
	user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
	date_created = models.DateTimeField(
		db_column='date_created',
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the object was added to database")
	)
	notif_type = models.PositiveSmallIntegerField(
		choices=NOTIF_TYPES,
		verbose_name=_("Notification Type"),
		help_text=_("1 - FRIEND REQUEST\n 2 - MESSAGE\n"),
		null=False,
		blank=False
	)
	message = models.TextField(verbose_name=_("Message Text"), blank=True, null=True)
	friend_id = models.ForeignKey(
		User,
		related_name="friend",
		verbose_name=_("Friend requested"),
		help_text=_("ID of the user requested to add current user to the list of friends"),
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	status = models.BooleanField(verbose_name=_("Status"), default=True, blank=True)

	class Meta:
		verbose_name = _("Notification")
		verbose_name_plural = _("Notifications")
		db_table = "notifications"
		ordering = ("date_created", )

	def __str__(self):
		return "NOTIF-" + str(self.notif_type) + "-" + str(self.id)
