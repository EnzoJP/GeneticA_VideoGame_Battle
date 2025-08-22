
#fitness functions 

def maximize_damage(stats):
    if not stats["won"]: # If it loses, fitness 0
        return 0
    return stats["damage_done"]

def minimize_damage_taken(stats):
    if not stats["won"]: # If it loses, fitness 0
        return 0
    return 1 / (1 + stats["damage_taken"]) # Normalize damage taken

def minimize_turns(stats):
    if not stats["won"]: # If it loses, fitness 0
        return 0
    return 1 / (1 + stats["turns"]) # Normalize turns taken

def combine_with_weights():
    pass