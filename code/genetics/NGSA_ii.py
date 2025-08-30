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
            n_var=50,              # número de acciones en la secuencia
            n_obj=2,               # turnos y score
            n_constr=0,
            xl=0,                  # valor mínimo (índice de acción)
            xu=len(ACTION_MAP)-1   # valor máximo (último índice)
        )
        self.makoto = makoto

    def _evaluate(self, x, out, *args, **kwargs):
        # convertir individuo a STRINGS
        indiv_str = [ACTION_MAP_INV[i] for i in x]

        # correr tu simulación normal
        turns, score = fitnessF.fitness_test_2(indiv_str)

        out["F"] = [turns, -score]

class ActionSequenceSampling(Sampling):
    def __init__(self, makoto, actions):
        super().__init__()
        self.makoto = makoto
        # filtramos "use_item" porque nuestra función ya lo reemplaza por los nombres de items
        self.actions = actions

    def _do(self, problem, n_samples, **kwargs):
        pop = []
        for _ in range(n_samples):
            # 1) generar individuo en STRINGS usando tu función
            print(self.actions)
            indiv_int = []
            indiv_str = generate_random_actions(self.actions, problem.n_var, self.makoto)
            #indiv_str = check_sp_cost(indiv_str, self.makoto)
            print(indiv_str)
            # 2) convertir a INTs para que pymoo lo entienda
            indiv_int = [ACTION_MAP[a] for a in indiv_str]

            pop.append(indiv_int)

        tree_array = np.array(pop)
        return tree_array



class MyCrossover(Crossover):
    def __init__(self, makoto):
        super().__init__(2, 1)
        self.makoto = makoto

    def _do(self, problem, X, **kwargs):
        n_matings = X.shape[1]
        children = []
        for k in range(n_matings):
            parent1, parent2 = X[0,k], X[1,k]  # arrays de ints

            # 1) convertir a strings
            parent1_str = [ACTION_MAP_INV[i] for i in parent1]
            parent2_str = [ACTION_MAP_INV[i] for i in parent2]

            # 2) aplicar TU crossover (que trabaja con strings)
            child_str = crossover_two_points(parent1_str, parent2_str, self.makoto)

            # 3) volver a ints
            print(f"Child after crossover (str): {child_str}")
            child = np.array([ACTION_MAP[a] for a in child_str])

            children.append(child)
        children_array = np.array(children)
        children_array = children_array[np.newaxis, :, :]
        return children_array


class MyMutation(Mutation):
    def __init__(self, makoto):
        super().__init__()
        self.makoto = makoto

    def _do(self, problem, X, **kwargs):
        for i in range(len(X)):
            # 1) convertir individuo a strings
            indiv_str = [ACTION_MAP_INV[j] for j in X[i]]

            # 2) mutar con tu función normal
            mutated_str = mutate(indiv_str, self.makoto)

            # 3) volver a ints para devolver a pymoo
            X[i] = [ACTION_MAP[a] for a in mutated_str]
        return X

def genetic_combat_nsga2(party_members, enemy):
    makoto = party_members[0]
    actions = makoto.list_of_actions

    problem = CombatProblem(makoto)

    algorithm = NSGA2(
        pop_size=25,
        sampling=ActionSequenceSampling(makoto,actions),
        crossover=MyCrossover(makoto),
        mutation=MyMutation(makoto),
        eliminate_duplicates=True
    )

    res = minimize(
        problem,
        algorithm,
        ('n_gen', 30),   # generaciones
        verbose=True
    )
    best_solution = res.X[0]

    # mostrar resultados
    print("Best solutions:")
    print(res.X)   # acciones
    print(res.F)   # [turns, -score]

    # convertir la mejor solución a strings
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
    while new_action == "Soma" or new_action == "Precious Egg" or new_action == "Magic Mirror" or new_action == "use_item":
        new_action = random.choice(actions)
    action_sequence_new = copy.deepcopy(action_sequence)
    action_sequence_new[mutation_point] = new_action
    return action_sequence_new
  