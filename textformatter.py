# For formatting text

textlist = []
emp_str = ""
trip_quote = '```'
#head_1 = 'Name'
#head_2 = 'Weapon Type'
#head_3 = 'Damage'
#head_4 = 'Effects'
newline = "\n"
rowcount = 1
textlist.append(trip_quote)
#textlist.append(f'   | {head_1:<15} | {head_2:<19} | {head_3:<6} | {head_4:<30}')
textlist.append(f'{emp_str:-<92}')
#for weapon in weaponlist:
#    textlist.append(f'{rowcount:<3}| {weapon._names:<15} | {weapon._type:<19} | {weapon.damage:>6} | {", ".join(weapon._effects.split("newline")):<40}')
#    rowcount += 1
textlist.append(f'|{"BBBBB     OOOO    U     U  N   N  TTTTTTTT  Y     Y":^90}|')
textlist.append(f'|{" B    B   O    O   U     U  NN  N     TT      Y   Y  ":^90}|')
textlist.append(f'|{"BBBBB   O      O  U     U  N N N     TT        Y   ":^90}|')
textlist.append(f'|{"B    B   O    O   U     U  N  NN     TT        Y   ":^90}|')
textlist.append(f'|{"BBBBB     OOOO     UUUUU   N   N     TT        Y   ":^90}|')
textlist.append(f'{emp_str:-<92}')
textlist.append(f'|{"  Dangerous creature sighted at the woods near the edge of town. Capable of casting ":<90}|')
textlist.append(f'|{"  magic, observed creating a mist that causes armour and flesh to dissolve. No further":<90}|')
textlist.append(f'|{"  information known. Melee combat inadvisable.":<90}|')
textlist.append(f'|{"  Handsome reward offered. Head required as proof.":<90}|')
textlist.append(f'{emp_str:-<92}')
textlist.append(trip_quote)
formattedtext = "\n".join(textlist)
print(formattedtext)