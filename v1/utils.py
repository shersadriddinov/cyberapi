from v1.models import *


def convert_zero_to_none(weapon_dict):
	for value in weapon_dict.values():
		if value == 0:
			value = None
	return weapon_dict


def get_or_make_weapon_config(weapon_dict, profile):
	convert_zero_to_none(weapon_dict)
	if weapon_dict is not None:
		try:
			weapon_conf = WeaponConfig.objects.get(
				weapon=UserWeapon.objects.filter(weapon_with_addons__weapon__pk=weapon_dict['weapon'], profile=profile).first(),
				stock=Stock.objects.filter(pk=weapon_dict["stock"]).first(),
				barrel=Barrel.objects.filter(pk=weapon_dict["barrel"]).first(),
				muzzle=Muzzle.objects.filter(pk=weapon_dict["muzzle"]).first(),
				mag=Mag.objects.filter(pk=weapon_dict["mag"]).first(),
				scope=Scope.objects.filter(pk=weapon_dict["scope"]).first(),
				grip=Grip.objects.filter(pk=weapon_dict["grip"]).first(),
			)
		except WeaponConfig.DoesNotExist:
			weapon_conf = WeaponConfig.objects.create(
				weapon=UserWeapon.objects.filter(weapon_with_addons__weapon__pk=weapon_dict['weapon'], profile=profile).first(),
				stock=Stock.objects.filter(pk=weapon_dict["stock"]).first(),
				barrel=Barrel.objects.filter(pk=weapon_dict["barrel"]).first(),
				muzzle=Muzzle.objects.filter(pk=weapon_dict["muzzle"]).first(),
				mag=Mag.objects.filter(pk=weapon_dict["mag"]).first(),
				scope=Scope.objects.filter(pk=weapon_dict["scope"]).first(),
				grip=Grip.objects.filter(pk=weapon_dict["grip"]).first(),
			)
		except WeaponConfig.MultipleObjectsReturned:
			weapon_conf = WeaponConfig.objects.get(
				weapon=UserWeapon.objects.filter(weapon_with_addons__weapon__pk=weapon_dict['weapon'], profile=profile).first(),
				stock=Stock.objects.filter(pk=weapon_dict["stock"]).first(),
				barrel=Barrel.objects.filter(pk=weapon_dict["barrel"]).first(),
				muzzle=Muzzle.objects.filter(pk=weapon_dict["muzzle"]).first(),
				mag=Mag.objects.filter(pk=weapon_dict["mag"]).first(),
				scope=Scope.objects.filter(pk=weapon_dict["scope"]).first(),
				grip=Grip.objects.filter(pk=weapon_dict["grip"]).first(),
			).first()
		except KeyError:
			raise Exception("cannot create weapon config")
		return weapon_conf
	else:
		return None


