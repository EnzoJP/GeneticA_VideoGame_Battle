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

def minimize_damage_taken1(list_of_actions):
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

def minimize_damage_taken2(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    turns = stats["turns"]
    if not stats["won"]: # If it loses, fitness 0
        return None,0
    return turns,(1 / (1 + stats["damage_taken"])) # Normalize damage taken

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
    
def fitness_test_1(list_of_actions):
    #returns only the fitness value
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    
    stats = automatized_combat(party_members, enemy, list_of_actions)

    won = 1 if stats["won"] else 0
    turns = stats["turns"]
    damage = stats["damage_done"]
    deaths = stats["deaths"]

    """we start with a huge number and we subtract points for more turns and deaths and add points for damage done"""

    if won:
        enemy_max_hp = enemy.max_HP
        return 1000000 - turns*1000 - deaths*100 + (damage / enemy_max_hp) 
    else:
        return damage - deaths*10 - turns #only we care about damage and deaths


def fitness_with_weights2(list_of_actions):
    ########################

    #must return turns,fitness if won else None,fitness !

    #####################
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



def fitness_test_2(list_of_actions):
    #same to 1 but returns the turns if won also
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    
    
    stats = automatized_combat(party_members, enemy, list_of_actions)

    won = 1 if stats["won"] else 0
    turns = stats["turns"]
    damage = stats["damage_done"]
    deaths = stats["deaths"]
    

    """we start with a huge number and we subtract points for more turns and deaths and add points for damage done"""

    if won:
        enemy_max_hp = enemy.max_HP
        return turns,(1000000 - turns*1000 - deaths*100 + (damage / enemy_max_hp))
    else:
        return None,(damage - deaths*10 - turns  ) #only we care about damage and deaths  



def fitness_with_weights1(list_of_actions):
    ########################

    #must NOT return turns!!!

    #####################
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

def best_fitness(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]

    stats = automatized_combat(party_members, enemy, list_of_actions)

    # --- 1) if loose -> fitness very low
    if not stats["won"]:

        return -1000 + (stats["damage_done"] / enemy.max_HP) * 500 - stats["deaths"] * 50

    # --- 2) if won -> 
    # calculate score 
    turn_score   = 1 - (stats["turns"] / 50)         #
    death_score  = 1 - (stats["deaths"] / 4)         
    damage_score = stats["damage_done"] / enemy.max_HP  
    hp_bonus     = (1 - stats["damage_taken"] / (4*Makoto.max_HP)) 

    # wheights
    W_TURN   = 0.4
    W_DEATH  = 0.99
    W_DAMAGE = 0.2
    W_HP     = 0.1

    score = (
        10000   # big bonus for winning
        + W_TURN   * turn_score   * 1000
        + W_DEATH  * death_score  * 1000
        + W_DAMAGE * damage_score * 1000
        + W_HP     * hp_bonus     * 1000
    )

    return score

def best_fitness_2(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]

    stats = automatized_combat(party_members, enemy, list_of_actions)

    
    if not stats["won"]:

        return None,(-1000 + (stats["damage_done"] / enemy.max_HP) * 500 - stats["deaths"] * 50)


    turn_score   = 1 - (stats["turns"] / 50)         
    death_score  = 1 - (stats["deaths"] / 4)         
    damage_score = stats["damage_done"] / enemy.max_HP  
    hp_bonus     = (1 - stats["damage_taken"] / (4*Makoto.max_HP)) 

    # Pesos ajustables
    W_TURN   = 0.4
    W_DEATH  = 0.99
    W_DAMAGE = 0.2
    W_HP     = 0.1

    score = (
        10000   
        + W_TURN   * turn_score   * 1000
        + W_DEATH  * death_score  * 1000
        + W_DAMAGE * damage_score * 1000
        + W_HP     * hp_bonus     * 1000
    )

    return stats["turns"], score

def retur_stats(list_of_actions):
    enemy = enemy1.Enemy()
    Makoto = party.Makoto()
    Yukari = party.Yukari()
    Akihiko = party.Akihiko()
    Junpei = party.Junpei()
    party_members = [Makoto, Yukari, Akihiko, Junpei]
    stats = automatized_combat(party_members, enemy, list_of_actions)
    if not stats["won"]:
        damage = stats["damage_done"]
        deaths = stats["deaths"]
        #damage_taken = stats["damage_taken"]
        turns = stats["turns"]
        return False,damage,deaths,turns
    else:
        damage = stats["damage_done"]
        deaths = stats["deaths"]
        #damage_taken = stats["damage_taken"]
        turns = stats["turns"]
        return True,damage,deaths,turns
