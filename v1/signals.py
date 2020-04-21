from django.db.models.signals import post_save
from django.dispatch import receiver
from v1.models import *


@receiver(post_save, sender=Weapon)
def create_weapon_with_addons(sender, instance, created, **kwargs):
	if created:
		WeaponAddons.objects.create(weapon=instance)


@receiver(post_save, sender=UserWeapon)
def create_weapon_with_addons(sender, instance, created, **kwargs):
	if created:
		instance.user_addon_stock = list(instance.weapon_with_addons.stock.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_barrel = list(instance.weapon_with_addons.barrel.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_muzzle = list(instance.weapon_with_addons.muzzle.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_mag = list(instance.weapon_with_addons.mag.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_scope = list(instance.weapon_with_addons.scope.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.user_addon_grip = list(instance.weapon_with_addons.grip.filter(default=True, hidden=False).values_list('id', flat=True))
		instance.save()