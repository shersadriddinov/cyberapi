import binascii
import os
from datetime import timedelta

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
	"""
	Model to represent user notifications
	"""
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


SERVER_STATUS = (
	(0, _("Server not assigned")),
	(1, _("Preparing")),
	(2, _("Waiting for players")),
	(3, _("Game in process")),
	(4, _("Game finished")),
	(5, _("Ready for close"))
)

SERVER_TYPE = (
	(0, _("public")),
	(1, _("private"))
)

MATCH_TYPE = (
	(0, _("casual")),
)


def validate_port(value):
	if value > 65535:
		raise ValidationError(
			_('%(value)s is not port number'),
			params={'value': value},
		)


class Server(models.Model):
	"""
	Model to keep track of game servers
	"""
	host_address = models.GenericIPAddressField(
		null=True,
		blank=False,
		help_text=_("IP address accepts both IPv4, IPv6"),
		verbose_name=_("Host address")
	)
	port = models.PositiveIntegerField(
		verbose_name=_("Port"),
		validators=(validate_port, ),
		null=False,
		default=8080,
		blank=False
	)
	init_user = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		verbose_name=_("User requested server creation")
	)
	status = models.PositiveSmallIntegerField(
		choices=SERVER_STATUS,
		verbose_name=_("Server current status"),
		help_text=_("0 - Server not assigned\n1 - Preparing\n2 - Waiting for players\n3 - Game in process\n4 - Game finished\n5 - Ready for close"),
		default=0,
		blank=False
	)
	date_created = models.DateTimeField(
		db_column='date_created',
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the object was added to database")
	)
	token = models.CharField(_("Token"), max_length=40, db_index=True)
	game_type = models.PositiveSmallIntegerField(
		choices=MATCH_TYPE,
		verbose_name=_("Game type"),
		help_text=_("0 - Casual\n"),
		null=False,
		blank=False
	)
	server_type = models.PositiveSmallIntegerField(
		choices=SERVER_TYPE,
		verbose_name=_("Server Security Type"),
		help_text=_("0 - Public\n1 - Private\n2"),
		null=False,
		blank=False
	)
	white_list = models.ManyToManyField(User, blank=True, verbose_name=_("White List"), related_name='server_white_list')

	class Meta:
		verbose_name = _("Game Server")
		verbose_name_plural = _("Game Servers")
		db_table = "game_servers"
		ordering = ("date_created", )

	def save(self, *args, **kwargs):
		if not self.token:
			self.token = self.generate_key()
		return super().save(*args, **kwargs)

	def generate_key(self):
		return binascii.hexlify(os.urandom(20)).decode()

	def __str__(self):
		return str(self.host_address) + ":" + str(self.port)


class Invite(models.Model):
	"""
	Model to represent game invites send by users
	"""
	host_user = models.ForeignKey(User, related_name="host_user", on_delete=models.CASCADE, verbose_name=_("Inviter"), null=False, blank=False)
	invited_user = models.ForeignKey(User, related_name="invited_user", on_delete=models.CASCADE, verbose_name=_("Invited"), null=False, blank=False)
	server = models.ForeignKey(Server, on_delete=models.CASCADE, verbose_name=_("Server"), null=False, blank=False)
	expires = models.DateTimeField(
		db_column='expires',
		null=False,
		blank=True,
		verbose_name=_("Expiry Date"),
		help_text=_("If not specified, invitation expires after 3 days")
	)
	date_created = models.DateTimeField(
		db_column='date_created',
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the object was added to database")
	)

	class Meta:
		verbose_name = _("Invitation")
		verbose_name_plural = _("Invitations")
		db_table = "invitations"
		ordering = ("date_created", )

	def save(self, *args, **kwargs):
		if not self.expires:
			self.expires = timezone.now() + timedelta(hours=24 * 3)
		self.server.white_list.add(self.invited_user)
		self.server.save()
		return super().save(*args, **kwargs)

	def __str__(self):
		return str(self.host_user) + "-" + str(self.invited_user) + "-" + str(self.id)


class GameWinPlace(models.Model):
	place = models.PositiveSmallIntegerField(verbose_name=_("Place in Game"), null=False, blank=False)
	reward = models.PositiveSmallIntegerField(verbose_name=_("Reward for Place"), null=False, blank=False)

	class Meta:
		verbose_name = _("Points for Game Winning")
		verbose_name_plural = _("Points for Game Winning")


GAME_STAT_METRICS = (
	(1, "kill"),
	(2, "death"),
	(3, "damage"),
	(4, "action")
)


class GameStatFactor(models.Model):
	metric = models.PositiveSmallIntegerField(verbose_name=_("Metric"), choices=GAME_STAT_METRICS, null=False, blank=False)
	factor = models.FloatField(verbose_name=_("Factor"), null=False, blank=False)

	class Meta:
		verbose_name = _("Factor for Experience Count")
		verbose_name_plural = _("Factors for Experience Count")


class PlayerStatistic(models.Model):
	user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE, null=False, blank=False)
	game = models.ForeignKey(Server, verbose_name=_("Game"), on_delete=models.SET_NULL, null=True, blank=True)
	place = models.ForeignKey(GameWinPlace, verbose_name=_("Place"), on_delete=models.CASCADE, null=False, blank=False)
	kill = models.PositiveSmallIntegerField(verbose_name=_("Kill"), null=False, blank=False, default=0)
	death = models.PositiveSmallIntegerField(verbose_name=_("Death"), null=False, blank=False, default=0)
	damage = models.PositiveIntegerField(verbose_name=_("Damage"), null=False, blank=False, default=0)
	action = models.PositiveSmallIntegerField(verbose_name=_("Actions"), null=False, blank=False, default=0)
	date = models.DateTimeField(verbose_name=_("Game Date"), default=timezone.now, )

	class Meta:
		db_table = "stats"
		verbose_name = _("Player Statistic")
		verbose_name_plural = _("Players Statistics")
		ordering = ("date", )
		unique_together = ("user", "game")

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		factor_kill = GameStatFactor.objects.get(metric=1).factor
		factor_death = GameStatFactor.objects.get(metric=2).factor
		factor_damage = GameStatFactor.objects.get(metric=3).factor
		factor_action = GameStatFactor.objects.get(metric=4).factor
		self.user.profile.experience += (self.kill * factor_kill + self.death * factor_death + self.damage * factor_damage + self.action * factor_action) + self.place.reward
		self.user.profile.save()
		super(PlayerStatistic, self).save(force_insert, force_update, using, update_fields)
