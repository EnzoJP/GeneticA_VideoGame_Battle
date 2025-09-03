import random
import copy
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.core.sampling import Sampling
from pymoo.core.problem import ElementwiseProblem
from combat.automatized_combat import automatized_combat
from genetics.random import generate_random_actions, calculate_sp_cost
import genetics.fitnessF as fitnessF
from genetics.model_genetic import check_sp_cost
from pymoo.core.crossover import Crossover
from pymoo.core.mutation import Mutation
import numpy as np

ACTION_MAP = {
    "basic_attack": 0,
    "recarm": 1,
    "mediarama": 2,
    "rakunda": 3,
    "bufula": 4,
    "torrent_shot": 5,
    "hamaon": 6,
    "Soma": 7,
    "Precious Egg": 8,
    "Magic Mirror": 9,
}

ACTION_MAP_INV = {v: k for k, v in ACTION_MAP.items()}

class CombatProblem(ElementwiseProblem):
    def __init__(self, makoto):
        super().__init__(
            n_var=50,              # secuence length
            n_obj=2,               # objetives death, -damage
            n_constr=0,
            xl=0,                  # min index
            xu=len(ACTION_MAP)-1   # max index
        )
        self.makoto = makoto

    def _evaluate(self, x, out, *args, **kwargs):
        # convert to strings
        indiv_str = [ACTION_MAP_INV[i] for i in x]

        
        win,damage,deaths,turns = fitnessF.retur_stats(indiv_str[:])
        if not win:
            out["F"] = [deaths + 10, -damage]  # penalize losses heavily
        else:
            out["F"] = [deaths, -damage]  # minimize deaths, maximize damage

class ActionSequenceSampling(Sampling):
    def __init__(self, makoto, actions):
        super().__init__()
        self.makoto = makoto
        self.actions = actions

    def _do(self, problem, n_samples, **kwargs):
        pop = []
        for _ in range(n_samples):
            # Generate string sequence
            indiv_str = generate_random_actions(self.actions, problem.n_var, self.makoto)
            
            # make sure the length is correct
            if len(indiv_str) > problem.n_var:
                indiv_str = indiv_str[:problem.n_var]  # cut if too long
            elif len(indiv_str) < problem.n_var:
                # just in case if too short
                extra_actions = generate_random_actions(
                    self.actions, 
                    problem.n_var - len(indiv_str), 
                    self.makoto
                )
                indiv_str.extend(extra_actions)
            
            # Convert to int
            indiv_int = []
            for a in indiv_str:
                if a in ACTION_MAP:
                    indiv_int.append(ACTION_MAP[a])
                else:
                    # just if action not found, should not happen
                    indiv_int.append(ACTION_MAP["basic_attack"])
                    print(f"Advertencia: acción '{a}' no encontrada en ACTION_MAP")
            
            pop.append(indiv_int)
        
        # make sure all individuals have the correct length
        for i, indiv in enumerate(pop):
            if len(indiv) != problem.n_var:
                print(f"Individuo {i} tiene longitud {len(indiv)}, esperada {problem.n_var}")
                # Ajust
                if len(indiv) > problem.n_var:
                    pop[i] = indiv[:problem.n_var]
                else:
                    pop[i] = indiv + [ACTION_MAP["basic_attack"]] * (problem.n_var - len(indiv))
        
        return np.array(pop)



class MyCrossover(Crossover):
    def __init__(self, makoto):
        super().__init__(2, 1)
        self.makoto = makoto

    def _do(self, problem, X, **kwargs):
        n_matings = X.shape[1]
        n_offsprings = self.n_offsprings  # number of children
        
        # prepare array for children (1 child per generation)
        children = np.full((n_offsprings, n_matings, problem.n_var), -1, dtype=int)
        
        for k in range(n_matings):
            parent1, parent2 = X[0, k], X[1, k]
            
            
            parent1_str = [ACTION_MAP_INV[i] for i in parent1]
            parent2_str = [ACTION_MAP_INV[i] for i in parent2]

            
            child_str = crossover_two_points(parent1_str, parent2_str, self.makoto)
            
            
            if len(child_str) != problem.n_var:
                if len(child_str) > problem.n_var:
                    child_str = child_str[:problem.n_var]
                else:
                    # Extender con acciones básicas si es más corto
                    child_str.extend(['basic_attack'] * (problem.n_var - len(child_str)))
            
            
            child_int = [ACTION_MAP[a] for a in child_str]
            children[0, k] = child_int  
        
        return children

