from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Profile(models.Model):
	"""
	Information about user, works in one to one link with default :model:User
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.PositiveIntegerField(
		help_text=_('Coins earned by playing'),
		verbose_name=_("Game Balance"),
	)
	donate = models.PositiveIntegerField(
		help_text=_('Coins obtained by donations'),
		verbose_name=_("Donate Balance")
	)

	# Fields to add
	# character M2M

