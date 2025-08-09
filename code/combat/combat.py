import combat.enemy as enemy
import combat.party as party


def start_combat(party_members, enemy):
    print("Combat started!")

    pass


def simulate_combat(party_members, enemy):
    print("Simulating combat...")
    menu_finished = False
    while menu_finished == False:
        print("Select a algotithm to use for combat simulation:")

        print("1. Random")
        print("2. genetico")