class MyMutation(Mutation):
    def __init__(self, makoto):
        super().__init__()
        self.makoto = makoto

    def _do(self, problem, X, **kwargs):
        for i in range(len(X)):
            
            indiv_str = [ACTION_MAP_INV[j] for j in X[i]]

            
            mutated_str = mutate(indiv_str, self.makoto)

            
            X[i] = [ACTION_MAP[a] for a in mutated_str]
        return X

def genetic_combat_nsga2(party_members, enemy,seed):
    makoto = party_members[0]
    actions = makoto.list_of_actions

    problem = CombatProblem(makoto)

    algorithm = NSGA2(
        pop_size=38,
        sampling=ActionSequenceSampling(makoto,actions),
        crossover=MyCrossover(makoto),
        mutation=MyMutation(makoto),
        eliminate_duplicates=False
    )

    res = minimize(
        problem,
        algorithm,
        ('n_gen', 55),   # generaciones
        verbose=True,
        seed=seed,
        save_history=True

    )
    best_solution = res.X[0]

    
    print("Best solutions:")
    print(res.X)   
    print(res.F)   

    import matplotlib.pyplot as plt
    import numpy as np
    from pymoo.util.nds.non_dominated_sorting import NonDominatedSorting

    # Print basic info
    #print("res.F shape:", res.F.shape)
    #print("Number of final solutions:", len(res.F))
    #print("First 10 solutions:")
    #for i in range(min(10, len(res.F))):
        #print(f"Solution {i}: {res.F[i]}")

    # Collect all individuals from history (if save_history=True was used in minimize)
    all_F = np.vstack([algo.pop.get("F") for algo in res.history])

    # Extract values
    turns_all = all_F[:, 0]
    score_all = -all_F[:, 1]  # make score positive

    # Final front only
    turns_final = res.F[:, 0]
    score_final = -res.F[:, 1]

    # Plot all individuals (gray background points)
    plt.figure(figsize=(12, 8))
    plt.scatter(turns_all, score_all, color='gray', alpha=0.9, s=50, label='All evaluated solutions')

    
    plt.scatter(turns_final, score_final, color='red', alpha=0.3, s=50)

    # Highlight Pareto front
    nds = NonDominatedSorting()
    non_dominated_indices = nds.do(res.F, only_non_dominated_front=True)
    non_dominated_F = res.F[non_dominated_indices]
    plt.scatter(non_dominated_F[:, 0], -non_dominated_F[:, 1],
                color='blue', s=80, edgecolors='black', alpha=0.9,
                label='Pareto front (non-dominated)')

    # Labels and title
    plt.xlabel('Deaths (minimize)', fontsize=12)
    plt.ylabel('Damage (maximize)', fontsize=12)
    plt.title('NSGA-II Results (All Generations)', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    #plt.show()   
    
    best_actions = [ACTION_MAP_INV[i] for i in best_solution]
    print(f"Best action sequence: {best_actions}")
    result = automatized_combat(party_members, enemy, best_actions)
    if result["won"]:
        print("Combat finished with a win.")
    else:
        print("Combat finished with a loss.")
    return result


  


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
            child1 = comon_sense_child(child1, makoto)
            return child1
        else:
            child2 = comon_sense_child(child2, makoto)
            return child2

    else:
        child = comon_sense_child(child, makoto)
        return child
    

def mutate(action_sequence,makoto):
    #mutate the action sequence by changing a random action, not items because it's difficult to track 
    mutation_point = random.randint(0, len(action_sequence) - 1)
    actions = makoto.list_of_actions
    new_action = random.choice(actions)
    while new_action == "Soma" or new_action == "Precious Egg" or new_action == "Magic Mirror" or new_action == "use_item":
        new_action = random.choice(actions)
    action_sequence_new = copy.deepcopy(action_sequence)
    action_sequence_new[mutation_point] = new_action
    return action_sequence_new
  
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