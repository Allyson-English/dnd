import random
import time
from time import sleep
import sys

def dice_roll(num_of_sides: int):
    while True:
        try:
            player_roll = int(input("\nRoll a D{} and enter your result here: ".format(num_of_sides)))
        except ValueError:
            continue
        if player_roll > num_of_sides:
            print("Your response cannot be higher than {}.".format(num_of_sides))
            continue
        elif player_roll < 1:
            print("Your response cannot be a negative number.")
            continue
        else:
            break
    return player_roll

class Character:
    
    def __init__(self, name, armour, weapon, health, damageroll, narrative_options):
        self.name = name
        self.armour = armour
        self.weapon = weapon
        self.health = health
        self.damageroll = damageroll
        self.narrative_options = narrative_options
        self.alive = True 
        
    def narrative(self, message_type, villan):
        message = random.choice(self.narrative_options[message_type])
        message = message.replace("ENEMYWEAPON", villan.weapon).replace("PLAYERWEAPON", self.weapon.type_of_weapon).replace("ENEMY",villan.name)
        return message
    
    def narrative_full(self):
        for k in self.narrative_options.keys():
            print(k)

class Enemy:
    
    def __init__(self, name, armour, weapon, health, damageroll, narrative_options):
        self.name = name
        self.armour = armour
        self.weapon = weapon
        self.health = health
        self.damageroll = damageroll
        self.narrative_options = narrative_options
        self.alive = True 
        
    def narrative(self, message_type, hero):
        message = random.choice(self.narrative_options[message_type])
        message = message.replace("PLAYERWEAPON", hero.weapon.type_of_weapon).replace("ENEMYWEAPON", self.weapon).replace("ENEMY",self.name)
        return message  
    
    def narrative_full(self):
        for k in self.narrative_options.keys():
            print(k)
            
class BattleTool:
    
    def __init__(self, weapon_dict):
        
        def weapon_chosen(weapon_dict: dict):
            
            print("\nTravelers should always be ready for battle, to choose your weapon:", end=' ') 
            wep_choice = dice_roll(len(weapon_dict))
            type_of_weapon, damage_capacity = weapon_dict.get(wep_choice)
            print("\nA {} deals {} in damage and can be a great tool in the hands of a wise fighter.".format(type_of_weapon, damage_capacity))
            print("In the hands of a fool, however, it can be incredibly dangerous.") 
            print("Use it well.")
            return type_of_weapon, damage_capacity
        
        self.type_of_weapon, self.damage_capacity = weapon_chosen(weapon_dict)
    

weapon_dict = {1: ('great sword', 8), 2: ('hand axe', 6), 3: ('double axe', 6), 4: ('lucerne hammer',8), 5: ('voulge', 10), 6: ('war hammer', 8),
                7: ('great sword', 8), 8: ('short sword', 6), 9: ('dagger', 6), 10: ('war scythe', 8), 11: ('rapier', 8), 12: ('lance', 10),
                13: ('great sword', 8), 14: ('lucerne hammer', 8), 15: ('war scythe', 8),16: ('short sword', 6), 17: ('lance', 10), 
                  18: ('great sword', 8), 19: ('long sword', 8), 20: ('long sword', 8)
              }

def user_input(players_choice: list):
    """
    allowed_responses has to be a list of strings.
    """
    allowed_responses_lower = []
    for s in players_choice:
        allowed_responses_lower.append(s.lower())
        
    while True:
        response = str(input('\nType your response here:')).lower()
        if not response in allowed_responses_lower:
            print('{} not allowed. Please answer with either "Yes" or "No".'.format(response))
        else:
            break
    return response


def enemy_strike(villan, hero):  
    enemy_hit = random.randint(1, 20)
    
    if enemy_hit > hero.armour:
        damage = villan.damageroll
        print(f"\nThe {villan.name} rolls {enemy_hit}, dealing {damage} in damage.\n")
        hero.health -= damage
        time.sleep(1) 

        if hero.health <= 0:
            print(hero.narrative('HHealth_Dead', villan))
            hero.alive = False
            return 

        elif 0 < hero.health <= 9:
            print(hero.narrative('HHealth_Below_9', villan))
            time.sleep(1) 

        elif 9 < hero.health:
            print(hero.narrative('HHealth_Above_9', villan))
            time.sleep(1) 
    else:
        print(f"\nThe {villan.name} rolls {enemy_hit}-- a miss!\n")
        print(hero.narrative('EWhiff', villan))
        time.sleep(1) 

