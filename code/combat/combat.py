import combat.enemy as enemy
import combat.party as party


def start_combat(party_members, enemy):
    #the order is Makoto, Sleeping table, Yukari, Akihiko, Junpei
    # only makoto can decide the attack the others are Pseudo-random
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
                print("Select an action:")
                selection_choice = False
                while selection_choice == False:
                    show_member_actions(member)
                    choice = input("Enter your choice: ")
                    if choice.isdigit() and 1 <= int(choice) <= len(member.list_of_actions):
                        action = member.list_of_actions[int(choice) - 1]
                        getattr(member, action)() # call the method by name
                        selection_choice = True
                    else:
                        print("Invalid choice. Please try again.")

            if member != protagonist:
                ##pseudo_aleatorias they follow tactics
                print(f"{member.name}'s turn:")
                print("Select an action:")

                if member.name == "Yukari":
                    actions = member.list_of_actions

                elif member.name == "Akihiko":
                    actions = member.list_of_actions

                elif member.name == "Junpei":
                    actions = member.list_of_actions
                    
    if enemy.HP <= 0:
        print(f"{enemy.name} Victory!, The enemy has been defeated!")
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
        print("Select a algotithm to use for combat simulation:")

        print("1. Random")
        print("2. genetico modelo")
        print("3. genetico modificado")
        print("4. NGSA-II")

        choice = input("Enter your choice (1-4): ")

        if choice in ['1', '2', '3', '4']:
            if choice == '1':
                import genetics.random as random_algo
                random_algo.start_combat_random(party_members, enemy)
            menu_finished = True
        else:
            print("Invalid choice. Please try again.")
        

