from django.db import models
from django.utils.translation import gettext_lazy as _

from v1.models import *


class Lot(models.Model):
	"""
	Model to represent single lot in store, might include weapon, character, addons
	"""

	tech_name = models.CharField(
		null=False,
		blank=True,
		max_length=256,
		verbose_name=_("Technical name"),
		help_text=_("Object item technical name")
	)
	premium = models.BooleanField(
		default=False,
		blank=True,
		verbose_name=_("Premium item"),
		help_text=_("Premium items are only available for donat balance")
	)
	price = models.PositiveIntegerField(
		null=False,
		default=0,
		blank=True,
		help_text=_('Could be in balance or donat value'),
		verbose_name=_("Price")
	)
	status = models.BooleanField(
		default=True,
		blank=True,
		verbose_name=_("Status"),
		help_text=_("Is item available for purchase")
	)
	date_created = models.DateTimeField(
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the object was added to database")
	)
	character = models.ManyToManyField(Character, blank=True, verbose_name=_("Character"), related_name="lot_character",)
	weapons = models.ManyToManyField(Weapon, blank=True, verbose_name=_("Weapon"), related_name="lot_weapons")
	stock = models.ManyToManyField(Stock, blank=True, verbose_name=_("Stock"), related_name="lot_stock")
	barrel = models.ManyToManyField(Barrel, blank=True, verbose_name=_("Barrel"), related_name="lot_barrel")
	muzzle = models.ManyToManyField(Muzzle, blank=True, verbose_name=_("Muzzle"), related_name="lot_muzzle")
	mag = models.ManyToManyField(Mag, blank=True, verbose_name=_("Magazine"), related_name="lot_mag")
	scope = models.ManyToManyField(Scope, blank=True, verbose_name=_("Scope"), related_name="lot_scope")
	grip = models.ManyToManyField(Grip, blank=True, verbose_name=_("Grip"), related_name="lot_grip")

	class Meta:
		db_table = "lots"
		verbose_name = _("Lot")
		verbose_name_plural = _("Lots")
		ordering = ("-date_created", )

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if not self.tech_name:
			self.tech_name = str(self.id)
		super(Lot, self).save(force_insert, force_update, using, update_fields)

	def __str__(self):
		return self.tech_name


class UserLots(models.Model):
	"""
	User bought items
	"""

	user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("User"))
	lot = models.ForeignKey(Lot, on_delete=models.CASCADE, verbose_name=_("Lot"))
	date_purchased = models.DateTimeField(
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Purchased"),
		help_text=_("Date when the lot was purchased")
	)

	class Meta:
		unique_together = ('user', 'lot')
		db_table = "user_lots"
		verbose_name = _("User Lot")
		verbose_name_plural = _("User Lots")
		ordering = ("-date_purchased", )

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		# Add all characters in slot to user
		for character in self.lot.character.all():
			UserCharacter.objects.get_or_create(character=character, profile=self.user)
		# Add all weapons on lot to user
		for weapon in self.lot.weapons.all():
			weapon_with_addons = WeaponAddons.objects.get(weapon=weapon)
			UserWeapon.objects.get_or_create(weapon_with_addons=weapon_with_addons, profile=self.user)
		# Add stock from lot to available user_weapon object
		for stock in self.lot.stock.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user):
				if stock in user_weapon.weapon_with_addons.stock.all() and stock.id not in user_weapon.user_addon_stock:
					user_weapon.user_addon_stock.append(stock.id)
					break
		# Add barrel from lot to available user_weapon object
		for barrel in self.lot.barrel.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user):
				if barrel in user_weapon.weapon_with_addons.barrel.all() and barrel.id not in user_weapon.user_addon_barrel:
					user_weapon.user_addon_barrel.append(barrel.id)
					break
		# Add stock from lot to available user_weapon object
		for muzzle in self.lot.muzzle.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user):
				if muzzle in user_weapon.weapon_with_addons.muzzle.all() and muzzle.id not in user_weapon.user_addon_muzzle:
					user_weapon.user_addon_muzzle.append(muzzle.id)
					break
		# Add mag from lot to available user_weapon object
		for mag in self.lot.mag.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user):
				if mag in user_weapon.weapon_with_addons.mag.all() and mag.id not in user_weapon.user_addon_mag:
					user_weapon.user_addon_mag.append(mag.id)
					break
		# Add grip from lot to available user_weapon object
		for grip in self.lot.grip.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user):
				if grip in user_weapon.weapon_with_addons.grip.all() and grip.id not in user_weapon.user_addon_grip:
					user_weapon.user_addon_grip.append(grip.id)
					break
		# Add grip from lot to available user_weapon object
		for grip in self.lot.grip.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user):
				if grip in user_weapon.weapon_with_addons.grip.all() and grip.id not in user_weapon.user_addon_grip:
					user_weapon.user_addon_grip.append(grip.id)
					break
		# Add scope from lot to available user_weapon object
		for scope in self.lot.scope.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user):
				if scope in user_weapon.weapon_with_addons.grip.all() and scope.id not in user_weapon.user_addon_scope:
					user_weapon.user_addon_scope.append(scope.id)
					break
		super(UserLots, self).save(force_insert, force_update, using, update_fields)


