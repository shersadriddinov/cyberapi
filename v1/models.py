from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


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
	karma = models.SmallIntegerField(
		null=False,
		default=0,
		blank=True,
		help_text=_('Points earned/losed by good/bad behaviour'),
		verbose_name=_("Karma")
	)
	client_settings_json = JSONField(
		null=True,
		blank=True,
		verbose_name=_("Custom user settings"),
		help_text=_("JSON field containing user custom settings"),
	)

	class Meta:
		db_table = 'profile'
		verbose_name = _('User Balance')
		verbose_name_plural = _('User Balance')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()




