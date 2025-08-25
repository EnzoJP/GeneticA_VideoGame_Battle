from combat.automatized_combat import automatized_combat
from genetics.random import generate_random_actions, calculate_sp_cost
import genetics.fitnessF as fitnessF
import random
import copy

def genetic_combat(party_members, enemy):
    
    makoto  = party_members[0]
    actions = makoto.list_of_actions
    print("Starting combat with genetic algorithm...")

    #poulation starting with 50 random actions

    population_size = 25
    population = [generate_random_actions(actions, 50, makoto) for _ in range(population_size)]

    actions_results = genetic_algorithm(population, makoto)
    result = automatized_combat(party_members, enemy, actions_results[:])

    if result["won"]:
        print("Combat finished with a win.")
    else:
        print("Combat finished with a loss.")
    return result
    
def genetic_algorithm(population,makoto):
    # this is the implementation of the genetic algorithm in AIMA book, adapted for our combat scenario
    """return the best action sequence from the population"""
    
    pop_long = len(population)
    old_population = [evaluate(ind) for ind in population]
    old_population.sort(key=lambda x: x[1], reverse=True)
    jsut_a_test = old_population[:]

    for generation in range(30):  # number of generations
        new_population = []
        for i in range(pop_long): # make the new ones
            
            parent1,_ = random.choice(old_population)
            parent2,_ = random.choice(old_population)

            child = crossover(parent1, parent2,makoto)

            if random.random() < 0.10:  # mutation probability
                child = mutate(child,makoto)
                # check if the action sequence is valid in terms of SP cost
                child = check_sp_cost(child,makoto)
                new_population.append(evaluate(child))
            else:
                child = check_sp_cost(child,makoto)
                new_population.append(evaluate(child))

        #sort the new population based on fitness 
        new_population.sort(key=lambda x: x[1], reverse=True)
        
        # drop the worst 10 and replace with the best 10 of the old population (elitism)
        new_population = new_population[:pop_long - 10] + old_population[:10]

        old_population = copy.deepcopy(new_population)
    
    final_order = sorted(old_population, key=lambda x: x[1], reverse=True)

    #print the fitness for debugging
    for ind, fit in final_order:
        print(f"Fitness: {fit}")

    for ind, fit in jsut_a_test:
        print(f"Just a test Fitness: {fit}")

    return final_order[0][0]  # return the best action sequence

def  crossover(parent1, parent2,makoto):
    #crossover between two parents to create a child action sequence using one point crossover
    #to solve duplicate items, we will keep the first time an item appears and mutate the duplicate
    #then we do the opposite and we compare the fitness of both.

    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]

    # check for duplicate items
    actions = makoto.list_of_actions
    items = ["Soma", "Precious Egg", "Magic Mirror"]

    if child.count("Soma") > 1 or child.count("Precious Egg") > 1 or child.count("Magic Mirror") > 1:

        posible_actions = [action for action in actions if action not in items]
        #keep the first time an item appears and mutate the duplicate
        child1= copy.deepcopy(child)
        temporary_items = []
        for i in range(len(child1)):
            if child1[i] in items:
                if child1[i] in temporary_items:
                    new_action = random.choice(posible_actions)
                    while new_action == "Soma" or new_action == "Precious Egg" or new_action == "Magic Mirror":
                        new_action = random.choice(posible_actions)
                    child1[i] = new_action
                else:
                    temporary_items.append(child1[i])

        
        fitness1 = fitnessF.fitness_test_1(child1[:])

        #do the opposite, keep the last time an item appears and mutate the previous ones
        child2 = copy.deepcopy(child)
        temporary_items = []

        for i in range(len(child2)-1, -1, -1):
            if child2[i] in items:
                if child2[i] in temporary_items:
                    new_action = random.choice(posible_actions)
                    while new_action == "Soma" or new_action == "Precious Egg" or new_action == "Magic Mirror":
                        new_action = random.choice(posible_actions)
                    child2[i] = new_action
                else:
                    temporary_items.append(child2[i])

        
        fitness2 = fitnessF.fitness_test_1(child2[:])

        if fitness1 > fitness2:
            return child1
        else:
            return child2

    else:   
        return child
    
def mutate(action_sequence,makoto):
    #mutate the action sequence by changing a random action, not items because it's difficult to track 
    mutation_point = random.randint(0, len(action_sequence) - 1)
    actions = makoto.list_of_actions
    new_action = random.choice(actions)
    while new_action == "Soma" or new_action == "Precious Egg" or new_action == "Magic Mirror":
        new_action = random.choice(actions)
    action_sequence_new = copy.deepcopy(action_sequence)
    action_sequence_new[mutation_point] = new_action
    return action_sequence_new
    

def check_sp_cost(list_actions, makoto):
    # check if the action sequence is valid in terms of SP cost
    # if the SP cost of the actions is less than the SP amount
    # check cutting the list in every iteration to see when we have to use the reserved item ("Precious Egg")
    actions = copy.deepcopy(list_actions)
    for i in range(len(actions)):
        if actions[i] == "Soma" or actions[i] == "Precious Egg" or actions[i] == "Magic Mirror":
            continue
        if actions[i] == "basic_attack":
            continue
        sp_cost = calculate_sp_cost(actions[:i+1])
        if sp_cost > makoto.SP:
            # if the SP cost is greater than the SP amount, we have to use the reserved item
            if "Precious Egg" not in actions:
                actions.insert(i, "Precious Egg")
        else:
            continue
    return actions




def evaluate(ind):
    #evaluate an stores the fitness of an individual,avoiding multiple evaluations
    return (ind, fitnessF.fitness_test_1(ind[:]))