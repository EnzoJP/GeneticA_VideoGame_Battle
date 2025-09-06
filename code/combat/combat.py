import combat.enemy as enemy1
import combat.party as party
import random
import combat.metrics_and_plots as metrics
from concurrent.futures import ThreadPoolExecutor
import time
import numpy as np
import matplotlib.pyplot as plt
import os

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

def print_results(name, losses, wins, win_rate, avg_turns, std_turns, avg_damage_done, std_damage_done, avg_damage_taken, std_damage_taken, avg_deaths, std_deaths, elapsed_time):
    # Show results -> stats
    print(f"\n=== {name} Results ===")
    print(f"Wins: {wins}, Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Average Turns: {avg_turns:.2f} ± {std_turns:.2f}")
    print(f"Average Damage Done: {avg_damage_done:.2f} ± {std_damage_done:.2f}")
    print(f"Average Damage Taken: {avg_damage_taken:.2f} ± {std_damage_taken:.2f}")
    print(f"Average Deaths: {avg_deaths:.2f} ± {std_deaths:.2f}")
    print(f"Total Time: {elapsed_time:.4f} seconds")
    print(f"Average Time per Simulation: {elapsed_time/50:.6f} seconds")
    
# Compare algorithms and make plots
def compare_all_algorithms(n_simulations=10, save_plots=False):
    algorithms = {
        'Random': run_random_simulation,
        'Model Genetic': run_simulation,
        'Modified Genetic': run_simulation_modified_genetic,
        'NSGA-II': run_simulation_ngsa2
    }
    results = {}
    
    for algo_name, algo_func in algorithms.items():
        print(f"\n=== Ejecutando {algo_name} ===")
        
        wins = 0
        turns_list = []
        turns_won_list = []  # Nueva lista para turnos de partidas ganadas
        damage_done_list = []
        damage_taken_list = []
        deaths_list = []
        base_seed = 33
        start_time = time.time()
        
        for i in range(n_simulations):
            result = algo_func(base_seed + i)
            
            if result["won"]:
                wins += 1
                turns_won_list.append(result["turns"])  # Solo agregar si ganó
            turns_list.append(result["turns"])
            damage_done_list.append(result["damage_done"])
            damage_taken_list.append(result["damage_taken"])
            deaths_list.append(result["deaths"])
        
        win_rate = metrics.calculate_win_rate(wins, n_simulations - wins)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Calculate stats
        avg_turns = np.mean(turns_list)
        std_turns = np.std(turns_list)
        avg_damage_done = np.mean(damage_done_list)
        std_damage_done = np.std(damage_done_list)
        avg_damage_taken = np.mean(damage_taken_list)
        std_damage_taken = np.std(damage_taken_list)
        avg_deaths = np.mean(deaths_list)
        std_deaths = np.std(deaths_list)

        # Show results
        print_results(algo_name, n_simulations - wins, wins, win_rate, avg_turns, std_turns, 
                     avg_damage_done, std_damage_done, avg_damage_taken, std_damage_taken, 
                     avg_deaths, std_deaths, elapsed_time)

        # Save results for plots
        results[algo_name] = {
            'turns': turns_list,
            'turns_won': turns_won_list,  # Nuevo campo para turnos de partidas ganadas
            'damage_done': damage_done_list,
            'damage_taken': damage_taken_list,
            'deaths': deaths_list,
            'win_rate': win_rate
        }
    
    # Make directory for plots if it doesn't exist
    plot_dir = "comparison_plots"
    if save_plots and not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    
    # Generate comparative plots
    if save_plots:
        metrics.create_all_comparative_plots(results, plot_dir)
        print(f"\nGráficos guardados en el directorio: {plot_dir}")
    else:
        metrics.create_all_comparative_plots(results)
    
    return results


