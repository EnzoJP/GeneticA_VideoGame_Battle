
class Makoto:
    def __init__(self):
        self.name = "Makoto"
        self.HP = 366
        self.SP = 246
        self.strong = "fire"
        self.critic_rate = 0.10 
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "recarm", "mediarama", "rakunda"]

    def basic_attack(self):
        print(f"{self.name} usa basic attack!")
        return  
    
    def recarm(self):
        print(f"{self.name} usa recarm!")
        return
    
    def mediarama(self):
        print(f"{self.name} usa mediarama!")
        return 
    
    def rakunda(self):
        print(f"{self.name} usa rakunda!")
        return
    

        
class Yukari:
    def __init__(self):
        self.name = "Yukari"
        self.HP = 287
        self.SP = 285
        self.block= "wind"
        self.weak = "electric"
        self.citic_rate = 0.10 
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "me_patra", "mediarama", "diarama", "garula"]


    def basic_attack(self):
        #basic attack 
        print(f"{self.name} usa basic attack!")
        return  
    
    def me_patra(self):
        #Dispels Panic, Fear, and Distress (party). Coste: 6 SP. (Solo lo tira si mmiembros se ven afectados por algun estado)
        print(f"{self.name} usa me Patra!")
        return
    
    def mediarama(self):
        #Moderately restores party's HP. Coste: 16 SP. (Lo va a tirar si hay por lo menos 2 miembros con vida baja, si hay solo uno tira diarama)
        print(f"{self.name} usa mediarama!")
        return 
    
    def recarm(self):
        #Revives an ally, restoring 50% of HP. Coste: 20 SP. (Solo lo usa si hay un miembro caído)
        print(f"{self.name} usa rakunda!")
        return
    
    def garula(self):
        #Deals medium Wind damage to one foe. Coste: 6 SP.
        print(f"{self.name} usa garula!")
        return
    
    def diarama(self):
        #Moderately restores 1 ally's HP. Coste: 8 sp.
        print(f"{self.name} usa diarama!")
        return
    
class Junpei:

    def __init__(self):
        self.name = "Junpei"
        self.HP = 381
        self.SP = 201
        self.strong = "fire"
        self.weak = "wind"
        self.critic_rate = 0.10 
        self.prob_counter_phisical = 0.15 #pasiva
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "rakukaja", "marakukaja", "torrent_shot", "blade_of_fury"]

    def basic_attack(self):
        #Normal attack
        print(f"{self.name} usa basic attack!")
        return
    
    def rakukaja(self):
        #Increases 1 ally's defense by 25%. Coste: 6 sp.
        print(f"{self.name} usa rakukaja!")
        return
    
    def marakukaja(self):
        #Increases party's defense by 25%. Coste: 12 SP
        print(f"{self.name} usa marakukaja!")
        return
    
    def torrent_shot(self):
        #Deals light Pierce damage to one foe (2-3 hits) Coste: 10% HP
        print(f"{self.name} usa torrent shot!")
        return
    
    def blade_of_fury(self):
        #Deals medium Slash damage to all foes. (2-3 hits) Coste: 16% HP
        print(f"{self.name} usa blade of fury!")
        return

    
class Akihiko:

    def __init__(self):
        self.name = "Akihiko"
        self.HP = 369
        self.SP = 210
        self.block = "electric"
        self.weak = "ice"
        self.critic_rate = 0.10 
        self.status = "normal" #normal es el estado por defecto
        self.fail_rate = 0.10
        self.list_of_actions = ["basic_attack", "zionga", "traunda", "rakunda", "sonic_punch", "sukunda"]

    def basic_attack(self):
        #Normal attack
        print(f"{self.name} usa basic attack!")
        return
    
    def zionga(self):
        #Deals medium Elec damage / shocks one foe (10% chance of shocking). Coste: 8 SP
        print(f"{self.name} usa zionga!")
        #el resultado se eleva por 25% por su habilidad pasiva
        return
    
    def traunda(self):
        #Decreases 1 foe's Attack by 25%*. Coste: 6 SP
        print(f"{self.name} usa traunda!")
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
    
