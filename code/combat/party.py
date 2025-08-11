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
        self.list_of_actions = ["basic_attack", "recarm", "mediarama", "rakunda","bufula","torrent_shot","hamaon","use_item"]
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
            if [m for m in enemy.strong if m == "slash"]:
                damage *= 0.6  # Less damage if enemy is strong
            elif [m for m in enemy.block if m == "slash"]:
                damage *= 0
            elif enemy.weak == "slash":
                damage *= 1.4  # Increased damage if enemy is weak
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def bufula(self, enemy):
        #Deals medium Ice damage / Freezes one foe. (10% chance of freezing). Coste: 8 SP
        print(f"{self.name} uses bufula!")
        self.SP -= 8
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 100
            if self.critic_rate > random.random():
                damage *= 1.5
            if [m for m in enemy.strong if m == "ice"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "ice"]:
                damage *= 0
            elif enemy.weak == "ice":
                damage *= 1.4
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")
            if random.random() < 0.10:  # 10% chance to freeze
                enemy.status = "frozen"
                print(f"{enemy.name} is frozen!")
    
    def torrent_shot(self, enemy):
        #Deals light Pierce damage to one foe. (2-3 hits). Coste: 10% HP
        print(f"{self.name} uses torrent shot!")
        self.HP -= 0.10 * self.HP
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 80
            if self.critic_rate > random.random():
                damage *= 1.5
            if [m for m in enemy.strong if m == "pierce"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "pierce"]:
                damage *= 0
            elif enemy.weak == "pierce":
                damage *= 1.4
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def hamaon(self, enemy):
        #(Light): instant kill, 1 foe (high odds). (40% chance). Coste: 12 SP
        print(f"{self.name} uses hamaon!")
        self.SP -= 12
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            if [m for m in enemy.block if m == "light"]:
                print(f"{enemy.name} is immune to light attacks!")
            else:
                if random.random() < 0.40:  # 40% prob
                    enemy.HP = 0
                    print(f"{enemy.name} was killed!")
                    enemy.status = "fallen"



    def recarm(self, party_members):
        #Revives an ally, restoring 50% of HP. Coste: 20 SP.
        print(f"{self.name} uses recarm!")
        self.SP -= 20
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            for member in party_members:
                if member.status == "fallen":
                    member.status = "normal"
                    member.HP = 0.50 * member.max_HP
                    print(f"{self.name} revives {member.name} with 50% HP!")
                    break
    
    def mediarama(self, party_members):
        #Moderately restores party's HP. Coste: 16 SP.
        print(f"{self.name} uses mediarama!")
        self.SP -= 16
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            for member in party_members:
                if member.status != "fallen":
                    member.HP += 100
                    if member.HP > member.max_HP:
                        member.HP = member.max_HP
            print("Party's HP restored by 100!")
    
    def rakunda(self, party_members):
        #increases 1 ally defense by 25%. Coste: 6 SP
        print(f"{self.name} uses rakunda!")
        self.SP -= 6
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
        self.reflect = None

    def basic_attack(self, enemy):
        #basic attack 
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 60  # Base damage
            if [ m for m in enemy.strong if m == "strike"]:
                damage *= 0.6  # Less damage if enemy is strong
            elif [ m for m in enemy.block if m == "strike"]:
                damage *= 0
            elif enemy.weak == "pierce":
                damage *= 1.4  # Increased damage if enemy is weak
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def me_patra(self, party_members):
        #Dispels Panic, Fear, and Distress (party). Coste: 6 SP. 
        print(f"{self.name} uses me Patra!")
        self.SP -= 6
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            for member in party_members:
                if member.status in ["panic", "fear", "distress"]:
                    member.status = "normal"
                    print(f"{member.name} is cured of {member.status}!")
            print("Party's status ailments cured!")
    
    def mediarama(self, party_members):
        #Moderately restores party's HP. Coste: 16 SP. 
        print(f"{self.name} uses mediarama!")
        self.SP -= 16
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            for member in party_members:
                if member.status != "fallen":
                    member.HP += 100
                    if member.HP > member.max_HP:
                        member.HP = member.max_HP
            print("Party's HP restored by 100!")

    def recarm(self, member):
        #Revives an ally, restoring 50% of HP. Coste: 20 SP.
        print(f"{self.name} uses recarm!")
        self.SP -= 20
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            if member.status == "fallen":
                member.status = "normal"
                member.HP = 0.50 * member.max_HP
                print(f"{self.name} revives {member.name} with 50% HP!")
            else:
                print(f"{member.name} is not fallen and cannot be revived.")
    
    def garula(self, enemy):
        #Deals medium Wind damage to one foe. Coste: 6 SP.
        print(f"{self.name} uses garula!")
        self.SP -= 6
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 80
            if self.critic_rate > random.random():
                damage *= 1.5
            if [ m for m in enemy.strong if m == "wind"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "wind"]:
                damage *= 0
            elif enemy.weak == "wind":
                damage *= 1.4
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def diarama(self,member):
        #Moderately restores 1 ally's HP. Coste: 8 sp.
        print(f"{self.name} uses diarama!")
        self.SP -= 8
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            member.HP += 100
            if member.HP > member.max_HP:
                member.HP = member.max_HP
            print(f"{self.name} restores 100 HP to {member.name}!")
    
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
        self.reflect = None

    def basic_attack(self, enemy):
        #Normal attack
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 60  # Base damage
            if [ m for m in enemy.strong if m == "slash"]:
                damage *= 0.6  # Less damage if the enemy is strong
            elif [ m for m in enemy.block if m == "slash"]:
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
    
    def torrent_shot(self,enemy):
        #Deals light Pierce damage to one foe (2-3 hits) Coste: 10% HP
        print(f"{self.name} uses torrent shot!")
        self.HP -= 0.10 * self.HP
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 80
            if self.critic_rate > random.random():
                damage *= 1.5
            if [ m for m in enemy.strong if m == "pierce"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "pierce"]:
                damage *= 0
            elif enemy.weak == "pierce":
                damage *= 1.4
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")
    
    def blade_of_fury(self,enemy):
        #Deals medium Slash damage to all foes. (2-3 hits) Coste: 16% HP
        print(f"{self.name} uses blade of fury!")
        self.HP -= 0.16 * self.HP
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 100
            if self.critic_rate > random.random():
                damage *= 1.5
            if [ m for m in enemy.strong if m == "slash"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "slash"]:
                damage *= 0
            elif enemy.weak == "slash":
                damage *= 1.4
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")

    
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
        self.reflect = None

    def basic_attack(self, enemy):
        #Normal attack
        print(f"{self.name} uses basic attack!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 60  # Base damage
            if [ m for m in enemy.strong if m == "strike"]:
                damage *= 0.6  # Less damage if the enemy is strong
            elif [m for m in enemy.block if m == "strike"]:
                damage *= 0
            elif enemy.weak == "strike":
                damage *= 1.4  # Increased damage if the enemy is weak
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")
    
    def zionga(self,enemy):
        #Deals medium Elec damage / shocks one foe (10% chance of shocking). Coste: 8 SP
        print(f"{self.name} usa zionga!")
        self.SP -= 8
        #el resultado se eleva por 25% por su habilidad pasiva
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 100
            if self.critic_rate > random.random():
                damage *= 1.5
            if [ m for m in enemy.strong if m == "electric"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "electric"]:
                damage *= 0
            elif enemy.weak == "electric":
                damage *= 1.4
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")
            if random.random() < 0.25:  # 10% chance to shock
                enemy.status = "shocked"
                print(f"{enemy.name} is shocked!")
    
    def tarunda(self,enemy):
        #Decreases 1 foe's Attack by 25%*. Coste: 6 SP
        print(f"{self.name} usa tarunda!")
        self.SP -= 6
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            pass
    
    def rakunda(self,enemy):
        #Decreases 1 foes' Defense by 25%*. Coste: 6 SP
        print(f"{self.name} usa rakunda!")
        self.SP -= 6
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            pass 
    
    def sonic_punch(self,enemy):
        #Deals light Strike damage to one foe. Coste: 9%.
        print(f"{self.name} usa sonic punch!")
        self.SP -= 9
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            damage = 70
            if self.critic_rate > random.random():
                damage *= 1.5
            if [ m for m in enemy.strong if m == "strike"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "strike"]:
                damage *= 0
            elif enemy.weak == "strike":
                damage *= 1.4
            enemy.HP -= damage
            print(f"{self.name} deals {damage} damage to {enemy.name}!")
        
    
    def sukunda(self, party_members):
        #Decrease 1 foe's Hit/Evasion rate by 10%*. Coste: 6 sp 
        print(f"{self.name} usa sukunda!")
        if self.fail_rate > random.random():
            print("The attack missed!")
        else:
            self.SP -= 6
            for member in party_members:
                if member.status != "fallen":
                    member.fail_rate -= 0.10
                print(f"{self.name} decreases the Hit/Evasion rate of {member.name} by 10%!")
                break #the first who is not fallen is affected
    