class BattlePass(models.Model):
	"""
	Model to represent available game battle passes
	"""
	title = models.CharField(max_length=256, verbose_name=_("Title"), null=False, blank=False)
	status = models.BooleanField(default=True, blank=True, verbose_name=_("Status"), help_text=_("Is battle pass active"))
	expires = models.PositiveIntegerField(
		verbose_name=_("Expires"),
		help_text=_("Hours to expire from purchase"),
		null=True,
		blank=True,
	)
	price = models.PositiveIntegerField(null=False, blank=False, help_text=_('Could be only in donat value'), verbose_name=_("Price"))
	reward = models.PositiveIntegerField(null=False, blank=False, help_text=_('Could be only in balance value'), verbose_name=_("Reward"))
	date_created = models.DateTimeField(
		db_column='date_created',
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Created"),
		help_text=_("Date when the object was added to database")
	)
	tasks = models.ManyToManyField(
		"Task",
		verbose_name=_("Tasks"),
		help_text=_("Select Tasks for this Battle Pass"),
		blank=False
	)

	class Meta:
		verbose_name = _("Battle Pass")
		verbose_name_plural = _("Battle Passes")
		ordering = ("-date_created", )


class Task(models.Model):
	"""
	Model to represent available tasks for BattlePasses
	"""
	title = models.CharField(max_length=256, verbose_name=_("Title"), null=False, blank=False)
	status = models.BooleanField(default=True, blank=True, verbose_name=_("Status"), help_text=_("Is task active"))
	target_score = models.PositiveIntegerField(
		null=False,
		blank=False,
		help_text=_('Score required to complete this task'),
		verbose_name=_("Target Score")
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
		verbose_name = _("Task")
		verbose_name_plural = _("Tasks")
		ordering = ("-date_created", )


class UserBattlePass(models.Model):
	"""
	Model to represent user purchased battle passes
	"""
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("User"))
	battle_pass = models.ForeignKey(BattlePass, on_delete=models.CASCADE, verbose_name=_("Battle Pass"))
	user_tasks = models.ManyToManyField("UserTask", blank=True, verbose_name=_("User Tasks"))
	status = models.BooleanField(default=True, blank=True, verbose_name=_("Status"), help_text=_("Is battle pass complete"))
	task_counter = models.PositiveSmallIntegerField(
		null=False,
		blank=True,
		help_text=_('Tasks left to complete'),
		verbose_name=_("Task Counter"),
	)
	date_purchased = models.DateTimeField(
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Purchased"),
		help_text=_("Date when user has purchased object")
	)

	class Meta:
		verbose_name = _("User Battle Pass")
		verbose_name_plural = _("User Battle Passes")
		ordering = ("-date_purchased", )


class UserTask(models.Model):
	"""
	Model to represent user tasks for user battle pass
	"""
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("User"))
	status = models.BooleanField(default=True, blank=True, verbose_name=_("Status"), help_text=_("Is task complete"))
	task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name=_("Task"))
	current_score = models.PositiveIntegerField(
		null=False,
		blank=False,
		help_text=_('Score user achieved to complete this task'),
		verbose_name=_("Current Score")
	)
	date_started = models.DateTimeField(
		null=False,
		blank=False,
		default=timezone.now,
		verbose_name=_("Date Task Started"),
		help_text=_("Date when user started task completion")
	)
	expires = models.PositiveIntegerField(
		verbose_name=_("Expires"),
		help_text=_("Hours to expire from purchase"),
		null=True,
		blank=True,
	)
	game_counter = models.PositiveSmallIntegerField(
		null=True,
		blank=True,
		help_text=_('Games user played to complete the task'),
		verbose_name=_("Game Counter"),
	)

	class Meta:
		verbose_name = _("User Task")
		verbose_name_plural = _("User Tasks")
		ordering = ("-date_started", )
