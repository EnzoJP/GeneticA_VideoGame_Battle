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
        self.critic_rate = 0.15
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.15
        self.defense = 24
        self.attack = 20
        self.atk_buff_turns = 0
        self.def_buff_turns = 0
        self.ev_buff_turns = 0
        self.list_of_actions = ["basic_attack", "recarm", "mediarama", "rakunda","bufula","torrent_shot","hamaon","use_item"]
        self.items = {
            "Soma": 1,
            "Precious Egg": 2,
            "Magic Mirror": 1
        }

    def all_out_attack (self, party_members, enemy):
        print("Critical hit! Time for an All-Out Attack!")
        total_damage = 0
        for member in party_members:
            if member.status == "normal":
                damage = random.randint(30, 50) * member.get_attack() / enemy.get_defense()
                total_damage += damage
        print(f"The party deals an extra {total_damage} damage to {enemy.name}!")
        return total_damage

    def get_defense(self):
        # Return current defense, applying buff if active
        if self.def_buff_turns > 0:
            return self.defense * 1.25
        return self.defense
    
    def get_attack(self):
        # Return current attack, applying buff if active
        if self.atk_buff_turns > 0:
            return self.attack * 1.25
        return self.attack

    def get_evasion(self):
        # Return current evasion, applying buff if active
        if self.ev_buff_turns > 0:
            return self.fail_rate - 0.10
        return self.fail_rate

    def basic_attack(self, enemy, party_members):
        print(f"{self.name} uses basic attack!")
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(45, 60) * attack_value / enemy_defense  # Base damage
            if [m for m in enemy.strong if m == "slash"]:
                damage *= 0.6  # Less damage if enemy is strong
            elif [m for m in enemy.block if m == "slash"]:
                damage *= 0
            elif enemy.weak == "slash":
                damage *= 1.4  # Increased damage if enemy is weak
            if self.critic_rate > random.random():
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
                enemy.HP -= damage
                print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def bufula(self, enemy):
        #Deals medium Ice damage / Freezes one foe. (10% chance of freezing). Coste: 8 SP
        print(f"{self.name} uses bufula!")
        self.SP -= 8
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(50, 64) * attack_value / enemy_defense
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
    
    def torrent_shot(self, enemy, party_members):
        #Deals light Pierce damage to one foe. (2-3 hits). Coste: 10% HP
        print(f"{self.name} uses torrent shot!")
        self.HP -= 0.10 * self.HP
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = 80 * attack_value / enemy_defense
            if self.critic_rate > random.random():
                damage *= 1.5
            if [m for m in enemy.strong if m == "pierce"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "pierce"]:
                damage *= 0
            elif enemy.weak == "pierce":
                damage *= 1.4
            if self.critic_rate > random.random():
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
                enemy.HP -= damage
                print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def hamaon(self, enemy):
        #(Light): instant kill, 1 foe (high odds). (40% chance). Coste: 12 SP
        print(f"{self.name} uses hamaon!")
        self.SP -= 12
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
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
        for member in party_members:
            if member.status != "fallen":
                member.HP += 100
                if member.HP > member.max_HP:
                    member.HP = member.max_HP
        print("Party's HP restored by 100!")
    
    def rakunda(self, enemy):
        #Decreases 1 foes' Defense by 25%. Coste: 6 SP
        print(f"{self.name} uses rakunda!")
        self.SP -= 6
        enemy.def_debuff_turns = 4
        print(f"{enemy.name}'s Defense decreased for 3 turns!")
    
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
                for member in party_members: 
                    member.reflect = ["ice", "fire", "electricity", "wind", "light", "dark", "almighty"]
                    
                print(f"{self.name} uses {item}!")
        else:
            print("Invalid item or item not available.")

    def use_item_auto(self, party_members, item):
        if item in self.items and self.items[item] > 0:
            self.items[item] -= 1
            if item == "Soma":
                for member in party_members:
                    if member.status != "fallen":
                        member.HP = member.max_HP
                        member.SP = member.max_SP
                print(f"{self.name} uses {item}!")
            elif item == "Precious Egg":
                if self.SP < 10:
                    #uses Precious Egg on itself
                    self.SP = self.max_SP
                    print(f"{self.name} uses {item} on itself!")
                else:
                    target = random.choice(party_members)
                    target.SP = target.max_SP
                    print(f"{self.name} uses {item} on {target.name}!")
            elif item == "Magic Mirror":
                for member in party_members:
                    member.reflect = ["ice", "fire", "electricity", "wind", "light", "dark", "almighty"]
                print(f"{self.name} uses {item}!")
        
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
        self.fail_rate = 0.15
        self.defense = 24
        self.attack = 20
        self.atk_buff_turns = 0
        self.def_buff_turns = 0
        self.ev_buff_turns = 0
        self.list_of_actions = ["basic_attack", "me_patra", "mediarama", "recarm", "diarama", "garula"]
        self.reflect = None

    def get_defense(self):
        # Return current defense, applying buff if active
        if self.def_buff_turns > 0:
            return self.defense * 1.25
        return self.defense
    
    def get_attack(self):
        # Return current attack, applying buff if active
        if self.atk_buff_turns > 0:
            return self.attack * 1.25
        return self.attack

    def get_evasion(self):
        # Return current evasion, applying buff if active
        if self.ev_buff_turns > 0:
            return self.fail_rate - 0.10
        return self.fail_rate
    
    def all_out_attack (self, party_members, enemy):
        print("Critical hit! Time for an All-Out Attack!")
        total_damage = 0
        for member in party_members:
            if member.status == "normal":
                damage = random.randint(30, 50) * member.get_attack() / enemy.get_defense()
                total_damage += damage
        print(f"The party deals an extra {total_damage} damage to {enemy.name}!")
        return total_damage

    def choose_action(self, party_members, enemy):
        available_actions = ["basic_attack"]
        fallen_ally = any(
            m.status == "fallen" 
            for m in party_members)
        low_hp_allies = [m for m in party_members 
                     if m.status != "fallen" and m.HP < m.max_HP * 0.65]
        ally_with_status = any(m.status in ["panic", "fear", "distress"] for m in party_members)

        if fallen_ally and self.SP >= 20:
            return "recarm"
        if len(low_hp_allies) >= 2 and self.SP >= 16:
            return "mediarama" #If there are 2 or more low HP allies, cures all
        elif len(low_hp_allies) == 1 and self.SP >= 8:
            return "diarama" #If there is 1 low HP ally, cures them
        if ally_with_status and self.SP >= 6:
            return "me_patra"
        if self.SP >= 6:
            available_actions.append("garula")
        return random.choice(available_actions)

    def basic_attack(self, enemy, party_members):
        #basic attack 
        print(f"{self.name} uses basic attack!")
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(40, 50) * attack_value / enemy_defense  # Base damage
            if [ m for m in enemy.strong if m == "strike"]:
                damage *= 0.6  # Less damage if enemy is strong
            elif [ m for m in enemy.block if m == "strike"]:
                damage *= 0
            elif enemy.weak == "pierce":
                damage *= 1.4  # Increased damage if enemy is weak
            if self.critic_rate > random.random():
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
                enemy.HP -= damage
                print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def me_patra(self, party_members):
        #Dispels Panic, Fear, and Distress (party). Coste: 6 SP. 
        print(f"{self.name} uses me Patra!")
        self.SP -= 6
        for member in party_members:
            if member.status in ["panic", "fear", "distress"]:
                member.status = "normal"
                print(f"{member.name} is cured of {member.status}!")
        print("Party's status ailments cured!")
    
    def mediarama(self, party_members):
        #Moderately restores party's HP. Coste: 16 SP. 
        print(f"{self.name} uses mediarama!")
        self.SP -= 16
        for member in party_members:
            if member.status != "fallen":
                member.HP += 110
                if member.HP > member.max_HP:
                    member.HP = member.max_HP
        print("Party's HP restored by 100!")

    def recarm(self, party_members):
        #Revives an ally, restoring 50% of HP. Coste: 20 SP.
        self.SP -= 20
        for member in party_members:
            if member.status == "fallen":
                member.status = "normal"
                member.HP = 0.50 * member.max_HP
                break
        print(f"{self.name} uses recarm!")
        print(f"{self.name} revives {member.name} with 50% HP!")
    
    def garula(self, enemy):
        #Deals medium Wind damage to one foe. Coste: 6 SP.
        print(f"{self.name} uses garula!")
        self.SP -= 6
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(48, 64) * attack_value / enemy_defense
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

    def diarama(self, member):
        #Moderately restores 1 ally's HP. Coste: 8 sp.
        print(f"{self.name} uses diarama!")
        self.SP -= 8
        
        if member.status != "fallen":
            member.HP += 140
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
        self.critic_rate = 0.25
        self.prob_counter_phisical = 0.15 #pasiva
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.15
        self.defense = 24
        self.attack = 20
        self.atk_buff_turns = 0
        self.def_buff_turns = 0
        self.ev_buff_turns = 0
        self.list_of_actions = ["basic_attack", "rakukaja", "marakukaja", "torrent_shot", "blade_of_fury"]
        self.reflect = None

    def get_defense(self):
        # Return current defense, applying buff if active
        if self.def_buff_turns > 0:
            return self.defense * 1.25
        return self.defense
    
    def get_attack(self):
        # Return current attack, applying buff if active
        if self.atk_buff_turns > 0:
            return self.attack * 1.25
        return self.attack

    def get_evasion(self):
        # Return current evasion, applying buff if active
        if self.ev_buff_turns > 0:
            return self.fail_rate - 0.10
        return self.fail_rate
    
    def all_out_attack (self, party_members, enemy):
        print("Critical hit! Time for an All-Out Attack!")
        total_damage = 0
        for member in party_members:
            if member.status == "normal":
                damage = random.randint(30, 50) * member.get_attack() / enemy.get_defense()
                total_damage += damage
        print(f"The party deals an extra {total_damage} damage to {enemy.name}!")
        return total_damage

    def choose_action(self, party_members, enemy):
        available_actions = ["basic_attack"]
        low_defense = any(member.def_buff_turns == 0 
                          for member in party_members 
                          if member.status != "fallen")
        if low_defense:
            if self.SP >= 12:
                available_actions.append("marakukaja")
            elif self.SP >= 6:
                valid_allies = [member for member in party_members 
                                if member.status != "fallen" 
                                and member.def_buff_turns == 0]
                if valid_allies:
                    available_actions.append("rakukaja")
        if self.HP > self.max_HP * 0.16:  
            available_actions.append("blade_of_fury")
        if self.HP > self.max_HP * 0.10: 
            available_actions.append("torrent_shot")
        
        return random.choice(available_actions)

    def basic_attack(self, enemy, party_members):
        #Normal attack
        print(f"{self.name} uses basic attack!")
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(45, 55) * attack_value / enemy_defense  # Base damage
            if [ m for m in enemy.strong if m == "slash"]:
                damage *= 0.6  # Less damage if the enemy is strong
            elif [ m for m in enemy.block if m == "slash"]:
                damage *= 0
            elif enemy.weak == "slash":
                damage *= 1.4  # Increased damage if the enemy is weak
            if self.critic_rate > random.random():
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
                enemy.HP -= damage
                print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def rakukaja(self, target):
        #Increases 1 ally's defense by 25%. Coste: 6 sp.
        print(f"{self.name} uses rakukaja!")
        self.SP -= 6
        
        target.def_buff_turns = 4
        print(f"{target.name}'s Defense increased for 3 turns!")

    def marakukaja(self, party_members):
        #Increases party's defense by 25%. Coste: 12 SP
        print(f"{self.name} uses marakukaja!")
        for member in party_members:
            member.def_buff_turns = 4
        print("Party's Defense increased for 3 turns!")
    
    def torrent_shot(self, enemy, party_members):
        #Deals light Pierce damage to one foe (2-3 hits) Coste: 10% HP
        print(f"{self.name} uses torrent shot!")
        self.HP -= 0.10 * self.HP
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(51, 80) * attack_value / enemy_defense
            if self.critic_rate > random.random():
                damage *= 1.5
            if [ m for m in enemy.strong if m == "pierce"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "pierce"]:
                damage *= 0
            elif enemy.weak == "pierce":
                damage *= 1.4
            if self.critic_rate > random.random():
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
                enemy.HP -= damage
                print(f"{self.name} deals {damage} damage to {enemy.name}!")

    def blade_of_fury(self, enemy, party_members):
        #Deals medium Slash damage to all foes. (2-3 hits) Coste: 16% HP
        print(f"{self.name} uses blade of fury!")
        self.HP -= 0.16 * self.HP
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(55, 83) * attack_value / enemy_defense
            if self.critic_rate > random.random():
                damage *= 1.5
            if [ m for m in enemy.strong if m == "slash"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "slash"]:
                damage *= 0
            elif enemy.weak == "slash":
                damage *= 1.4
            if self.critic_rate > random.random():
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
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
        self.fail_rate = 0.15
        self.defense = 24
        self.attack = 20
        self.atk_buff_turns = 0
        self.def_buff_turns = 0
        self.ev_buff_turns = 0
        self.list_of_actions = ["basic_attack", "zionga", "tarunda", "rakunda", "sonic_punch", "sukunda"]
        self.reflect = None

    def get_defense(self):
        # Return current defense, applying buff if active
        if self.def_buff_turns > 0:
            return self.defense * 1.25
        return self.defense
    
    def get_attack(self):
        # Return current attack, applying buff if active
        if self.atk_buff_turns > 0:
            return self.attack * 1.25
        return self.attack

    def get_evasion(self):
        # Return current evasion, applying buff if active
        if self.ev_buff_turns > 0:
            return self.fail_rate - 0.10
        return self.fail_rate

    def all_out_attack (self, party_members, enemy):
        print("Critical hit! Time for an All-Out Attack!")
        total_damage = 0
        for member in party_members:
            if member.status == "normal":
                damage = random.randint(30, 50) * member.get_attack() / enemy.get_defense()
                total_damage += damage
        print(f"The party deals an extra {total_damage} damage to {enemy.name}!")
        return total_damage

    def choose_action(self, party_members, enemy):
        # Prioritizes buffing and debuffing over attacking
        available_actions1 = []
        if enemy.def_debuff_turns == 0 and self.SP >= 6:
            available_actions1.append("rakunda")
        if enemy.atk_debuff_turns == 0 and self.SP >= 6:
            available_actions1.append("tarunda")
        for member in party_members:
            if member.status != "fallen" and member.ev_buff_turns == 0 and self.SP >= 6:
                available_actions1.append("sukunda")
                break
        available_actions2 = ["basic_attack"]
        if  self.HP > self.max_HP * 0.09:  
            available_actions2.append("sonic_punch")
        if self.SP >= 8:
            available_actions2.append("zionga")
        if len(available_actions1) > 0:
            if random.random() < 0.85:  # 85% chance to choose a buff/debuff action (his tactic)
                return random.choice(available_actions1)
            else:
                return random.choice(available_actions2)
        return random.choice(available_actions2)

    def basic_attack(self, enemy, party_members):
        #Normal attack
        print(f"{self.name} uses basic attack!")
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(47, 56) * attack_value / enemy_defense  # Base damage
            if [ m for m in enemy.strong if m == "strike"]:
                damage *= 0.6  # Less damage if the enemy is strong
            elif [m for m in enemy.block if m == "strike"]:
                damage *= 0
                enemy_blocks = True
            elif enemy.weak == "strike":
                damage *= 1.4  # Increased damage if the enemy is weak
            if self.critic_rate > random.random() and enemy_blocks != True:
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
                enemy.HP -= damage
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
    
    def zionga(self,enemy):
        #Deals medium Elec damage / shocks one foe (10% chance of shocking). Coste: 8 SP
        print(f"{self.name} usa zionga!")
        self.SP -= 8
        fail_rate = self.get_evasion()
        # el resultado se eleva por 25% por su habilidad pasiva
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = (random.randint(45, 59) * 1.25 ) * attack_value / enemy_defense # 1.25 por pasiva
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
            if random.random() < 0.10:  # 10% chance to shock
                enemy.status = "shocked"
                print(f"{enemy.name} is shocked!")
    
    def tarunda(self,enemy):
        #Decreases 1 foe's Attack by 25%*. Coste: 6 SP
        print(f"{self.name} usa tarunda!")
        self.SP -= 6
        enemy.atk_debuff_turns = 4
        print(f"{self.name} decreases the Attack of {enemy.name} by 25%!")

    def rakunda(self, enemy):
        #Decreases 1 foes' Defense by 25%*. Coste: 6 SP
        print(f"{self.name} usa rakunda!")
        self.SP -= 6
        enemy.def_debuff_turns = 4
        print(f"{self.name} decreases the Defense of {enemy.name} by 25%!")

    def sonic_punch(self, enemy, party_members):
        #Deals light Strike damage to one foe. Coste: 9% HP.
        print(f"{self.name} usa sonic punch!")
        self.SP -= 9
        fail_rate = self.get_evasion()
        if fail_rate > random.random():
            print("The attack missed!")
        else:
            attack_value = self.get_attack()
            enemy_defense = enemy.get_defense()
            damage = random.randint(45, 68) * attack_value / enemy_defense
            if [ m for m in enemy.strong if m == "strike"]:
                damage *= 0.6
            elif [m for m in enemy.block if m == "strike"]:
                enemy_blocks = True
                damage *= 0
            elif enemy.weak == "strike":
                damage *= 1.4
            if self.critic_rate > random.random() and enemy_blocks != True:
                damage *= 1.2
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
                damage += self.all_out_attack(party_members, enemy)
                enemy.HP -= damage
            else:
                enemy.HP -= damage
                print(f"{self.name} deals {damage} damage to {enemy.name}!")
        
    
    def sukunda(self, party_members):
        #Decrease 1 foe's Hit/Evasion rate by 10%*. Coste: 6 sp 
        print(f"{self.name} usa sukunda!")
        self.SP -= 6
        for member in party_members:
            if member.status != "fallen":
                member.ev_buff_turns = 4
                print(f"{self.name} increases the Evasion of {member.name} by 10%!")