from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Profile(models.Model):
	"""
	Information about user, works in one to one link with default :model:`User`
	"""
	# TODO: add field character (M2M)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	balance = models.PositiveIntegerField(
		db_column='balance',
		null=False,
		default=0,
		blank=True,
		help_text=_('Coins earned by playing'),
		verbose_name=_("Game Balance"),
	)
	donate = models.PositiveIntegerField(
		db_column='column',
		null=False,
		default=0,
		blank=True,
		help_text=_('Coins obtained by donations'),
		verbose_name=_("Donate Balance")
	)

	class Meta:
		db_table = 'user_balance'
		verbose_name = _('User Balance')
		verbose_name_plural = _('User Balance')