def player_strike(hero, villan):
    print("\nBegin your attack!\n")
    player_hit = dice_roll(20)
    
    if player_hit > enemy.armour:
        damage = dice_roll(hero.damageroll)
        print("\nYour attack is successful and you deal {} in damage.\n".format(damage))
        villan.health -= damage
        time.sleep(1) 
        if villan.health <= 0:
            print(villan.narrative('EHEALTH_DEAD', hero))
            villan.alive = False
            return 
        elif 0 < villan.health <= 9:
            print(villan.narrative('EHEALTH_Below_9', hero))
            time.sleep(1) 
        elif 9 < villan.health:
            print(villan.narrative('EHEALTH_Above_9', hero))
            time.sleep(1) 
    else:
        
        print(villan.narrative('HWhiff', hero))
        time.sleep(1) 

def battle_sequence(villan, hero):
    
    print(f"\nAs you reach for your {hero.weapon.type_of_weapon} and prepare to fight, roll to see who will get the first strike.\n", end='')
    time.sleep(1) 
    
    enemy_initiative = random.randint(1, 20)
    player_initiative = dice_roll(20)
    
    time.sleep(1) 
    
    if player_initiative >= enemy_initiative:
        
        print(f"\n{hero.name} wins the initiative roll.\n")
        
        while hero.alive and villan.alive:
            player_strike(hero, villan)
            if not villan.alive:
                return
            enemy_strike(villan, hero)
            if not hero.alive:
                return
            
    else:
        print(f"\nThe {enemy.name} wins the initiative roll.")
        
        while hero.alive and villan.alive:
            enemy_strike(villan, hero)
            if not hero.alive:
                return
            player_strike(hero, villan)  
            if not villan.alive:
                return

enemy_narrative = {

   'EHEALTH_Below_9':
     ["The ENEMY absorbs the blow but is moving slowly... you can tell that victory is close.",
      "As your strike lands, you can tell that that the ENEMY is badly hurt.",
      "Your PLAYERWEAPON strikes the ENEMY directly and you smile, realizing that victory may be within your grasp.",
      "The ENEMY lets out a terrible gurgle as your PLAYERWEAPON makes a direct hit. Perhaps this skirmish won't be so challenging, after all.",
      "As your PLAYERWEAPON makes contact, you can tell the ENEMY is hurt."],
        
   'EHEALTH_Above_9':
    ["The ENEMY is surprisingly nimble and though you make contact with your PLAYERWEAPON, you wonder whether you may be outskilled.",
     "Your hits seem to wash off the ENEMY like water and they continue attacking with the a terrifying strength.",
     "Though there is sweat on your brow but you feel energized by the knowledge that winning is within your power.",
      f"Your clear skill with a PLAYERWEAPON shines through and you hope this skirmish will end soon."],

   'EHEALTH_DEAD': 
     ["The ENEMY buckles under the blow from your PLAYERWEAPON. For a moment, you remain on edge, waiting for another attack, until you realize.. you've won.",
     "The ENEMY falls, defeated. This battle wasn't easy and you breathe a sight of relief that it's over."],

    'HWhiff':
    ["You're quick on your feet but perhaps your could work on your dexterity... your lunge completely misses the ENEMY.",
         "Your attack misses the ENEMY and you stumble a bit trying to regain your composure. Better luck next time.",
         "You whiff! As you work to regain composure, you wonder whether your skills have deserted you."], 
}

player_narrative = {
    
    'HHealth_Above_9':
        ["The enemy strikes but the blow rolls off of you-- this clearly isn't your first battle and you intend to win.",
         "The blow hits but it's nothing you can't handle. You quickly brush it off and prepare to strike.",
         "'Hardly scratched me,' you think to yourself as you quickly recompose yourself.",
         "You feel the ENEMYWEAPON strike, knocking the wind out of you. Your eyes blur but you hurry to regain composure and make a hit before they strike again.",
         "Your arms ache but you think you just may be getting the upper hand and you push onwards, determined to win."],
    
    'HHealth_Below_9':
        ["The blow isn't fatal, but you're badly hurt and wonder if you can handle much more of this.",
         "Your wounds are severe and it requires every last ounce of energy to continue on.",
         "You're hurt, but you keep fighting-- recognizing that at this point, you have no other choice but to win",
         "You feel the strike of the ENEMYWEAPON and you know you've been hurt.",
         "The shock of the blow reverberates through you-- the strike costs you in health points and you wonder how much more of this you can handle.",
         "'That'll hurt in the morning,' you think to yourself... if you make it morning, that is.",
         "Pain radiates through your limbs but you press onwards, determined to make it out of this alive."],

    'HHealth_Dead':
        [f"Suddenly, time seems to slow and your strength is all but gone. You stumble forward, collapsing before the ENEMYWEAPON. It's over.",
         f"As soon as you feel the strike of the ENEMYWEAPON, you can tell it's over. The grip on your PLAYERWEAPON is lost and you can feel yourself dropping."],

    'EWhiff':
        ["The ENEMY is no match for you and you quickly sidestep their ENEMYWEAPON.",
        "You're a bit frazzled but easily avoid the ENEMYWEAPON as it lurches towards you."]}
        
