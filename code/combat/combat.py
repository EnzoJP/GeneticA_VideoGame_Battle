import combat.enemy as enemy1
import combat.party as party
import random
import combat.metrics_and_plots as metrics
from concurrent.futures import ThreadPoolExecutor
import time

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


def start_combat(party_members, enemy):
    #the order is Makoto, Sleeping table, Yukari, Akihiko, Junpei
    # only makoto can decide the attack the others are Pseudo-random (defined tactics)
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
                print("Select an action:")
                selection_choice = False
                while selection_choice == False:
                    show_member_actions(member)
                    choice = input("Enter your choice: ")
                    print("-------------------------------------------------------------------")
                    if choice.isdigit() and 1 <= int(choice) <= len(member.list_of_actions):
                        action = member.list_of_actions[int(choice) - 1]
                        if action in ["recarm","mediarama", "use_item"]:
                            getattr(member, action)(party_members) # calls with party_members as parameter 
                        elif action in ["bufula", "hamaon","rakunda"]:
                            getattr(member, action)(enemy) # calls with enemy as parameter
                        elif action in ["basic_attack", "torrent_shot"]:
                            getattr(member,action)(enemy, party_members) #calls with enemy and party as parameters
                        selection_choice = True
                    else:
                        print("Invalid choice. Please try again.")

            if protagonist.HP <= 0:
                break

            if member != protagonist:
                # pseudo_random (they follow tactics)
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
                elif action_name in ["basic_attack", "torrent_shot","blade_of_fury", "sonic_punch"]:
                    getattr(member, action_name)(enemy, party_members)
                else:
                    getattr(member, action_name)(enemy)
            
        effects_turns(party_members, enemy)

    if enemy.HP <= 0:
        print("Victory!, The enemy has been defeated!")
    if protagonist.HP <= 0:
        print(f"{protagonist.name} has fallen! Game Over.")

    


def show_status(party_members, enemy):
    print("Party Status:")
    for member in party_members:
        print(f"{member.name} - HP: {member.HP}, SP: {member.SP}, Status: {member.status}")
    print(f"Enemy: {enemy.name} - HP: {enemy.HP}, SP: {enemy.SP}, Status: {enemy.status}")
    print("---------------------")


def show_member_actions(member):
    # Display the actions available for the member
    print(f"{member.name}'s actions:")
    for action in member.list_of_actions:
        print(member.list_of_actions.index(action) + 1, action)


    

def simulate_combat(party_members, enemy):
    print("Simulating combat...")
    menu_finished = False
    while menu_finished == False:
        print("Select an algorithm to use for combat simulation:")

        print("1. Random")
        print("2. model genetic")
        print("3. modified genetic")
        print("4. NGSA-II")

        choice = input("Enter your choice (1-4): ")

        if choice in ['1', '2', '3', '4']:
            if choice == '1':
                import genetics.random as random_algo
                wins = 0
                losses = 0
                average_turns = 0
                base_seed = 33
                start_time = time.time()
                results = []
                for i in range(50):
                    random.seed(base_seed + i)
                    enemy = enemy1.Enemy()
                    Makoto = party.Makoto()
                    Yukari = party.Yukari()
                    Akihiko = party.Akihiko()
                    Junpei = party.Junpei()
                    party_members = [Makoto, Yukari, Akihiko, Junpei]
                    result = random_algo.start_combat_random(party_members, enemy)
                    results.append(result)
                for result in results:
                    if result["won"]:
                        wins += 1
                        average_turns += result["turns"]
                    else:
                        losses += 1
                print(f"wins: {wins}, losses: {losses}")
                win_rate = metrics.calculate_win_rate(wins, losses)
                average_turns = average_turns / wins if wins > 0 else 0
                average_turns = round(average_turns)
                print (f"Average turns for random algorithm: {average_turns}")
                print  (f"Win rate for random algorithm: {win_rate}%")
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time elapsed: {elapsed_time:.2f} seconds")

            elif choice == '2':
                wins = 0
                losses = 0
                average_turns = 0
                base_seed = 33
                start_time = time.time()
                results = [run_simulation(base_seed + i) for i in range(10)]

                for result in results:
                    if result["won"]:
                        wins += 1
                        average_turns += result["turns"]
                    else:
                        losses += 1
                print(f"wins: {wins}, losses: {losses}")
                average_turns = average_turns / wins if wins > 0 else 0
                average_turns = round(average_turns)
                print (f"Average turns for model genetic algorithm: {average_turns}")
                win_rate = metrics.calculate_win_rate(wins, losses)
                print(f"Win rate for model genetic algorithm: {win_rate}%")
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time elapsed: {elapsed_time:.2f} seconds")

            elif choice == '3':
                import genetics.modified_genetic as modified_genetic
                wins = 0
                losses = 0
                average_turns = 0
                base_seed = 33
                start_time = time.time()
                results = [run_simulation_modified_genetic(base_seed + i) for i in range(3)]

                for result in results:
                    if result["won"]:
                        wins += 1
                        average_turns += result["turns"]
                    else:
                        losses += 1
                print(f"wins: {wins}, losses: {losses}")
                average_turns = average_turns / wins if wins > 0 else 0
                average_turns = round(average_turns)
                print (f"Average turns for modified genetic algorithm: {average_turns}")
                win_rate = metrics.calculate_win_rate(wins, losses)
                print(f"Win rate for modified genetic algorithm: {win_rate}%")
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time elapsed: {elapsed_time:.2f} seconds")

            elif choice == '4':
                import genetics.NGSA_ii as ngsa_ii_algo
                wins = 0
                losses = 0
                average_turns = 0
                base_seed = 33
                start_time = time.time()
                results = [ngsa_ii_algo.genetic_combat_nsga2(party_members, enemy) for i in range(2)]
                for result in results:
                    if result["won"]:
                        wins += 1
                        average_turns += result["turns"]
                    else:
                        losses += 1
                print(f"wins: {wins}, losses: {losses}")
                average_turns = average_turns / wins if wins > 0 else 0
                average_turns = round(average_turns)
                print (f"Average turns for NGSA-II algorithm: {average_turns}")
                win_rate = metrics.calculate_win_rate(wins, losses)
                print(f"Win rate for NGSA-II algorithm: {win_rate}%")
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time elapsed: {elapsed_time:.2f} seconds")
    
            menu_finished = True
  
        else:
            print("Invalid choice. Please try again.")
        

def run_simulation(seed):
    random.seed(seed)
    import genetics.model_genetic as model_genetic_algo
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    return model_genetic_algo.genetic_combat(party_members, enemy)


def run_simulation_modified_genetic(seed):
    random.seed(seed)
    import genetics.modified_genetic as modified_genetic_algo
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    return modified_genetic_algo.genetic_combat_mod(party_members, enemy)

def run_simulation_ngsa2(seed):
    random.seed(seed)
    import genetics.NGSA_ii as ngsa_ii_algo
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    return ngsa_ii_algo.genetic_combat_nsga2(party_members, enemy)

def run_random_simulation(seed):
    random.seed(seed)
    import genetics.random as random_algo
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    return random_algo.start_combat_random(party_members, enemy)
    
    
    
