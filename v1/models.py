from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Character(models.Model):
	"""

	"""
	tech_name = models.CharField(
		db_column='tech_name',
		null=False,
		blank=False,
		max_length=256,
		verbose_name=_("Technical name"),
		help_text=_("Character technical name")
	)
	default = models.BooleanField(
		db_column='default',
		default=False,
		blank=True,
		verbose_name=_("Default Character"),
		help_text=_("Is the character available by default")
	)
	hidden = models.BooleanField(
		db_column='hidden',
		default=False,
		blank=True,
		verbose_name=_("Exclude from requests"),
		help_text=_("Exclude from requests made by users")
	)
	date_created = models.DateTimeField(
		db_column='date_created',
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the character was added to database")
	)

	class Meta:
		db_table = "character"
		verbose_name = _("Character")
		verbose_name_plural = _("Characters")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Weapon(models.Model):
	"""

	"""
	tech_name = models.CharField(
		db_column='tech_name',
		null=False,
		blank=False,
		max_length=256,
		verbose_name=_("Technical name"),
		help_text=_("Weapon technical name")
	)
	addon_stock_count = models.PositiveSmallIntegerField(
		db_column="addon_stock_count",
		default=1,
		blank=True,
		verbose_name=_("Addon Stock Count"),
		help_text=_("The number of available stock for this weapon")
	)
	addon_barrel_count = models.PositiveSmallIntegerField(
		db_column="addon_barrel_count",
		default=1,
		blank=True,
		verbose_name=_("Addon Barrel Count"),
		help_text=_("The number of available barrel for this weapon")
	)
	addon_muzzle_count = models.PositiveSmallIntegerField(
		db_column="addon_muzzle_count",
		default=1,
		blank=True,
		verbose_name=_("Addon Muzzle Count"),
		help_text=_("The number of available muzzle for this weapon")
	)
	addon_mag_count = models.PositiveSmallIntegerField(
		db_column="addon_mag_count",
		default=1,
		blank=True,
		verbose_name=_("Addon Mag Count"),
		help_text=_("The number of available mag for this weapon")
	)
	addon_scope_count = models.PositiveSmallIntegerField(
		db_column="addon_scope_count",
		default=1,
		blank=True,
		verbose_name=_("Addon Scope Count"),
		help_text=_("The number of available scope for this weapon")
	)
	addon_grip_count = models.PositiveSmallIntegerField(
		db_column="addon_grip_count",
		default=1,
		blank=True,
		verbose_name=_("Addon Grip Count"),
		help_text=_("The number of available grip for this weapon")
	)
	default = models.BooleanField(
		db_column='default',
		default=False,
		blank=True,
		verbose_name=_("Default Weapon"),
		help_text=_("Is the weapon available by default")
	)
	hidden = models.BooleanField(
		db_column='hidden',
		default=False,
		blank=True,
		verbose_name=_("Exclude from requests"),
		help_text=_("Exclude from requests made by users")
	)
	date_created = models.DateTimeField(
		db_column='date_created',
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the weapon was added to database")
	)

	class Meta:
		db_table = "weapon"
		verbose_name = _("Weapon")
		verbose_name_plural = _("Weapons")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Addon(models.Model):
	"""

	"""
	tech_name = models.CharField(
		db_column='tech_name',
		null=False,
		blank=False,
		max_length=256,
		verbose_name=_("Technical name"),
		help_text=_("Addon technical name")
	)
	default = models.BooleanField(
		db_column='default',
		default=False,
		blank=True,
		verbose_name=_("Default Addon"),
		help_text=_("Is the addon available by default")
	)
	hidden = models.BooleanField(
		db_column='hidden',
		default=False,
		blank=True,
		verbose_name=_("Exclude from requests"),
		help_text=_("Exclude from requests made by users")
	)
	date_created = models.DateTimeField(
		db_column='date_created',
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the addon was added to database")
	)

	class Meta:
		abstract = True


class Stock(Addon):
	"""
	#TODO: Find rules for stock
	"""
	class Meta:
		db_table = "addon_stock"
		verbose_name = _("Addon Stock")
		verbose_name_plural = _("Addon Stocks")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Barrel(Addon):
	"""
	#TODO: Find rules for barrel
	"""

	class Meta:
		db_table = "addon_barrel"
		verbose_name = _("Addon Barrel")
		verbose_name_plural = _("Addon Barrels")
		ordering = ("-date_created",)

	def __str__(self):
		return self.tech_name


class Muzzle(Addon):
	"""
	#TODO: Find rules for Muzzle
	"""

	class Meta:
		db_table = "addon_muzzle"
		verbose_name = _("Addon Muzzle")
		verbose_name_plural = _("Addon Muzzles")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Mag(Addon):
	"""
	#TODO: Find rules for Mag
	"""

	class Meta:
		db_table = "addon_mag"
		verbose_name = _("Addon Magazine")
		verbose_name_plural = _("Addon Magazines")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Scope(Addon):
	"""
	#TODO: Find rules for Scope
	"""

	class Meta:
		db_table = "addon_scope"
		verbose_name = _("Addon Scope")
		verbose_name_plural = _("Addon Scopes")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Grip(Addon):
	"""
	#TODO: Find rules for Grip
	"""

	class Meta:
		db_table = "addon_grip"
		verbose_name = _("Addon Grip")
		verbose_name_plural = _("Addon Grips")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Profile(models.Model):
	"""
	Information about user, works in one to one link with default :model:`User`
	"""	
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
		db_column='karma',
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
	character = models.ManyToManyField(
		Character,
		blank=True,
		verbose_name=_("User's Character"),
		related_name="profile_character",
		through="UserCharacter"
	)

	class Meta:
		db_table = 'profile'
		verbose_name = _('User Balance')
		verbose_name_plural = _('User Balance')

	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


class UserCharacter(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("User"))
	character = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name=_("Character"))
	date_added = models.DateTimeField(verbose_name=_("Date Added"), default=timezone.now)

	class Meta:
		db_table = "profile_character"
		verbose_name = _("User & Character")
		verbose_name_plural = _("Users & Characters")
		ordering = ("-date_added", )

	def __str__(self):
		return self.profile.user.username + " with " + self.character.tech_name


class UserWeapon(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("User"))
	weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE, verbose_name=_("Weapon"))
	date_added = models.DateTimeField(verbose_name=_("Date Added"), default=timezone.now)

