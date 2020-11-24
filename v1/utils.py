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

	user_config_slot1 = UserWeaponConfig.objects.filter(profile=user.profile, current=True, slot=0)
	user_config_slot2 = UserWeaponConfig.objects.filter(profile=user.profile, current=True, slot=1)

	if user_config_slot1:
		response['main_character'] = {
			"id": user_config_slot1.character.id,
			"tech_name": user_config_slot1.character.tech_name
		}
		response['weapon_first_slot'] = {
			"id": user_config_slot1.weapon.weapon_with_addons.weapon.id,
			"tech_name": user_config_slot1.weapon.weapon_with_addons.weapon.tech_name
		}
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
			"tech_name": user_config_slot2.weapon.weapon_with_addons.weapon.tech_name
		}
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
				"id": user_character.first().character.id,
				"tech_name": user_character.first().character.tech_name
			}
		else:
			start_characters = Character.objects.filter(default=True, hidden=False)
			response['start_characters'] = [
				{"id": item.character.id, "tech_name": item.character.tech_name} for item in start_characters
			]
	return response
