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
    result = automatized_combat(party_members, enemy, list_of_actions)

    if result["won"]:
        return 100
    else:
        return 0
    
def fitness_test_1(list_of_actions): # si en el automatized_combat.py no se indican los turnos maximos queda en bucle infinito!!!!
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    
    stats = automatized_combat(party_members, enemy, list_of_actions)
    if not stats["won"]:
        return 0 #If it loses, fitness 0
    turn_score = 1000 / stats["turns"]  # Less turns = better
    damage_score = stats["damage_done"] / enemy.max_HP  # Percentage of damage
    death_penalty = 500 * stats["deaths"]  # Penalty for deaths
    
    fitness = turn_score + damage_score - death_penalty # Final fitness
    
    return min(1, fitness)

def fitness_test_ponderada(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    if not stats["won"]:
        return 0 # If it loses, fitness 0
    
    TURN_WEIGHT = 200 # peso por turnos
    DAMAGE_WEIGHT = 200 # peso por daños
    DEATH_PENALTY = 100 # peso por miembros de la party que han muerto
    
    base_score = 1000 # Base score for winning
    turn_score = (50 - min(stats["turns"], 50)) * TURN_WEIGHT  # max 50 turnos
    damage_bonus = stats["damage_done"] * DAMAGE_WEIGHT
    death_penalty = stats["deaths"] * DEATH_PENALTY
    fitness = base_score + turn_score + damage_bonus - death_penalty
    
    return min(1,fitness)