import random

class Enemy:
    def __init__(self):
        self.name = "Sleeping Table"
        self.HP = 1700
        self.SP = 500
        self.block= ["light", "dark"]
        self.strong = ["basic_attack", "physical","piercing"]
        self.low_damage = ["fire"]
        self.low_damage_rate = 0.25
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.critic_rate = 0.10
        self.list_of_actions = ["basic_attack", "maragidyne", "hamaon", "magidola", "evil_touch", "ghastly_wail"]

    def attacks_rate(self, party):
        # party es una lista de los personajes en combate
        #decide en base probabilidad de cada ataque cual usar
        #basic_attack solo si no tiene SP
        maragidyne = 0.40
        hamaon = 0.25
        magidola = 0.15
        evil_touch = 0.20
        #ghastly_wail es solo si alguien tiene miedo
        #fear boost es una pasiva

        if self.SP < 10: #ver numero
            return "basic_attack"
        
        for member in party:
            if member.status == "fear":
                return "ghastly_wail"
        
        attack = random.random()
        if attack < maragidyne:
            return "maragidyne"
        elif attack < maragidyne + hamaon:
            return "hamaon"
        elif attack < maragidyne + hamaon + magidola:
            return "magidola"
        elif attack < maragidyne + hamaon + magidola + evil_touch:
            return "evil_touch"
        

        
    def basic_attack(self):
        print(f"{self.name} usa basic attack!")
        return
    
    def maragidyne(self):
        print(f"{self.name} usa maragidyne!")
        return
    
    def hamaon(self):
        print(f"{self.name} usa hamaon!")
        return
    
    def magidola(self):
        print(f"{self.name} usa magidola!")
        return
    
    def evil_touch(self):
        print(f"{self.name} usa evil touch!")
        return
    
    def ghastly_wail(self):
        print(f"{self.name} usa ghastly wail!")
        return
    
