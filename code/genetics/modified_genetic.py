from combat.automatized_combat import automatized_combat
from genetics.random import generate_random_actions, calculate_sp_cost
from genetics.model_genetic import mutate, check_sp_cost
import genetics.fitnessF as fitnessF
import random
import copy
import combat.enemy as enemy1
import combat.party as party

def genetic_combat_mod(party_members, enemy):
    #more adapted version and imporoved
    # crossover two points
    # cut all solutions once they win to the length of the winning solution
    #More elitism, drop the worst 10 and replace with the best 10 of the old population,and,
    #we keep the podium of all generations to the final result and compare them at the end, doing a mini tournament winrate test
    

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

    #comon sense, we want to avoid son silly actions in the begining
    population = comon_sense_start(population, makoto)
    global_min_index_to_cut = 50
    pop_long = len(population)
    min_index_to_cut = None
    old_population = []
    for ind in population:
        turns,fit_tup = evaluate2(ind)
        if turns is not None:
            if min_index_to_cut is None or turns < min_index_to_cut:
                if turns <= 15: #avoid too small sequences
                    min_index_to_cut = 15
                    global_min_index_to_cut = 15
                else:
                    min_index_to_cut = turns
                    global_min_index_to_cut = turns
        old_population.append(fit_tup)

    old_population.sort(key=lambda x: x[1], reverse=True)
    
    jsut_a_test = old_population[:]
    
    # cut and re-evaluate the population if there is a winner
    if global_min_index_to_cut is not None:
        old_population = cut_it_All(old_population[:], global_min_index_to_cut, makoto)
    
    best_of_all_generations = old_population[:3]  #keep the podium
        
       

    for generation in range(30):  # number of generations
        new_population = []
        for i in range(pop_long):
            parent1,_ = random.choice(old_population)
            parent2,_ = random.choice(old_population)

            child = crossover_two_points(parent1, parent2,makoto)

            if random.random() < 0.10:  # mutation probability
                child = mutate(child,makoto)
                child = comon_sense_child(child, makoto)
                # check if the action sequence is valid in terms of SP cost
                child = check_sp_cost(child,makoto)
                new_population.append(evaluate(child))
            else:
                child = comon_sense_child(child, makoto)
                child = check_sp_cost(child,makoto)
                new_population.append(evaluate(child))
        #sort the new population based on fitness and check if there is a winner, if so cut all
        new_population.sort(key=lambda x: x[1], reverse=True)

        for ind in new_population:
            turns,fit_tup = evaluate2(ind[0])
            if turns is not None:
                if global_min_index_to_cut is None or turns < global_min_index_to_cut:
                    if turns <= 15: #avoid too small sequences
                        global_min_index_to_cut = 15
                    else:
                        global_min_index_to_cut = turns

        if global_min_index_to_cut is not None:
            new_population = cut_it_All(new_population[:], global_min_index_to_cut, makoto)
            
        
        new_population.sort(key=lambda x: x[1], reverse=True)
        best_of_all_generations = best_of_all_generations + new_population[:3] #add the podium of this generation to the best of all generations
        

        #elitism - drop the worst 10 and replace with the best 10 of the old population
        new_population = new_population[:pop_long - 10] + old_population[:10]
        old_population = copy.deepcopy(new_population)

    best_of_all_generations = best_of_all_generations + new_population[:3] #add the last generation podium
    final_order = sorted(best_of_all_generations, key=lambda x: x[1], reverse=True)


    # test the best of all generations in a mini tournament to choose the best one
    tournament_candidates = final_order[:10]
    tournament_results = []
    for ind, fit in tournament_candidates:
        wins = 0
        for _ in range(25):  # best of 
            enemy = enemy1.Enemy()
            Makoto = party.Makoto()
            Yukari = party.Yukari()
            Akihiko = party.Akihiko()
            Junpei = party.Junpei()
            party_members = [Makoto, Yukari, Akihiko, Junpei]
            result = automatized_combat(party_members, enemy, ind[:])
            if result["won"]:
                wins += 1
        tournament_results.append((ind, wins))
    
    tournament_results.sort(key=lambda x: x[1], reverse=True)
    print("Tournament results:")
    #print(tournament_results)
    print(final_order)
    print(f"Global min index to cut: {global_min_index_to_cut}")

    #print the fitness for debugging
    for ind, fit in final_order:
        print(f"Fitness: {fit}")

    for ind, fit in jsut_a_test:
        print(f"Just a test Fitness: {fit}")

    
    #final desicion if a draw in the tournament, choose the one with better fitness
    if tournament_results[0][1] == tournament_results[1][1]:
        if fitnessF.best_fitness(tournament_results[0][0][:]) >= fitnessF.best_fitness(tournament_results[1][0][:]):
            return tournament_results[0][0]
        else:
            return tournament_results[1][0]
    else:
        return tournament_results[0][0]

    

def cut_it_All(population, index, makoto):
    #cut all the action sequences to the index given and re-evaluate them
    new_population = []
    for ind, fit in population:
        if len(ind) <= index or index <= 15: #avoid too small sequences
            new_population.append((ind, fit))
        else:
            new_ind = ind[:index]
            _,tuple_fit = evaluate2(new_ind)
            new_population.append(tuple_fit)
            
            
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
    actions = [act for act in actions if act != "use_item"]
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

        
        fitness1 = fitnessF.best_fitness(child1[:])

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

        
        fitness2 = fitnessF.best_fitness(child2[:])

        if fitness1 > fitness2:
            return child1
        else:
            return child2

    else:   
        return child
    

def evaluate2(ind):
    #evaluate the individual using the fitness function,avoiding multiple evaluation, and using turns
    turns,fit = fitnessF.best_fitness_2(ind[:])
    return turns,(ind, fit)


def evaluate(ind):
    #evaluate the individual using the fitness function,avoiding multiple evaluation
    fit = fitnessF.best_fitness(ind[:])
    return (ind, fit)

def comon_sense_start(population, makoto):
    #avoid silly actions in the begining like using items of mana or basic attack aat the start
    new_population = []
    for ind in population:
        new_ind = ind[:]
        for i in range(10):  # first 10 actions
            if new_ind[i] == "use_item" or new_ind[i] == "Precious Egg" or new_ind[i] == "basic_attack" or new_ind[i] == "hamaon" or new_ind[i] == "torrent_shot":
                new_action = random.choice(makoto.list_of_actions)
                while new_action == "use_item" or new_action == "Precious Egg" or new_action == "basic_attack":
                    new_action = random.choice(makoto.list_of_actions)
                new_ind[i] = new_action
        new_population.append(new_ind)
    return new_population

def comon_sense_child(child, makoto):
    #avoid silly actions in the begining like using items of mana or basic attack aat the start
    new_child = child[:]
    for i in range(10):  
        if new_child[i] == "use_item" or new_child[i] == "Precious Egg" or new_child[i] == "basic_attack" or new_child[i] == "hamaon" or new_child[i] == "torrent_shot":
            new_action = random.choice(makoto.list_of_actions)
            while new_action == "use_item" or new_action == "Precious Egg" or new_action == "basic_attack":
                new_action = random.choice(makoto.list_of_actions)
            new_child[i] = new_action
    return new_child