def simulate_combat(party_members, enemy):
    print("Simulating combat...")
    menu_finished = False
    while menu_finished == False:
        print("Select an algorithm to use for combat simulation:")

        print("1. Random")
        print("2. model genetic")
        print("3. modified genetic")
        print("4. NGSA-II")
        print("5. Compare all algorithms")

        choice = input("Enter your choice (1-5): ")

        if choice in ['1', '2', '3', '4','5']:
            if choice == '1':
                import genetics.random as random_algo
                wins = 0
                losses = 0
                turns_list = []
                damage_done_list = []
                damage_taken_list = []
                deaths_list = []
                base_seed = 33
                start_time = time.time()
                
                for i in range(100):
                    random.seed(base_seed + i)
                    enemy = enemy1.Enemy()
                    Makoto = party.Makoto()
                    Yukari = party.Yukari()
                    Akihiko = party.Akihiko()
                    Junpei = party.Junpei()
                    party_members = [Makoto, Yukari, Akihiko, Junpei]
                    result = random_algo.start_combat_random(party_members, enemy)
                    
                    if result["won"]:
                        wins += 1
                    else:
                        losses += 1
                    turns_list.append(result["turns"])
                    damage_done_list.append(result["damage_done"])
                    damage_taken_list.append(result["damage_taken"])
                    deaths_list.append(result["deaths"])
                
                win_rate = metrics.calculate_win_rate(wins, losses)
                end_time = time.time()
                elapsed_time = end_time - start_time

                # Calculate stats
                avg_turns = np.mean(turns_list)
                std_turns = np.std(turns_list)
                avg_damage_done = np.mean(damage_done_list)
                std_damage_done = np.std(damage_done_list)
                avg_damage_taken = np.mean(damage_taken_list)
                std_damage_taken = np.std(damage_taken_list)
                avg_deaths = np.mean(deaths_list)
                std_deaths = np.std(deaths_list)
                print_results("Random Algorithm", losses, wins, win_rate, avg_turns, std_turns, avg_damage_done, std_damage_done, avg_damage_taken, std_damage_taken, avg_deaths, std_deaths, elapsed_time)
                
                
            elif choice == '2':
                wins = 0
                losses = 0
                turns_list = []
                damage_done_list = []
                damage_taken_list = []
                deaths_list = []
                base_seed = 33
                start_time = time.time()
                
                for i in range(100):
                    result = run_simulation(base_seed + i)
                    
                    if result["won"]:
                        wins += 1
                    else:
                        losses += 1
                    turns_list.append(result["turns"])
                    damage_done_list.append(result["damage_done"])
                    damage_taken_list.append(result["damage_taken"])
                    deaths_list.append(result["deaths"])
                
                win_rate = metrics.calculate_win_rate(wins, losses)
                end_time = time.time()
                elapsed_time = end_time - start_time

                # Calculate stats
                avg_turns = np.mean(turns_list)
                std_turns = np.std(turns_list)
                avg_damage_done = np.mean(damage_done_list)
                std_damage_done = np.std(damage_done_list)
                avg_damage_taken = np.mean(damage_taken_list)
                std_damage_taken = np.std(damage_taken_list)
                avg_deaths = np.mean(deaths_list)
                std_deaths = np.std(deaths_list)

                print_results("Model Genetic Algorithm", losses, wins, win_rate, avg_turns, std_turns, avg_damage_done, std_damage_done, avg_damage_taken, std_damage_taken, avg_deaths, std_deaths, elapsed_time)
                
            elif choice == '3':
                wins = 0
                losses = 0
                turns_list = []
                damage_done_list = []
                damage_taken_list = []
                deaths_list = []
                base_seed = 33
                start_time = time.time()
                
                for i in range(100):
                    result = run_simulation_modified_genetic(base_seed + i)
                    
                    if result["won"]:
                        wins += 1
                    else:
                        losses += 1
                    turns_list.append(result["turns"])
                    damage_done_list.append(result["damage_done"])
                    damage_taken_list.append(result["damage_taken"])
                    deaths_list.append(result["deaths"])
                
                win_rate = metrics.calculate_win_rate(wins, losses)
                end_time = time.time()
                elapsed_time = end_time - start_time

                # Calculate stats
                avg_turns = np.mean(turns_list)
                std_turns = np.std(turns_list)
                avg_damage_done = np.mean(damage_done_list)
                std_damage_done = np.std(damage_done_list)
                avg_damage_taken = np.mean(damage_taken_list)
                std_damage_taken = np.std(damage_taken_list)
                avg_deaths = np.mean(deaths_list)
                std_deaths = np.std(deaths_list)

                print_results("Modified Genetic Algorithm", losses, wins, win_rate, avg_turns, std_turns, avg_damage_done, std_damage_done, avg_damage_taken, std_damage_taken, avg_deaths, std_deaths, elapsed_time)
                
            elif choice == '4':
                wins = 0
                losses = 0
                turns_list = []
                damage_done_list = []
                damage_taken_list = []
                deaths_list = []
                base_seed = 33
                start_time = time.time()
                
                for i in range(100):
                    result = run_simulation_ngsa2(base_seed + i)
                    
                    if result["won"]:
                        wins += 1
                    else:
                        losses += 1
                    turns_list.append(result["turns"])
                    damage_done_list.append(result["damage_done"])
                    damage_taken_list.append(result["damage_taken"])
                    deaths_list.append(result["deaths"])
                
                win_rate = metrics.calculate_win_rate(wins, losses)
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # Calculate stats
                avg_turns = np.mean(turns_list)
                std_turns = np.std(turns_list)
                avg_damage_done = np.mean(damage_done_list)
                std_damage_done = np.std(damage_done_list)
                avg_damage_taken = np.mean(damage_taken_list)
                std_damage_taken = np.std(damage_taken_list)
                avg_deaths = np.mean(deaths_list)
                std_deaths = np.std(deaths_list)

                print_results("NSGA-II Algorithm", losses, wins, win_rate, avg_turns, std_turns, avg_damage_done, std_damage_done, avg_damage_taken, std_damage_taken, avg_deaths, std_deaths, elapsed_time)
            
            menu_finished = True
            if choice == '5':
                # Compare all algorithms
                save_plots = input("¿Guardar gráficos? (y/n): ").lower() == 'y'
                n_simulations = int(input("Número de simulaciones por algoritmo: ") or "10")
                compare_all_algorithms(n_simulations, save_plots)
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
    return ngsa_ii_algo.genetic_combat_nsga2(party_members, enemy,seed)

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
    
    
    
