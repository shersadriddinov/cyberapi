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
		help_text=_('Price'),
		verbose_name=_("Could be in balance or donat value")
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
		for character in self.lot.character.all():
			UserCharacter.objects.create(profile=self.user.profile, character=character)
		for weapon in self.lot.weapons.all():
			UserWeapon.objects.create(profile=self.user.profile, weapon_with_addons=WeaponAddons.objects.get(weapon=weapon))
		for stock in self.lot.stock.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user.profile):
				if user_weapon.weapon_with_addons.filter(stock=stock).exists():
					user_weapon.user_addon_stock.append(stock.id)
					break
		for barrel in self.lot.barrel.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user.profile):
				if user_weapon.weapon_with_addons.filter(barrel=barrel).exists():
					user_weapon.user_addon_stock.append(barrel.id)
					break
		for muzzle in self.lot.muzzle.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user.profile):
				if user_weapon.weapon_with_addons.filter(muzzle=muzzle).exists():
					user_weapon.user_addon_stock.append(muzzle.id)
					break
		for mag in self.lot.mag.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user.profile):
				if user_weapon.weapon_with_addons.filter(mag=mag).exists():
					user_weapon.user_addon_stock.append(mag.id)
					break
		for grip in self.lot.grip.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user.profile):
				if user_weapon.weapon_with_addons.filter(grip=grip).exists():
					user_weapon.user_addon_stock.append(grip.id)
					break
		for scope in self.lot.stock.all():
			for user_weapon in UserWeapon.objects.filter(profile=self.user.profile):
				if user_weapon.weapon_with_addons.filter(scope=scope).exists():
					user_weapon.user_addon_stock.append(scope.id)
					break
		super(UserLots, self).save(force_insert, force_update, using, update_fields)
