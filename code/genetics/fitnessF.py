from combat.automatized_combat import automatized_combat
import combat.enemy as enemy1
import combat.party as party

#fitness functions 
#execute the automatic battle from a list of actions and return the fitness value

def maximize_damage(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    if not stats["won"]: # If it loses, fitness 0
        return 0
    return stats["damage_done"]

def minimize_damage_taken(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    if not stats["won"]: # If it loses, fitness 0
        return 0
    return 1 / (1 + stats["damage_taken"]) # Normalize damage taken

def minimize_turns(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    if not stats["won"]: # If it loses, fitness 0
        return 0
    return 1 / (1 + stats["turns"]) # Normalize turns taken

def combine_with_weights(list_of_actions):    
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    pass

def default_fitness(list_of_actions):
    #a simple combination between damage and turns
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    pass

def just_a_test_fitness(list_of_actions):
    #just a temporal fitness function to test the combat
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    win = automatized_combat(party_members, enemy, list_of_actions)

    if win == True:
        return 100
    else:
        return 0
    