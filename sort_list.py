# Script to take in item lists according to specific parameters and sort them into a list according to a standardised order.

from weapon_gen import generate_weapon,classlist

# Weapon sorting
#   Function to sort things according to their names
async def weapon_sort(weapon_list):
    WeaponClasses = [[],[],[],[],[],[]]
    for weapon in weapon_list:
        # classlist = [lightweapon,sword,heavyweapon,poleweapon,rangedlight,ranged]
        # sorts weapons into various weapon classes
        if isinstance(weapon,classlist[0]):
            WeaponClasses[0].append(weapon)
        if isinstance(weapon,classlist[1]):
            WeaponClasses[1].append(weapon)
        if isinstance(weapon,classlist[2]):
            WeaponClasses[2].append(weapon)
        if isinstance(weapon,classlist[3]):
            WeaponClasses[3].append(weapon)
        if isinstance(weapon,classlist[4]):
            WeaponClasses[4].append(weapon)
        if isinstance(weapon,classlist[5]):
            WeaponClasses[5].append(weapon)
    for WClass in WeaponClasses:
        WClass.sort(key=lambda weapon: weapon._damage["dice"]*weapon._damage["dmg"])
        WClass.sort(key=lambda weapon: weapon._names)
    return [weapon for WClass in WeaponClasses for weapon in WClass]