def temp_user_profile_get(user):
	response = {
		"id": user.id,
		"username": user.username,
		"first_name": user.first_name,
		"email": user.email,
		"balance": user.profile.balance,
		"donate": user.profile.donate,
		"karma": user.profile.karma,
		"client_settings_json": user.profile.client_settings_json,
		"is_staff": user.is_staff,
	}

	user_config = UserWeaponConfig.objects.filter(profile=user.profile, current=True).first()

	if user_config is None:
		start_characters = Character.objects.filter(default=True, hidden=False)
		start_weapons_first_slot = Weapon.objects.filter(start=True, hidden=False, slot=0)
		response['start_characters'] = [
			{"id": item.id, "tech_name": item.tech_name} for item in start_characters
		]
		response['start_weapons_first_slot'] = [
			{"id": weapon.id, "tech_name": weapon.tech_name} for weapon in start_weapons_first_slot
		]
	else:
		# Main Character
		if user_config.character:
			response['main_character'] = {
				"id": user_config.character.id,
				"tech_name": user_config.character.tech_name
			}
		else:
			start_characters = Character.objects.filter(default=True, hidden=False)
			response['start_characters'] = [
				{"id": item.id, "tech_name": item.tech_name} for item in start_characters
			]

		# Primary
		if user_config.primary:
			response['weapon_first_slot'] = {
				"id": user_config.primary.weapon.weapon_with_addons.weapon.id,
				"tech_name": user_config.primary.weapon.weapon_with_addons.weapon.tech_name,
			}
			# Stock
			if user_config.primary.stock:
				response['weapon_first_slot']['stock'] = {
					"id": user_config.primary.stock.id,
					"tech_name": user_config.primary.stock.tech_name
				}
			else:
				response['weapon_first_slot']['stock'] = None
			# Barrel
			if user_config.primary.barrel:
				response['weapon_first_slot']['barrel'] = {
					"id": user_config.primary.barrel.id,
					"tech_name": user_config.primary.barrel.tech_name
				}
			else:
				response['weapon_first_slot']['barrel'] = None
			# Muzzle
			if user_config.primary.muzzle:
				response['weapon_first_slot']['muzzle'] = {
					"id": user_config.primary.muzzle.id,
					"tech_name": user_config.primary.muzzle.tech_name
				}
			else:
				response['weapon_first_slot']['muzzle'] = None
			# Mag
			if user_config.primary.mag:
				response['weapon_first_slot']['mag'] = {
					"id": user_config.primary.mag.id,
					"tech_name": user_config.primary.mag.tech_name
				}
			else:
				response['weapon_first_slot']['mag'] = None
			# Scope
			if user_config.primary.scope:
				response['weapon_first_slot']['scope'] = {
					"id": user_config.primary.scope.id,
					"tech_name": user_config.primary.scope.tech_name
				}
			else:
				response['weapon_first_slot']['scope'] = None
			# Grip
			if user_config.primary.grip:
				response['weapon_first_slot']['grip'] = {
					"id": user_config.primary.grip.id,
					"tech_name": user_config.primary.grip.tech_name
				}
			else:
				response['weapon_first_slot']['grip'] = None
		# if primary is None
		else:
			start_weapons_first_slot = Weapon.objects.filter(start=True, hidden=False, slot=0)
			response['start_weapons_first_slot'] = [
				{"id": weapon.id, "tech_name": weapon.tech_name} for weapon in start_weapons_first_slot
			]

		# Secondary
		if user_config.secondary:
			response['weapon_second_slot'] = {
				"id": user_config.secondary.weapon.weapon_with_addons.weapon.id,
				"tech_name": user_config.secondary.weapon.weapon_with_addons.weapon.tech_name,
			}
			# Stock
			if user_config.secondary.stock:
				response['weapon_second_slot']['stock'] = {
					"id": user_config.secondary.stock.id,
					"tech_name": user_config.secondary.stock.tech_name
				}
			else:
				response['weapon_second_slot']['stock'] = None
			# Barrel
			if user_config.secondary.barrel:
				response['weapon_second_slot']['barrel'] = {
					"id": user_config.secondary.barrel.id,
					"tech_name": user_config.secondary.barrel.tech_name
				}
			else:
				response['weapon_second_slot']['barrel'] = None
			# Muzzle
			if user_config.secondary.muzzle:
				response['weapon_second_slot']['muzzle'] = {
					"id": user_config.secondary.muzzle.id,
					"tech_name": user_config.secondary.muzzle.tech_name
				}
			else:
				response['weapon_second_slot']['muzzle'] = None
			# Mag
			if user_config.secondary.mag:
				response['weapon_second_slot']['mag'] = {
					"id": user_config.secondary.mag.id,
					"tech_name": user_config.secondary.mag.tech_name
				}
			else:
				response['weapon_second_slot']['mag'] = None
			# Scope
			if user_config.secondary.scope:
				response['weapon_second_slot']['scope'] = {
					"id": user_config.secondary.scope.id,
					"tech_name": user_config.secondary.scope.tech_name
				}
			else:
				response['weapon_second_slot']['scope'] = None
			# Grip
			if user_config.secondary.grip:
				response['weapon_second_slot']['grip'] = {
					"id": user_config.secondary.grip.id,
					"tech_name": user_config.secondary.grip.tech_name
				}
			else:
				response['weapon_second_slot']['grip'] = None
		# if secondary is None
		else:
			response['weapon_second_slot'] = None
	return response
