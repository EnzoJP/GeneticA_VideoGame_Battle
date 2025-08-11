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
        self.fail_rate = 0.15
        self.critic_rate = 0.10
        self.list_of_actions = ["basic_attack", "maragidyne", "hamaon", "megidola", "evil_touch", "ghastly_wail"]
        self.weak = ""

    def attacks_rate(self, party):
        # party es una lista de los personajes en combate
        #decide en base probabilidad de cada ataque cual usar
        #basic_attack solo si no tiene SP
        maragidyne = 0.40
        hamaon = 0.25
        megidola = 0.15
        evil_touch = 0.20
        #ghastly_wail es solo si alguien tiene miedo
        #fear boost es una pasiva

        if self.SP < 5: #ver numero
            return "basic_attack"
        
        for member in party:
            if member.status == "fear":
                return "ghastly_wail"
        
        attack = random.random()
        if attack < maragidyne:
            return "maragidyne"
        elif attack < maragidyne + hamaon:
            return "hamaon"
        elif attack < maragidyne + hamaon + megidola:
            return "megidola"
        elif attack < maragidyne + hamaon + megidola + evil_touch:
            return "evil_touch"
        
    def take_turn(self, party): # Enemy decides what to do based on attack probabilities

        action_name = self.attacks_rate(party)
        action = getattr(self, action_name)
        action(party) # Call the action method by name
        # Acá hacer que se elija entre los posibles ataques (los que les de el sp) o hacerlo en attacks_rate

    def basic_attack(self, party):
        #Normal attack using the Strike attribute. (Si SP<5)
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            
            target = random.choice(party)
            if target.status == "fallen":
                target = random.choice([m for m in party if m.status != "fallen"])  # Choose another target if fallen
            damage = 70  # Base damage
            if target.strong == "strike":
                damage *= 0.6  # Less damage if party member is strong
            elif target.block == "strike":
                damage *= 0
            elif target.weak == "strike":
                damage *= 1.4  # Increased damage if party member is weak
            target.HP -= damage
            print(f"{self.name} deals {damage} damage to {target.name}!")
            if target.HP <= 0:
                print(f"{target.name} has fallen!")
                target.status = "fallen"
                target.HP = 0  # eliminate HP to avoid negative values
        
    
    def maragidyne(self, party):
        #Deals heavy Fire damage to all foes. (39%)  Coste: 24 SP.
        if self.SP >= 24:
            self.SP -= 24
            print(f"{self.name} uses maragidyne!")
            for member in party:
                if member.status == "fallen":
                    continue
                else:
                    if self.critic_rate > random.random():
                        damage = 180 * 2  # ??
                    if member.weak == "fire":
                        damage = 180 * 1.4  # Increased damage if weak
                    else:
                        damage = 180 #despues cambiar daños

                    if self.fail_rate > random.random():
                        print(f"The attack missed! on [{member.name}]")
                    else:
                        member.HP -= damage
                        print(f"{self.name} deals {damage} damage to {member.name}!")
                        if member.HP <= 0:
                            print(f"{member.name} has fallen!")
                            member.status = "fallen"
                            member.HP = 0  # eliminate HP to avoid negative values

    def hamaon(self, party):
        #instant kill, 1 foe (high odds). (40% chance) (25%) Coste 12 SP
        if self.SP >= 12:
            self.SP -= 12
            target = random.choice(party)
            if target.status == "fallen":
                target = random.choice([m for m in party if m.status != "fallen"])
            print(f"{self.name} uses Hamaon on {target.name}!")
            if random.random() < 0.40:  # 40% prob 
                target.HP = 0
                print(f"{target.name} was killed!")
                target.status = "fallen"
                target.HP = 0  # eliminate HP to avoid negative values
            else:
                print(f"{target.name} resisted the attack.")
        else:
            print(f"{self.name} does not have enough SP to use Hamaon!")
    
    def megidola(self, party):
        #Deals heavy Almighty damage to all foes. (15%) Coste: 65 SP.
        if self.SP >= 65:
            self.SP -= 65
            print(f"{self.name} uses megidola!")
            for member in party:
                if member.status == "fallen":
                    continue
                else:
                    if self.fail_rate > random.random():
                        print(f"The attack missed! on [{member.name}]")
                    else: 
                        if self.critic_rate > random.random():
                            damage = 160 * 2  # ??
                        else:
                            damage = 160 #despues cambiar daños
                        
                        member.HP -= damage
                        print(f"{self.name} deals {damage} damage to {member.name}!")
                        if member.HP <= 0:
                            print(f"{member.name} has fallen!")
                            member.status = "fallen"
                            member.HP = 0  # eliminate HP to avoid negative values
    
    def evil_touch(self, party):
        #Instills Fear in 1 foe. (40% chance) (19%) Coste: 5 SP.
        #and the 25% increase because of the fear boost
        if self.SP < 5:
            print(f"{self.name} does not have enough SP to use Evil Touch!")
            return
        print(f"{self.name} uses evil touch!")
        target = random.choice(party)
        if target.status == "fallen":
            target = random.choice([m for m in party if m.status != "fallen"])
        if random.random() < 0.25: #25% chance to inflict fear
            print(f"{self.name} inflicts fear on {target.name}!")
            target.status = "fear"
        else:
            print(f"{self.name} fails to inflict fear.")
        
    
    def ghastly_wail(self, party): 
        #Instantly kills all foes who are fearful. 15 SP
        if self.SP < 15:
            print(f"{self.name} does not have enough SP to use Ghastly Wail!")
            return
        print(f"{self.name} uses ghastly wail!")
        for member in party:
            if member.status == "fear":
                member.HP = 0
                print(f"{member.name} was obliterated!")
                member.status = "fallen"
                member.HP = 0  # eliminate HP to avoid negative values
        
