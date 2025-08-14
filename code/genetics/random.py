import combat
import random
from combat.combat import show_member_actions
from combat.automatized_combat import automatized_combat

def start_combat_random(party_members, enemy):
    #random actions only in makoto it's the only one that can be controlled
    makoto = party_members[0]
    actions= makoto.list_of_actions
    print("Starting combat with random actions...")

    #a list of 50 actions is created 
    random_actions = random.choices(actions, k=50)
    print ("Random actions generated for combat.")
    print(random_actions)

    finished = automatized_combat(party_members, enemy, random_actions)

    if finished:
        print("Combat finished with a win.")
        return True
    else:
        print("Combat finished with a loss.")
        return False
        
        





    
