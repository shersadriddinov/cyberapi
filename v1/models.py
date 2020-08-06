from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class PlayItem(models.Model):
	"""
	Abstract class to inherit all common properties of characters, weapons and addons
	"""
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
	All characters user can use in game inherits from :model:`PlayItem`
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
	All weapons available in game, inherits from :model:`PlayItem`
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
	Abstract model for all addons, to collect all addons and their common properties, inherits from :model:`PlayItem`
	"""

	class Meta:
		abstract = True


class Stock(Addon):
	"""
	Stock addons, inherits from :model:`Addon`
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
	Barrel addons, inherits from :model:`Addon`
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
	Muzzle addons, inherits from :model:`Addon`
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
	Mag addons, inherits from :model:`Addon`
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
	Scope addons, inherits from :model:`Addon`
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
	Grip addons, inherits from :model:`Addon`
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
	friends = models.ManyToManyField(
		"Profile",
		verbose_name=_("Friends"),
		blank=True,
		related_name="friend_list",
		through="FriendsList",
	)
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


class FriendsList(models.Model):
	"""
	ManyToMany model for :model:`Profile` and :model:`Profile` to make friends & clans behaviour with some additional
	info, represents all friends of user and their clan
	"""
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("User"), related_name="profile")
	friend = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("Friend"), related_name="friend")
	date_added = models.DateTimeField(verbose_name=_("Date Added"), default=timezone.now)
	matches_played = models.PositiveIntegerField(verbose_name=_("In teams plays count"), default=0, blank=True)

	class Meta:
		db_table = "friends_list"
		verbose_name = _("Friends List")
		verbose_name_plural = _("Friends List")
		ordering = ("-date_added", )
		unique_together = ('profile', 'friend')

	@classmethod
	def add_friend(cls, profile, friend):
		connection, created = FriendsList.objects.get_or_create(profile=profile, friend=friend)
		reverse_connection, reverse_created = FriendsList.objects.get_or_create(profile=friend, friend=profile)
		return created

	@classmethod
	def remove_friend(cls, profile, friend):
		connection, created = FriendsList.objects.get_or_create(profile=profile, friend=friend)
		connection.delete() if not created else False
		reverse_connection, reverse_created = FriendsList.objects.get_or_create(profile=friend, friend=profile)
		reverse_connection.delete() if not reverse_created else False
		return not created

	def __str__(self):
		return str(self.profile)


class UserCharacter(models.Model):
	"""
	ManyToMany model for :model:`Profile` and :model:`Character` with some additional info. Represents all characters
	selected by user and all users selected certain character
	"""
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
	"""
	ManyToMany model for :model:`Weapon` and :model:`Addon`. Represents all available addons for the given weapon
	"""
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
	"""
	Many to Many model for :model:`Profile` and :model:`WeaponAddons`. Represents User and its
	weapons with selected addons.
	"""
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


class UserWeaponConfig(models.Model):
	"""
	Many to Many model for :model:`UserWeapon` and to addons. Represents User's Weapon with its addons combinations
	defined by user
	"""
	weapon = models.ForeignKey(UserWeapon, on_delete=models.CASCADE, verbose_name=_("User Weapon"), )
	date_created = models.DateTimeField(verbose_name=_("Date Created"), default=timezone.now)
	stock = models.ForeignKey(Stock, on_delete=models.SET_NULL, verbose_name=_("Stock"), null=True)
	barrel = models.ForeignKey(Barrel, on_delete=models.SET_NULL, verbose_name=_("Barrel"), null=True)
	muzzle = models.ForeignKey(Muzzle, on_delete=models.SET_NULL, verbose_name=_("Muzzle"), null=True)
	mag = models.ForeignKey(Mag, on_delete=models.SET_NULL, verbose_name=_("Magazine"), null=True)
	scope = models.ForeignKey(Scope, on_delete=models.SET_NULL, verbose_name=_("Scope"), null=True)
	grip = models.ForeignKey(Grip, on_delete=models.SET_NULL, verbose_name=_("Grip"), null=True)

	class Meta:
		db_table = "profile_weapon_config"
		verbose_name = _("User Weapons Configuration")
		verbose_name_plural = _("User Weapons Configuration")
		ordering = ("-date_created", )

	def __str__(self):
		return self.weapon.profile.user.username + " config " + str(self.id)

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if (
				self.stock.pk in self.weapon.user_addon_stock and
				self.barrel.pk in self.weapon.user_addon_barrel and
				self.muzzle.pk in self.weapon.user_addon_muzzle and
				self.mag.pk in self.weapon.user_addon_mag and
				self.scope.pk in self.weapon.user_addon_scope and
				self.grip.pk in self.weapon.user_addon_grip
		):
			super(UserWeaponConfig, self).save(force_insert, force_update, using, update_fields)
