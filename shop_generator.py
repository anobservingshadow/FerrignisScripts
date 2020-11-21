# Script to generate a shop
from weapon_gen import generate_weapons
from sort_list import weapon_sort

async def weapon_shop(size=20,shopname="Unnamed Shop"):
    rawweaponlist = await generate_weapons(size)
    weaponlist = await weapon_sort(rawweaponlist)
    shoplist = []
    emp_str = ""
    trip_quote = '```'
    head_1 = 'Name'
    head_2 = 'Weapon Type'
    head_3 = 'Damage'
    head_4 = 'Effects'
    newline = "\n"
    rowcount = 1
    shoplist.append(trip_quote)
    shoplist.append(shopname)
    shoplist.append(f'   | {head_1:<15} | {head_2:<19} | {head_3:<6} | {head_4}')
    shoplist.append(f'{emp_str:-<92}')
    for weapon in weaponlist:
        shoplist.append(f'{rowcount:<3}| {weapon._names:<15} | {weapon._type:<19} | {weapon.damage:>6} | {", ".join(weapon._effects.split("newline"))}')
        rowcount += 1
    shoplist.append(trip_quote)
    shoptable = "\n".join(shoplist)
    return shoptable