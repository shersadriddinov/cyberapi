from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from v1.models import *


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	"""
	Auto create :model:`Profile` and Token instances for each new :model:`User` instance
	"""
	if created:
		Profile.objects.create(user=instance)
		Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	"""
	Auto update :model:`Profile` instance for each :model:`User` instance update
	"""
	instance.profile.save()


@receiver(post_save, sender=Weapon)
def create_weapon_with_addons(sender, instance, created, **kwargs):
	"""
	Auto create :model:`WeaponAddons` instance for each :model:`Weapon` instance
	"""
	if created:
		WeaponAddons.objects.create(weapon=instance)


@receiver(post_save, sender=Weapon)
def add_default_weapon_for_all(sender, instance, **kwargs):
	"""
	Auto add weapon to all users if weapon is marked as a default
	"""
	if instance.default and not instance.hidden and getattr(instance, 'from_admin_site', False):
		weapon_with_addons = WeaponAddons.objects.get(weapon=instance)
		users = Profile.objects.all()
		for user in users:
			try:
				UserWeapon.objects.get(profile=user, weapon_with_addons=weapon_with_addons)
			except ObjectDoesNotExist:
				UserWeapon.objects.create(profile=user, weapon_with_addons=weapon_with_addons)


@receiver(post_save, sender=UserWeapon)
def create_weapon_with_addons(sender, instance, created, **kwargs):
	"""
	Auto add all default and not hidden addons for each :model:`UserWeapon` instance as a list of ids
	"""
	if created:
		instance.user_addon_stock = list(instance.weapon_with_addons.stock.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_barrel = list(instance.weapon_with_addons.barrel.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_muzzle = list(instance.weapon_with_addons.muzzle.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_mag = list(instance.weapon_with_addons.mag.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_scope = list(instance.weapon_with_addons.scope.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_grip = list(instance.weapon_with_addons.grip.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.save()
		UserWeaponConfig.objects.create(
			weapon=instance,
			stock=Stock.objects.get(pk=instance.user_addon_stock[0]),
			barrel=Barrel.objects.get(pk=instance.user_addon_barrel[0]),
			muzzle=Muzzle.objects.get(pk=instance.user_addon_muzzle[0]),
			mag=Mag.objects.get(pk=instance.user_addon_mag[0]),
			grip=Grip.objects.get(pk=instance.user_addon_grip[0]),
			scope=Scope.objects.get(pk=instance.user_addon_scope[0])
		)


@receiver(post_save, sender=Profile)
def add_default_weapons_with_addons_to_new_user(sender, instance, created, **kwargs):
	"""
	Auto add all default weapons for each new :model:`Profile` instance
	"""
	if created:
		default_weapons = WeaponAddons.objects.filter(weapon__default=True, weapon__hidden=False)
		for weapon in default_weapons:
			UserWeapon.objects.create(
				profile=instance,
				weapon_with_addons=weapon,
			)
