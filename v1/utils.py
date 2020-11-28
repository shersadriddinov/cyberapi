from v1.models import *


def create_weapon_config(weapon, slot, profile, character):
	stock = weapon.user_addon_stock
	barrel = weapon.user_addon_barrel
	muzzle = weapon.user_addon_muzzle
	mag = weapon.user_addon_mag
	scope = weapon.user_addon_scope
	grip = weapon.user_addon_grip

	config = UserWeaponConfig.objects.create(
		profile=profile,
		character=character,
		weapon=weapon,
		current=True,
		slot=slot,
	)

	config.stock = Stock.objects.get(pk=stock[0]) if stock else None
	config.barrel = Barrel.objects.get(pk=barrel[0]) if barrel else None
	config.muzzle = Muzzle.objects.get(pk=muzzle[0]) if muzzle else None
	config.mag = Mag.objects.get(pk=mag[0]) if mag else None
	config.scope = Scope.objects.get(pk=scope[0]) if scope else None
	config.grip = Grip.objects.get(pk=grip[0]) if grip else None
	config.save()


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

	user_config_slot1 = UserWeaponConfig.objects.filter(profile=user.profile, current=True, slot=0).first()
	user_config_slot2 = UserWeaponConfig.objects.filter(profile=user.profile, current=True, slot=1).first()

	if user_config_slot1:
		response['main_character'] = {
			"id": user_config_slot1.character.id,
			"tech_name": user_config_slot1.character.tech_name
		}
		response['weapon_first_slot'] = {
			"id": user_config_slot1.weapon.weapon_with_addons.weapon.id,
			"tech_name": user_config_slot1.weapon.weapon_with_addons.weapon.tech_name,
		}

		if user_config_slot1.stock:
			response['weapon_first_slot']['stock'] = {
				"id": user_config_slot1.stock.id,
				"tech_name": user_config_slot1.stock.tech_name
			}
		else:
			response['weapon_first_slot']['stock'] = None

		if user_config_slot1.barrel:
			response['weapon_first_slot']['barrel'] = {
				"id": user_config_slot1.barrel.id,
				"tech_name": user_config_slot1.barrel.tech_name
			}
		else:
			response['weapon_first_slot']['barrel'] = None

		if user_config_slot1.muzzle:
			response['weapon_first_slot']['muzzle'] = {
				"id": user_config_slot1.muzzle.id,
				"tech_name": user_config_slot1.muzzle.tech_name
			}
		else:
			response['weapon_first_slot']['muzzle'] = None

		if user_config_slot1.mag:
			response['weapon_first_slot']['mag'] = {
				"id": user_config_slot1.mag.id,
				"tech_name": user_config_slot1.mag.tech_name
			}
		else:
			response['weapon_first_slot']['mag'] = None

		if user_config_slot1.scope:
			response['weapon_first_slot']['scope'] = {
				"id": user_config_slot1.scope.id,
				"tech_name": user_config_slot1.scope.tech_name
			}
		else:
			response['weapon_first_slot']['scope'] = None

		if user_config_slot1.grip:
			response['weapon_first_slot']['grip'] = {
				"id": user_config_slot1.grip.id,
				"tech_name": user_config_slot1.grip.tech_name
			}
		else:
			response['weapon_first_slot']['grip'] = None

	else:
		start_weapons_first_slot = Weapon.objects.filter(start=True, hidden=False, slot=0)
		response['start_weapons_first_slot'] = [
			{"id": weapon.id, "tech_name": weapon.tech_name} for weapon in start_weapons_first_slot
		]

	if user_config_slot2:
		response['main_character'] = {
			"id": user_config_slot2.character.id,
			"tech_name": user_config_slot2.character.tech_name
		}
		response['weapon_second_slot'] = {
			"id": user_config_slot2.weapon.weapon_with_addons.weapon.id,
			"tech_name": user_config_slot2.weapon.weapon_with_addons.weapon.tech_name,
		}

		if user_config_slot2.stock:
			response['weapon_second_slot']['stock'] = {
				"id": user_config_slot2.stock.id,
				"tech_name": user_config_slot2.stock.tech_name
			}
		else:
			response['weapon_second_slot']['stock'] = None

		if user_config_slot2.barrel:
			response['weapon_second_slot']['barrel'] = {
				"id": user_config_slot2.barrel.id,
				"tech_name": user_config_slot2.barrel.tech_name
			}
		else:
			response['weapon_second_slot']['barrel'] = None

		if user_config_slot2.muzzle:
			response['weapon_first_slot']['muzzle'] = {
				"id": user_config_slot2.muzzle.id,
				"tech_name": user_config_slot2.muzzle.tech_name
			}
		else:
			response['weapon_second_slot']['muzzle'] = None

		if user_config_slot2.mag:
			response['weapon_second_slot']['mag'] = {
				"id": user_config_slot2.mag.id,
				"tech_name": user_config_slot2.mag.tech_name
			}
		else:
			response['weapon_second_slot']['mag'] = None

		if user_config_slot2.scope:
			response['weapon_second_slot']['scope'] = {
				"id": user_config_slot2.scope.id,
				"tech_name": user_config_slot2.scope.tech_name
			}
		else:
			response['weapon_second_slot']['scope'] = None

		if user_config_slot2.grip:
			response['weapon_first_slot']['grip'] = {
				"id": user_config_slot2.grip.id,
				"tech_name": user_config_slot2.grip.tech_name
			}
		else:
			response['weapon_second_slot']['grip'] = None
	else:
		start_weapons_second_slot = Weapon.objects.filter(start=True, hidden=False, slot=1)
		response['start_weapons_second_slot'] = [
			{"id": weapon.id, "tech_name": weapon.tech_name} for weapon in start_weapons_second_slot
		]

	# Check if main character appeared, or user has at least one, if both False, return start characters list
	if 'main_character' not in response.keys():
		user_character = UserCharacter.objects.filter(profile=user.profile)
		if user_character:
			response['main_character'] = {
				"id": user_character.first().id,
				"tech_name": user_character.first().tech_name
			}
		else:
			start_characters = Character.objects.filter(default=True, hidden=False)
			response['start_characters'] = [
				{"id": item.id, "tech_name": item.tech_name} for item in start_characters
			]
	return response
