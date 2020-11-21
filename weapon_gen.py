from numpy import random
from random import randint
# Light weapons - includes knives, daggers, cutlery, and other small weapons. Dice range is X = 2-6 and Y = 2-3 at base. Can be thrown under certain conditions with penalty -1 to Y
# Swords - basic one-handed bladed weapons, whether curved or straight. Dice range is X = 1-2 and Y = 4-6 at base. Can be used with shield.
#Heavy weapons - includes warhammers of all kinds, two-handed swords, axes, scythes, etc. Dice range is X = 1-2 and Y = 6-8. Decreases Strength requirement to cause knockback and/or armour breaking.
# Pole weapons - includes spears, glaives, and the like. Dice range is X = 1 and Y = 8-12. Piercing attacks can ignore armour below the strength level of the user.
# Ranged light weapons - throwing daggers and the like. Dice range is X = 1-3 and Y = 2-3 at base. No penalty when used in melee, limited throwing range.
# Ranged weapons - bows, crossbows, etc. Dice range is X = 1-3 and Y = 3-6 at base. Cannot be used in melee and requires accuracy roll.
# [Name]
# Type:
# Damage:
# Effects:
# Requirements:
# Description:
# Stats: [Constitution, Vitality, Precision, Perception, Attunement]
# effects = ['Poison','Burn','Freeze','Unsettle','Terrify',Paralyse','Sedate','Confuse','Curse','Purge']

weapon_stats = {'Light Weapon':("CON",2,6,2,3), 'Sword':("CON",1,2,4,6), 'Heavy Weapon':("CON",1,2,6,8), 'Pole Weapon':("CON",1,1,8,12), 'Ranged Light Weapon':("PREC",1,3,2,3), 'Ranged Weapon':("PREC",1,3,3,6)}
effects = {"stat":["CON","VIT","PREC","PRCP","ATT"],"skill":["Attack","Defense","Ally Buff","Anti-Enemy Buff"],"inflict":["Poison","Burn","Freeze","Terrify","Paralyse","Sedate","Curse","Purge"]}

def damage_gen(mindie,maxdie,mindmg,maxdmg):
    dicerange = range(mindie,maxdie+1)
    dmgrange = range(mindmg,maxdmg+1)
    dice = random.choice(dicerange)
    dmg = random.choice(dmgrange)
    return dice,dmg

def rarity_req(mid,damage):
    if damage <= mid:
        return random.choice(range(1,5))
    else:
        return random.choice(range(5,8))

def effect_gen():
    primes = [13,11,7,5,3,2]
    checkind = 0
    checknum = primes[checkind]
    gen_num = randint(1,99999999)
    effectlist = []
    while gen_num % checknum == 0:
        effect = random.choice(list(effects.keys()),p=[0.2,0.2,0.6])
        if effect == "stat":
            effectlist.append(random.choice(effects["stat"])+" +"+str(randint(2,7)))
        elif effect == "skill":
            effectlist.append(random.choice(effects["skill"])+" Skill")
        elif effect == "inflict":
            effectlist.append("Inflicts "+random.choice(effects["inflict"]))
        checkind += 1
        checknum *= primes[checkind]
        gen_num = randint(1,99999999)
    if effectlist:
        return "\n".join(effectlist)
    else:
        return ""

class weapon:
    def __init__(self):
        self._damage = {'dice':0,'dmg':0}
        self._effects = ""
        self._requirements = {'CON':0,'VIT':0,'PREC':0,'PRCP':0,'ATT':0}
        self._description = ""
    def getDMG(self):
        return str(self._damage['dice'])+"d"+str(self._damage['dmg'])
    def setDMG(self,dice,dmg):
        if isinstance(dice, int) and isinstance(dmg,int):
            self._damage['dice'] = dice
            self._damage['dmg'] = dmg
    damage = property(getDMG,setDMG)
    def getEffects(self):
        return self._effects
    def setEffects(self,effect):
        if isinstance(effect,str):
            self._effects = effect
    def delEffects(self):
        self._effects = None
    def getReqs(self):
        reqlist = []
        for req in self._requirements:
            if self._requirements[req] > 0:
                reqlist.append(req+" "+str(self._requirements[req]))
        if reqlist:
            reqlist.sort()
            reqlist.insert(0,"To Equip:")
            return "\n".join(reqlist)
        else:
            return "None"
    def setReqs(self,CON=0,VIT=0,PREC=0,PRCP=0,ATT=0):
        reqlist = [CON,VIT,PREC,PRCP,ATT]
        safecheck = 1
        for item in reqlist:
            if isinstance(item,int):
                continue
            else:
                safecheck = 0
        attributes = ['CON','VIT','PREC','PRCP','ATT']
        if safecheck:
            for index in range(reqlist):
                self._requirements[attributes[index]] = reqlist[index]
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self,desc):
        if isinstance(desc,str):
            self._description = desc
    @description.deleter
    def description(self):
        self._description = None
        
