from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class PlayItem(models.Model):
	tech_name = models.CharField(
		db_column='tech_name',
		null=False,
		blank=False,
		max_length=256,
		verbose_name=_("Technical name"),
		help_text=_("Object item technical name")
	)
	default = models.BooleanField(
		db_column='default',
		default=False,
		blank=True,
		verbose_name=_("Default"),
		help_text=_("Is the object available by default")
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
		help_text=_("Date when the object was added to database")
	)

	class Meta:
		abstract = True


class Character(PlayItem):
	"""

	"""

	class Meta:
		db_table = "character"
		verbose_name = _("Character")
		verbose_name_plural = _("Characters")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Weapon(PlayItem):
	"""

	"""

	class Meta:
		db_table = "weapon"
		verbose_name = _("Weapon")
		verbose_name_plural = _("Weapons")
		ordering = ("-date_created", )

	def __str__(self):
		return self.tech_name


class Addon(PlayItem):
	"""

	"""

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
	weapon = models.ManyToManyField(
		"WeaponAddons",
		blank=True,
		verbose_name=_("User's weapons with addons"),
		related_name="profile_weapon",
		through="UserWeapon"
	)

	class Meta:
		db_table = 'profile'
		verbose_name = _('User Game Status')
		verbose_name_plural = _('User Game Status')

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


class WeaponAddons(models.Model):
	weapon = models.ForeignKey(
		Weapon,
		on_delete=models.CASCADE,
		blank=False,
		verbose_name=_("Weapon"),
		help_text=_("Select weapon to attach all possible addons to it")
	)
	stock = models.ManyToManyField(
		Stock,
		blank=True,
		verbose_name=_("Stocks for selected weapon"),
		help_text=_("Select stocks to attach to chosen weapon")
	)
	barrel = models.ManyToManyField(
		Barrel,
		blank=True,
		verbose_name=_("Barrels for selected weapon"),
		help_text=_("Select barrels to attach to chosen weapon")
	)
	muzzle = models.ManyToManyField(
		Muzzle,
		blank=True,
		verbose_name=_("Muzzles for selected weapon"),
		help_text=_("Select muzzles to attach to chosen weapon")
	)
	mag = models.ManyToManyField(
		Mag,
		blank=True,
		verbose_name=_("Magazines for selected weapon"),
		help_text=_("Select magazines to attach to chosen weapon")
	)
	scope = models.ManyToManyField(
		Scope,
		blank=True,
		verbose_name=_("Scopes for selected weapon"),
		help_text=_("Select scopes to attach to chosen weapon")
	)
	grip = models.ManyToManyField(
		Grip,
		blank=True,
		verbose_name=_("Grips for selected weapon"),
		help_text=_("Select grips to attach to chosen weapon")
	)

	class Meta:
		db_table = "weapon_addons"
		verbose_name = _("Weapon & Available Addons")
		verbose_name_plural = _("Weapon & Available Addons")

	def __str__(self):
		return "Available Addons for " + self.weapon.tech_name


class UserWeapon(models.Model):
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("User"))
	weapon_with_addons = models.ForeignKey(WeaponAddons, on_delete=models.CASCADE, verbose_name=_("Weapon with Addons"))
	date_added = models.DateTimeField(verbose_name=_("Date Added"), default=timezone.now)
	user_addon_stock = ArrayField(
		models.PositiveIntegerField(blank=True),
		null=True,
		blank=True,
		verbose_name=_('User Stock Addons'),
		help_text=_("The list containing id's of user's stock addons, which points to id in Stock Addon table")
	)
	user_addon_barrel = ArrayField(
		models.PositiveIntegerField(blank=True),
		null=True,
		blank=True,
		verbose_name=_('User Barrel Addons'),
		help_text=_("The list containing id's of user's barrel addons, which points to id in Barrel Addon table")
	)
	user_addon_muzzle = ArrayField(
		models.PositiveIntegerField(blank=True),
		null=True,
		blank=True,
		verbose_name=_('User Stock Muzzle'),
		help_text=_("The list containing id's of user's muzzle addons, which points to id in Muzzle Addon table")
	)
	user_addon_mag = ArrayField(
		models.PositiveIntegerField(blank=True),
		null=True,
		blank=True,
		verbose_name=_('User Mag Addons'),
		help_text=_("The list containing id's of user's magazine addons, which points to id in Magazine Addon table")
	)
	user_addon_scope = ArrayField(
		models.PositiveIntegerField(blank=True),
		null=True,
		blank=True,
		verbose_name=_('User Scope Addons'),
		help_text=_("The list containing id's of user's scope addons, which points to id in Scope Addon table")
	)
	user_addon_grip = ArrayField(
		models.PositiveIntegerField(blank=True),
		null=True,
		blank=True,
		verbose_name=_('User Grip Addons'),
		help_text=_("The list containing id's of user's grip addons, which points to id in Grip Addon table")
	)

	class Meta:
		db_table = "profile_weapon"
		verbose_name = _("Profile & Weapon")
		verbose_name_plural = _("Profile & Weapon")
		ordering = ("-date_added", )

	def __str__(self):
		return self.profile.user.username + " with " + self.weapon_with_addons.weapon.tech_name
