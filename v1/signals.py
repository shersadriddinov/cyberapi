from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from v1.models import *
from v1.utils import create_weapon_config


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


@receiver(post_save, sender=UserWeapon)
def default_user_config(sender, instance, created, **kwargs):
	"""
	Try to auto create default user config using default start items
	"""
	if created:
		profile = instance.profile
		character = UserCharacter.objects.filter(profile=profile, character__default=True).first().character
		first_slot = UserWeapon.objects.filter(profile=profile, weapon_with_addons__weapon__slot=0, weapon_with_addons__weapon__start=True).first()
		second_slot = UserWeapon.objects.filter(profile=profile, weapon_with_addons__weapon__slot=1, weapon_with_addons__weapon__start=True).first()

		if character and first_slot and second_slot and (instance == first_slot or instance == second_slot):
			create_weapon_config(first_slot, 0, profile, character)
			create_weapon_config(second_slot, 1, profile, character)


@receiver(post_save, sender=UserWeaponConfig)
def set_new_current(sender, instance, created, **kwargs):
	"""
	Reset old current if new current chosen
	"""
	if instance.current:
		slot = 0 if instance.slot == 1 else 1
		if instance.character != UserWeaponConfig.objects.filter(profile=instance.profile, slot=slot, current=True).first().character:
			instance.current = False
			instance.save()
			raise Exception("Both current configs should have same character")
		else:
			previous = UserWeaponConfig.objects.filter(profile=instance.profile, slot=instance.slot, current=True).exclude(pk=instance.pk)
			for config in previous:
				config.current = False
				config.save()


# Old function to add new default weapon to all users
# @receiver(post_save, sender=Weapon)
# def add_default_weapon_for_all(sender, instance, created, **kwargs):
# 	"""
# 	Auto add weapon to all users if weapon is marked as a default
# 	"""
# 	if instance.default and not instance.hidden and getattr(instance, 'from_admin_site', False) and not created:
# 		weapon_with_addons = WeaponAddons.objects.get(weapon=instance)
# 		users = Profile.objects.all()
# 		for user in users:
# 			try:
# 				UserWeapon.objects.get(profile=user, weapon_with_addons=weapon_with_addons)
# 			except ObjectDoesNotExist:
# 				UserWeapon.objects.create(profile=user, weapon_with_addons=weapon_with_addons)

# Auto create User weapon config, left here for glory days
# @receiver(post_save, sender=UserWeapon)
# def create_weapon_with_addons(sender, instance, created, **kwargs):
# 	"""
# 	Auto add all default and not hidden addons for each :model:`UserWeapon` instance as a list of ids. Also adds default
# 	config
# 	"""
# 	# UserWeaponConfig.objects.create(
# 	# 	weapon=instance,
# 	# 	stock=Stock.objects.get(pk=instance.user_addon_stock[0]),
# 	# 	barrel=Barrel.objects.get(pk=instance.user_addon_barrel[0]),
# 	# 	muzzle=Muzzle.objects.get(pk=instance.user_addon_muzzle[0]),
# 	# 	mag=Mag.objects.get(pk=instance.user_addon_mag[0]),
# 	# 	grip=Grip.objects.get(pk=instance.user_addon_grip[0]),
# 	# 	scope=Scope.objects.get(pk=instance.user_addon_scope[0])
# 	# )


# Old function to add all new users default function
# @receiver(post_save, sender=Profile)
# def add_default_weapons_with_addons_to_new_user(sender, instance, created, **kwargs):
# 	"""
# 	Auto add all default weapons for each new :model:`Profile` instance
# 	"""
# 	if created:
# 		default_weapons = WeaponAddons.objects.filter(weapon__default=True, weapon__hidden=False)
# 		for weapon in default_weapons:
# 			UserWeapon.objects.create(
# 				profile=instance,
# 				weapon_with_addons=weapon,
# 			)


# Old function to make single main character
# @receiver(post_save, sender=UserCharacter)
# def set_new_main_character(sender, instance, created, **kwargs):
# 	"""
# 	After making a character main check for previous main character and make in False if True
# 	"""
# 	if instance.main:
# 		previous = UserCharacter.objects.filter(profile=instance.profile, main=True).exclude(pk=instance.pk).first()
# 		if previous:
# 			previous.main = False
# 			previous.save()


# Old function to make single main weapon
# @receiver(post_save, sender=UserWeapon)
# def remove_previous_main(sender, instance, created, **kwargs):
# 	"""
# 	After making a weapon main check for previous main character and make in False if True
# 	"""
# 	if instance.main:
# 		previous = UserWeapon.objects.filter(profile=instance.profile, main=True).exclude(pk=instance.pk).first()
# 		if previous:
# 			previous.main = False
# 			previous.save()
