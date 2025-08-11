import random
import combat.enemy as enemy

class Makoto:
    def __init__(self):
        self.name = "Makoto"
        self.max_HP = 366
        self.max_SP = 246
        self.HP = 366
        self.SP = 246
        self.strong = "fire"
        self.weak = ""
        self.reflect = None
        self.critic_rate = 0.10 
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "recarm", "mediarama", "rakunda", "use_item"]
        self.items = {
            "Soma": 1,
            "Precious Egg": 2,
            "Magic Mirror": 1
        }

    def basic_attack(self, enemy):
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 60  # Base damage
            if enemy.strong == "slash":
                damage *= 0.6  # Less damage if enemy is strong
            elif enemy.block == "slash":
                damage *= 0
            elif enemy.weak == "slash":
                damage *= 1.4  # Increased damage if enemy is weak
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def bufula(self, enemy):
        print(f"{self.name} uses bufula!")
        return
    
    def torrent_shot(self, enemy):
        print(f"{self.name} uses torrent shot!")
        return

    def hamaon(self, enemy):
        print(f"{self.name} uses hamaon!")
        return

    def recarm(self, party_members):
        print(f"{self.name} uses recarm!")
        return
    
    def mediarama(self, party_members):
        print(f"{self.name} uses mediarama!")
    
    def rakunda(self, party_members):
        print(f"{self.name} uses rakunda!")
        return

    
    def use_item(self, party_members):
        print(self.items)
        item = input("Enter the item you want to use: ")
        while item not in self.items or self.items[item] <= 0:
            print("Invalid item or item not available. Please try again.")
            item = input("Enter the item you want to use: ")
        if item in self.items and self.items[item] > 0:
            self.items[item] -= 1
            if item == "Soma":
                for member in party_members:
                    if member.status != "fallen":
                        member.HP = member.max_HP
                        member.SP = member.max_SP
                print(f"{self.name} uses {item}!")
            elif item == "Precious Egg":
                print("Select an ally or yourself")
                for i, member in enumerate(party_members):
                    print(f"{i}. {member.name} (SP: {member.SP})")
                choice = input()
                condition = False
                while condition == False:
                    if choice.isdigit() and 0 <= int(choice) <= len(party_members): # agregar chequeo 
                        target = party_members[int(choice) - 1]
                        target.SP = target.max_SP
                        print(f"{self.name} uses {item}!")
                        condition = True
                    else:
                        print("Invalid choice. Please try again.")
                        choice = input("Enter the number of the ally: ")
            elif item == "Magic Mirror":
                for member in party_members: # Ver cómo hacer que se salga el reflect despues de que les peguen
                    member.reflect = ["ice", "fire", "electricity", "wind", "light", "dark", "almighty"]
                    # ver que no instakillee al boss si refleja hamaon
                print(f"{self.name} uses {item}!")
        else:
            print("Invalid item or item not available.")

        
class Yukari:
    def __init__(self):
        self.name = "Yukari"
        self.max_HP = 287
        self.max_SP = 285
        self.HP = 287
        self.SP = 285
        self.block= "wind"
        self.weak = "electric"
        self.critic_rate = 0.10
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "me_patra", "mediarama", "recarm", "diarama", "garula"]


    def basic_attack(self, enemy):
        #basic attack 
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 60  # Base damage
            if enemy.strong == "pierce":
                damage *= 0.6  # Less damage if enemy is strong
            elif enemy.block == "pierce":
                damage *= 0
            elif enemy.weak == "pierce":
                damage *= 1.4  # Increased damage if enemy is weak
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def me_patra(self, party_members):
        #Dispels Panic, Fear, and Distress (party). Coste: 6 SP. (Solo lo tira si mmiembros se ven afectados por algun estado)
        print(f"{self.name} uses me Patra!")
        return
    
    def mediarama(self, party_members):
        #Moderately restores party's HP. Coste: 16 SP. (Lo va a tirar si hay por lo menos 2 miembros con vida baja, si hay solo uno tira diarama)
        print(f"{self.name} uses mediarama!")
        return

    def recarm(self, party_members):
        #Revives an ally, restoring 50% of HP. Coste: 20 SP. (Solo lo usa si hay un miembro caído)
        print(f"{self.name} uses recarm!")
        return
    
    def garula(self, enemy):
        #Deals medium Wind damage to one foe. Coste: 6 SP.
        print(f"{self.name} uses garula!")
        return

    def diarama(self, party_members):
        #Moderately restores 1 ally's HP. Coste: 8 sp.
        print(f"{self.name} uses diarama!")
        return
    
class Junpei:

    def __init__(self):
        self.name = "Junpei"
        self.max_HP = 381
        self.max_SP = 201
        self.HP = 381
        self.SP = 201
        self.strong = "fire"
        self.weak = "wind"
        self.critic_rate = 0.20 
        self.prob_counter_phisical = 0.15 #pasiva
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "rakukaja", "marakukaja", "torrent_shot", "blade_of_fury"]

    def basic_attack(self, enemy):
        #Normal attack
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 60  # Base damage
            if enemy.strong == "slash":
                damage *= 0.6  # Less damage if the enemy is strong
            elif enemy.block == "slash":
                damage *= 0
            elif enemy.weak == "slash":
                damage *= 1.4  # Increased damage if the enemy is weak
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def rakukaja(self):
        #Increases 1 ally's defense by 25%. Coste: 6 sp.
        print(f"{self.name} uses rakukaja!")
        return
    
    def marakukaja(self):
        #Increases party's defense by 25%. Coste: 12 SP
        print(f"{self.name} uses marakukaja!")
        return
    
    def torrent_shot(self):
        #Deals light Pierce damage to one foe (2-3 hits) Coste: 10% HP
        print(f"{self.name} uses torrent shot!")
        return
    
    def blade_of_fury(self):
        #Deals medium Slash damage to all foes. (2-3 hits) Coste: 16% HP
        print(f"{self.name} uses blade of fury!")
        return

    
class Akihiko:

    def __init__(self):
        self.name = "Akihiko"
        self.max_HP = 369
        self.max_SP = 210
        self.HP = 369
        self.SP = 210
        self.block = "electric"
        self.weak = "ice"
        self.critic_rate = 0.10 
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "zionga", "tarunda", "rakunda", "sonic_punch", "sukunda"]

    def basic_attack(self, enemy):
        #Normal attack
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 60  # Base damage
            if enemy.strong == "strike":
                damage *= 0.6  # Less damage if the enemy is strong
            elif enemy.block == "strike":
                damage *= 0
            elif enemy.weak == "strike":
                damage *= 1.4  # Increased damage if the enemy is weak
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")
    
    def zionga(self):
        #Deals medium Elec damage / shocks one foe (10% chance of shocking). Coste: 8 SP
        print(f"{self.name} usa zionga!")
        #el resultado se eleva por 25% por su habilidad pasiva
        return
    
    def tarunda(self):
        #Decreases 1 foe's Attack by 25%*. Coste: 6 SP
        print(f"{self.name} usa tarunda!")
        return 
    
    def rakunda(self):
        #Decreases 1 foes' Defense by 25%*. Coste: 6 SP
        print(f"{self.name} usa rakunda!")
        return
    
    def sonic_punch(self):
        #Deals light Strike damage to one foe. Coste: 9%.
        print(f"{self.name} usa sonic punch!")
        return
    
    def sukunda(self):
        #Decreases 1 foe's Hit/Evasion rate by 10%*. Coste: 6 sp
        print(f"{self.name} usa sukunda!")
        return
    