def quit_game():    
    print("\n\nEnd of Game")
    print("\n\nThank you for playing AirDnD!\n\n")
    response = str(input('\nWould you like to play again?\n')).lower()
    
    end_game = ['quit', 'q', 'no']
    continue_game = ['yes', 'y', 'continue', 'play again']
    
    while True:
        if response in end_game:
            sys.exit("Open the file at any time to play again.")
            return
        elif response in continue_game:
            enemies = [Enemy("Orc", 9, "great axe", 12, 6, enemy_narrative), Enemy("Ogre", 14, "bludgeon", 16, 8, enemy_narrative)]
            enemy = random.choice(enemies)
            play_game(weapon_dict, enemy)
        else:
            sys.exit("Open the file at any time to play again.")


def play_game(weapon_dict, enemy):
    print('\n\n\nWelcome to Air DnD, a virtual game edition of dungeons and dragons.\n\nMake sure you have a set of dice before beginning this game. \n\nAs you work your way through the story, you will be prompted to engage with each situation you encounter and will have to input your rolls.\n\nTo begin, please enter your name below.')
    print("(Remember to hit 'Enter' after inputting your responses.)\n")

    player_name = input()
    sleep(.5)
    print("\nWelcome, {}!".format(player_name))
    
    weapon = BattleTool(weapon_dict)
    
    health, armour = 16, 14
    
    player = Character(player_name, armour, weapon, health, weapon.damage_capacity, player_narrative)    

    print("\nAlong with your {}, you begin this game with {} health points and an armour class of {}.".format(weapon.type_of_weapon,health,armour))
    sleep(5)
    print("\nAnd now", end='')
    print('.', end='')
    sleep(.4)
    print('.', end='')
    sleep(.4)    
    print('.', end='')     
    sleep(.4)  
    print("\n\nThis game begins just after sunrise in the town of Calydon.")
    sleep(3)
    print("\nYou're a ranger traveling without companions, drawn to these lands from the stories you've read about in lore.")
    sleep(3)
    print("\nSome say that treasures are hidden here.")
    sleep(3)
    print("\nOthers say that terrible beasts await any wayward travelers.") 
    sleep(3)
    print("\nOne thing is for certain, you can't waste the whole day away at your campsite!")
    sleep(3)
    print("\nWhat do you say, {}, are you ready for an adventure? (Type Yes or No)".format(player_name))
    
    yes_list = ['yes', 'hell yes', 'hell  yeah', 'yeah', 'hell yeah', 'duh']
    no_list = ['n', 'no', 'hell no', 'nah', 'no way', "that's guna be a no for me dog"]
    ready_for_adventure = user_input(yes_list + no_list)
            
    if ready_for_adventure in yes_list:
        print("\nGreat! Let's go.")
    elif ready_for_adventure in no_list:
        print("\nAdventures aren't for the faint of heart, get some rest and maybe you'll be ready tomorrow.")
        

    print("\nWhile passing through one of the small, sleepy towns along your journey, you recall overhearing a few of the locals discussing some strange things happening recently.")
    sleep(3)
    print("\nYou can't be quite sure... but you're almost positive you heard one of them mention a mysterious case of glowing ruins near the foot of the mountains.")
    sleep(3)
    print("\nYou're no expert in sourcery but you suspect something so extraordinarily strange must have something to do with a very dark kind of magic.")
    sleep(3)
    print("\nYou also suspect that whomever could get to the bottom of this mysterious happening just might be eligible for a hefty reward from the town Mayor.")
    sleep(3)
    print("\nAs the sun creeps higher into the sky, you decide it might be worth your while to head towards the mountain and try to learn something.")
    sleep(3)    
    print("\nAs you climb over dense terrain, the forest slowly gives way to towering boulders. Up ahead, you see the an opening between two boulders that you suspect may be the entrance to a cave.")
    sleep(3)
    print(f"\nAll of a sudden, something lurches out from behind a nearby rock-- an {enemy.name}!")
    
    battle_sequence(enemy, player)
    
    quit_game()


enemies = [
    Enemy("Orc", 9, "great axe", 12, 6, enemy_narrative),
    Enemy("Ogre", 14, "bludgeon", 16, 8, enemy_narrative),
#     Enemy("Necromancer", 18, "staff", 30, 10, enemy_narrative)
]

enemy = random.choice(enemies)

play_game(weapon_dict, enemy)
