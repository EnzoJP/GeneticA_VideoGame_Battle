import combat.enemy as enemy
import combat.party as party
import combat.combat as combat

def main():
    sleeping_table = enemy.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()

    party_list = [Makoto, Yukari, Akihiko, Junpei]

    print ("Welcome to the Sleeping table combat!")
    print ("Select options:")
    print ("----------------------")
    menu_finished = False
    while menu_finished == False:
        print ("1. Start Combat")
        print ("2. Simulate combat and print results")
        print ("3. Exit")
        print ("---------------------")
        choice = input("Enter your choice: ")

        if choice == "1":
            combat.start_combat(party_list,sleeping_table)
            menu_finished = True
        elif choice == "2":
            combat.simulate_combat(party_list,sleeping_table)
        elif choice == "3":
            print("Exiting the game.")
            menu_finished = True
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    print("Starting the game...")




