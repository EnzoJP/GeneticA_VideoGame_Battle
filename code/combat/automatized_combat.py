import random
import combat.enemy as enemy
import combat.party as party
import random
import combat.metrics_and_plots as metrics
from combat.combat import show_member_actions, show_status

def effects_turns(party_members, enemy):
    # Party buffs
    for m in party_members:
        # defense buff
        if hasattr(m, "def_buff_turns") and m.def_buff_turns > 0:
            m.def_buff_turns -= 1
            if m.def_buff_turns == 0:
                print(f"{m.name}'s defense buff has worn off.")
        # attack buff
        if hasattr(m, "atk_buff_turns") and m.atk_buff_turns > 0:
            m.atk_buff_turns -= 1
            if m.atk_buff_turns == 0:
                print(f"{m.name}'s attack buff has worn off.")
        # evasion buff
        if hasattr(m, "ev_buff_turns") and m.ev_buff_turns > 0:
            m.ev_buff_turns -= 1
            if m.ev_buff_turns == 0:
                print(f"{m.name}'s evasion buff has worn off.")

    # Enemy debuffs
    if hasattr(enemy, "def_debuff_turns") and enemy.def_debuff_turns > 0:
        enemy.def_debuff_turns -= 1
        if enemy.def_debuff_turns == 0:
            print(f"{enemy.name}'s defense debuff has worn off.")
    if hasattr(enemy, "atk_debuff_turns") and enemy.atk_debuff_turns > 0:
        enemy.atk_debuff_turns -= 1
        if enemy.atk_debuff_turns == 0:
            print(f"{enemy.name}'s attack debuff has worn off.")



def automatized_combat(party_members, enemy,list_of_actions):
    #simulate combat, list of actions is the list of makoto's actions
    """returns the boolean result of the combat"""
    print("Starting automatized combat...")

    protagonist = party_members[0]
    fight_list = [protagonist, enemy] + party_members[1:]
    while enemy.HP > 0 and protagonist.HP > 0:
        for member in fight_list:
            if protagonist.HP <= 0:
                return False
            show_status(party_members, enemy)
            if member.HP <= 0:
                print(f"{member.name} has fallen!")
                continue #skip turn if dead
            if member == enemy:
                if enemy.status != "normal":
                    print(f"{enemy.name} is affected by {enemy.status} and cannot act!")
                    enemy.status = "normal" # reset status after missing a turn
                    continue
                attack = enemy.attacks_rate(party_members)
                if attack == "basic_attack":
                    enemy.basic_attack(party_members)
                elif attack == "maragidyne":
                        # check if the members are not under magic mirror
                        if any(m.reflect is not None for m in party_members):
                            # if the member is under magic mirror, skip their turn
                            print(f"{member.name} uses maragidyne!")
                            print("The party is under Magic Mirror!")
                            # the enemy skips their turn and reset the reflect status of the party
                            for m in party_members:
                                if m.reflect is not None:
                                    m.reflect = None
                            #for each memeber the enemy takes a small amount of damage between 40-60
                            for m in party_members:
                                if m.HP > 0 and m != enemy:
                                    damage = random.randint(40, 60)
                                    enemy.HP -= damage
                                    print(f"{enemy.name} takes {damage} damage from the enemy's maragidyne!")
                            continue
                        else:
                            enemy.maragidyne(party_members)
                elif attack == "hamaon":
                    print(f"{member.name} uses hamaon!")
                    if any(m.reflect is not None for m in party_members):
                        print("The attack was reflected but is not effective!")
                        for m in party_members:
                            if m.reflect is not None:
                                m.reflect = None
                        continue
                    else:
                        enemy.hamaon(party_members)
                elif attack == "megidola":
                    print(f"{member.name} uses megidola!")
                    if any(m.reflect is not None for m in party_members):
                        print("the party is under Magic Mirror!")
                        for m in party_members:
                            if m.reflect is not None:
                                m.reflect = None
                        for m in party_members:
                            if m.HP > 0 and m != enemy:
                                damage = random.randint(40, 60)
                                enemy.HP -= damage
                                print(f"{enemy.name} takes {damage} damage from the enemy's megidola!")
                        continue
                    else:
                        enemy.megidola(party_members)
                elif attack == "evil_touch":
                    enemy.evil_touch(party_members)
                elif attack == "ghastly_wail":
                    enemy.ghastly_wail(party_members)
                continue #skip turn


            if member.status != "normal":
                if member.status == "fear":
                    print(f"{member.name} is too scared to act!")
                    continue
                continue

            if member == protagonist:
                print(f"{member.name}'s turn:")
                
                if len(list_of_actions) == 0:
                    print("No more actions left for the protagonist!")
                    return False
                action = list_of_actions.pop(0)  # get the next action from the list
                print(f"{member.name} uses {action}!")
                
                print("-------------------------------------------------------------------")
                if action in ["recarm","mediarama"]:
                    getattr(member, action)(party_members) # calls with party_members as parameter 
                elif action in ["bufula", "hamaon", "rakunda"]:
                    getattr(member, action)(enemy) # calls with enemy as parameter
                elif action in ["basic_attack", "torrent_shot"]:
                    getattr(member,action)(enemy, party_members) #calls with enemy and party as parameters
                elif action in ["Soma", "Precious Egg", "Magic Mirror"]:
                    if action == "Soma":
                        member.use_item_auto(party_members, "Soma")
                    elif action == "Precious Egg":
                        member.use_item_auto(party_members, "Precious Egg")
                    elif action == "Magic Mirror":
                        member.use_item_auto(party_members, "Magic Mirror")
                
            

            if protagonist.HP <= 0:
                return False

            if member != protagonist:
                # pseudo_aleatorias (they follow tactics)
                print(f"{member.name}'s turn:")

                action_name = member.choose_action(party_members, enemy)
                
                if action_name in ["recarm", "mediarama", "me_patra", "marakukaja", "sukunda"]:
                    getattr(member, action_name)(party_members)
                elif action_name in ["rakukaja", "diarama"]:
                    # Select random ally
                    valid_allies = [ally for ally in party_members if ally.status != "fallen"]
                    if valid_allies:
                        target = random.choice(valid_allies)
                        getattr(member, action_name)(target)
                    else:
                        print("No valid targets! Skipping turn.")
                elif action_name in ["basic_attack", "torrent_shot", "blade_of_fury", "sonic_punch"]:
                    getattr(member, action_name)(enemy, party_members)
                else:
                    getattr(member, action_name)(enemy)

        effects_turns(party_members, enemy)
            

        

    if enemy.HP <= 0:
        return True
    if protagonist.HP <= 0:
        return False
    

