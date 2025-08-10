import combat
import random
from combat.combat import show_status, show_member_actions

def start_combat_random(party_members, enemy):
    #random actions 
    #the order is Makoto, Sleeping table, Yukari, Akihiko, Junpei
    print("Combat started!")
    protagonist = party_members[0]
    fight_list = [protagonist, enemy] + party_members[1:]
    while enemy.HP > 0 and protagonist.HP > 0:
        for member in fight_list:
            show_status(party_members, enemy)
            if member.HP <= 0:
                print(f"{member.name} has fallen!")
                continue #skip turn if dead
            if member == enemy:
                attack = enemy.attacks_rate(party_members)
                if attack == "basic_attack":
                    enemy.basic_attack()
                elif attack == "maragidyne":
                    enemy.maragidyne()
                elif attack == "hamaon":
                    enemy.hamaon()
                elif attack == "magidola":
                    enemy.magidola()
                elif attack == "evil_touch":
                    enemy.evil_touch()
                elif attack == "ghastly_wail":
                    enemy.ghastly_wail()
                continue #skip turn

            if member.status != "normal":
                if member.status == "fear":
                    print(f"{member.name} is too scared to act!")
                    continue
                continue

            if member == protagonist: 
                print(f"{member.name}'s turn:")
                action = random.choice(member.list_of_actions)
                print(f"{member.name} uses {action}!")
                getattr(member, action)()
                
            if member != protagonist:
                #pseudo_aleatorias they follow tactics
                print(f"{member.name}'s turn:")
                if member.name == "Yukari":
                    pass
                if member.name == "Akihiko":
                    pass
                if member.name == "Junpei":
                    pass


    if enemy.HP <= 0:
        print("Victory! The enemy has been defeated.")

    if protagonist.HP <= 0:
        print(f"{protagonist.name} has fallen! Game Over.")