class lightweapon(weapon):
    def __init__(self):
        super().__init__()
        self._names = random.choice(["Dirk","Dagger","Knife","Kris","Stiletto","Cinquedea","Pugio","Tanto","Katar"])
        self._type = "Light Weapon"
        dice,dmg = damage_gen(2,6,2,3)
        super().setDMG(int(dice),int(dmg))
        self._requirements[weapon_stats["Light Weapon"][0]] = rarity_req((weapon_stats["Light Weapon"][2]*weapon_stats["Light Weapon"][4])/2,dice*dmg)
        self._effects = effect_gen()
    def __repr__(self):
        buildstring = [self._names,"Type: "+self._type,"Damage: "+self.getDMG(),self._effects,self.getReqs(),"Description:\n"+self._description]
        return "\n".join(item for item in buildstring if item)

class sword(weapon):
    def __init__(self):
        super().__init__()
        self._names = random.choice(["Sword","Scimitar","Katana","Bolo","Khanda","Xiphos","Falchion","Rapier","Saber","Spatha","Baston","Jian"])
        self._type = "Sword"
        dice,dmg = damage_gen(1,2,4,6)
        super().setDMG(int(dice),int(dmg))
        self._requirements[weapon_stats["Sword"][0]] = rarity_req((weapon_stats["Sword"][2]*weapon_stats["Sword"][4])/2,dice*dmg)
        self._effects = effect_gen()
    def __repr__(self):
        buildstring = [self._names,"Type: "+self._type,"Damage: "+self.getDMG(),self._effects,self.getReqs(),"Description:\n"+self._description]
        return "\n".join(item for item in buildstring if item)

class heavyweapon(weapon):
    def __init__(self):
        super().__init__()
        self._names = random.choice(["Mace","Morning Star","Bearded Axe","Sledgehammer","War Hammer","Quarterstaff","Bardiche","Macahuitl","Halberd","Monk's Spade","Bec de Corbin"])
        self._type = "Heavy Weapon"
        dice,dmg = damage_gen(1,2,6,8)
        super().setDMG(int(dice),int(dmg))
        self._requirements[weapon_stats["Heavy Weapon"][0]] = rarity_req((weapon_stats["Heavy Weapon"][2]*weapon_stats["Heavy Weapon"][4])/2,dice*dmg)
        self._effects = effect_gen()
    def __repr__(self):
        buildstring = [self._names,"Type: "+self._type,"Damage: "+self.getDMG(),self._effects,self.getReqs(),"Description:\n"+self._description]
        return "\n".join(item for item in buildstring if item)

class poleweapon(weapon):
    def __init__(self):
        super().__init__()
        self._names = random.choice(["Dory","Pike","Ahlspiess","Yari","Naginata","Iklwa","Lance","Fork","Saintie","Qiang","Hasta"])
        self._type = "Pole Weapon"
        dice,dmg = damage_gen(1,1,8,12)
        super().setDMG(int(dice),int(dmg))
        self._requirements[weapon_stats["Pole Weapon"][0]] = rarity_req((weapon_stats["Pole Weapon"][2]*weapon_stats["Pole Weapon"][4])/2,dice*dmg)
        self._effects = effect_gen()
    def __repr__(self):
        buildstring = [self._names,"Type: "+self._type,"Damage: "+self.getDMG(),self._effects,self.getReqs(),"Description:\n"+self._description]
        return "\n".join(item for item in buildstring if item)

class rangedlight(weapon):
    def __init__(self):
        super().__init__()
        self._names = random.choice(["Chakram","Kunai","Mambele","Dart","Throwing Knife","Bolas","Shuriken"])
        self._type = "Ranged Light Weapon"
        dice,dmg = damage_gen(1,3,2,3)
        super().setDMG(int(dice),int(dmg))
        self._requirements[weapon_stats["Ranged Light Weapon"][0]] = rarity_req((weapon_stats["Ranged Light Weapon"][2]*weapon_stats["Ranged Light Weapon"][4])/2,dice*dmg)
        self._effects = effect_gen()
    def __repr__(self):
        buildstring = [self._names,"Type: "+self._type,"Damage: "+self.getDMG(),self._effects,self.getReqs(),"Description:\n"+self._description]
        return "\n".join(item for item in buildstring if item)

class ranged(weapon):
    def __init__(self):
        super().__init__()
        self._names = random.choice(["Daikyu","Gakgun","Arbalest","Crossbow","Revolver","Blunderbuss","Musket","Kestros"])
        self._type = "Ranged Weapon"
        dice,dmg = damage_gen(1,3,3,6)
        super().setDMG(int(dice),int(dmg))
        self._requirements[weapon_stats["Ranged Weapon"][0]] = rarity_req((weapon_stats["Ranged Weapon"][2]*weapon_stats["Ranged Weapon"][4])/2,dice*dmg)
        self._effects = effect_gen()
    def __repr__(self):
        buildstring = [self._names,"Type: "+self._type,"Damage: "+self.getDMG(),self._effects,self.getReqs(),"Description:\n"+self._description]
        return "\n".join(item for item in buildstring if item)

classlist = [lightweapon,sword,heavyweapon,poleweapon,rangedlight,ranged]

async def generate_weapon():
    new_weapon = random.choice(classlist)()
    return new_weapon

async def generate_weapons(x):
    weaponlist = []
    for number in range(x):
        weaponlist.append(random.choice(classlist)())
    return weaponlist