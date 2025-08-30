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
    random_actions = generate_random_actions(actions, 50,makoto)
    #print ("Random actions generated for combat.")
    #print(random_actions)

    finished = automatized_combat(party_members, enemy, random_actions)

    print(random_actions)

    if finished["won"]:
        print("Combat finished with a win.")
    else:
        print("Combat finished with a loss.")
    
    return finished
        
def generate_random_actions(actions, num_actions,makoto):
    #generate a list of random actions but it has to be legal
    #in terms of items, only we allow items that are in the inventory(1-Soma,2-Precious Egg,1-Magic Mirror)
    #insted of using "use_item" we use the name of the item
    #one Precious Egg is reserved for the protagonist if he is without sp

    random_actions = []
    random_without_items = []
    items_avaliable = ["Soma", "Precious Egg", "Magic Mirror"]
    random_without_items = actions[:]
    random_without_items.remove("use_item")
    #print(f"Items available: {items_avaliable}")
    for i in range(num_actions):
        action = random.choice(actions)
        if action == "use_item" and len(items_avaliable) != 0 : # if there are items available
            print("Using an item...")
            item = random.choice(items_avaliable)
            random_actions.append(item)
            items_avaliable.remove(item)  # avoid using it again
        else:
            action = random.choice(random_without_items)
            random_actions.append(action)

    # if the SP cost of the actions is less than the SP amount
    # check cutting the list in every iteration to see when we have to use the reserved item
    
    for i in range(len(random_actions)):
        if random_actions[i] == "Soma" or random_actions[i] == "Precious Egg" or random_actions[i] == "Magic Mirror":
            continue
        if random_actions[i] == "basic_attack":
            continue
        sp_cost = calculate_sp_cost(random_actions[:i+1])
        if sp_cost > makoto.SP:
            # if the SP cost is greater than the SP amount, we have to use the reserved item
            if "Precious Egg" not in random_actions:
                random_actions.insert(i, "Precious Egg")
        else:
            continue
        
    
    print(f"Final action sequence (length {len(random_actions)}): {random_actions}")
    return random_actions
            


def calculate_sp_cost(actions):
    # Calculate the total SP cost of the actions
    sp_cost = 0
    for action in actions:
        if action == "bufula":
            sp_cost += 8
        elif action == "hamaon":
            sp_cost += 12
        elif action == "recarm":
            sp_cost += 20
        elif action == "mediarama":
            sp_cost += 16
        elif action == "rakunda":
            sp_cost += 6

    return sp_cost
    
