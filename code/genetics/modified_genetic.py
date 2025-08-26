from combat.automatized_combat import automatized_combat
from genetics.random import generate_random_actions, calculate_sp_cost
from genetics.model_genetic import evaluate, mutate, check_sp_cost
import genetics.fitnessF as fitnessF
import random
import copy

def genetic_combat_mod(party_members, enemy):
    #more adapted version and imporoved
    # crossover two points
    # cut all solutions once they win to the length + 1 (to compesate randomness of the fight ) of the winning solution
    #More elitism, drop the worst 10 and replace with the best 10 of the old population,and,
    #we keep the podium of all generations to the final result and compare them at the end
    #mutation probability improved to 20% to compesate elitism

    makoto  = party_members[0]
    actions = makoto.list_of_actions
    print("Starting combat with genetic algorithm modificated...")

    #poulation starting with 50 random actions
    population_size = 25
    population = [generate_random_actions(actions, 50, makoto) for _ in range(population_size)]

    actions_results = genetic_algorithm_mod(population, makoto)
    result = automatized_combat(party_members, enemy, actions_results[:])

    if result["won"]:
        print("Combat finished with a win.")
    else:
        print("Combat finished with a loss.")
    return result
    

def genetic_algorithm_mod(population,makoto):

    pop_long = len(population)
    old_population = [evaluate(ind) for ind in population]
    old_population.sort(key=lambda x: x[1], reverse=True)
    jsut_a_test = old_population[:]

    ##
    # #logic to cut here
    ####

    best_of_all_generations = old_population[:3]  #keep the podium

    for generation in range(30):  # number of generations
        new_population = []
        for i in range(pop_long):
            parent1,_ = random.choice(old_population)
            parent2,_ = random.choice(old_population)

            child = crossover_two_points(parent1, parent2,makoto)

            if random.random() < 0.20:  # mutation probability
                child = mutate(child,makoto)
                # check if the action sequence is valid in terms of SP cost
                child = check_sp_cost(child,makoto)
                new_population.append(evaluate(child))
            else:
                child = check_sp_cost(child,makoto)
                new_population.append(evaluate(child))
        #sort the new population based on fitness and check if there is a winner, if so cut all

        ####
        #logic to cut here
        #####
        
        new_population.sort(key=lambda x: x[1], reverse=True)
        #keep the podium
        best_of_all_generations = best_of_all_generations + new_population[:3]

        #elitism - drop the worst 10 and replace with the best 10 of the old population
        new_population = new_population[:pop_long - 10] + old_population[:10]
        old_population = copy.deepcopy(new_population)

    final_order = sorted(best_of_all_generations, key=lambda x: x[1], reverse=True)

    #print the fitness for debugging
    for ind, fit in final_order:
        print(f"Fitness: {fit}")

    for ind, fit in jsut_a_test:
        print(f"Just a test Fitness: {fit}")

    return final_order[0][0]  # return the best action sequence

            

def cut_it_All(population, index, makoto):
    new_population = []
    for ind, fit in population:
        cut_ind = ind[:index+1]
        new_population.append(evaluate(cut_ind))
    return new_population
    
def  crossover_two_points(parent1, parent2,makoto):
    #crossover between two parents to create a child action sequence using two points crossover
    #to solve duplicate items, we will keep the first time an item appears and mutate the duplicate
    #then we do the opposite and we compare the fitness of both.

    crossover_point1 = random.randint(0, len(parent1) - 1)
    crossover_point2 = random.randint(0, len(parent1) - 1)
    if crossover_point1 > crossover_point2:
        crossover_point1, crossover_point2 = crossover_point2, crossover_point1
    child = parent1[:crossover_point1] + parent2[crossover_point1:crossover_point2] + parent1[crossover_point2:]
    

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