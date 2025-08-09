
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
        print(f"{self.name} usa basic attack!")
        return  
    
    def me_patra(self):
        print(f"{self.name} usa me Patra!")
        return
    
    def mediarama(self):
        print(f"{self.name} usa mediarama!")
        return 
    
    def recarm(self):
        print(f"{self.name} usa rakunda!")
        return
    
    def garula(self):
        print(f"{self.name} usa garula!")
        return
    
    def diarama(self):
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
        print(f"{self.name} usa basic attack!")
        return
    
    def rakukaja(self):
        print(f"{self.name} usa rakukaja!")
        return
    
    def marakukaja(self):
        print(f"{self.name} usa marakukaja!")
        return
    
    def torrent_shot(self):
        print(f"{self.name} usa torrent shot!")
        return
    
    def blade_of_fury(self):
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
        print(f"{self.name} usa basic attack!")
        return
    
    def zionga(self):
        print(f"{self.name} usa zionga!")
        #el resultado se eleva por 25% por su habilidad pasiva
        return
    
    def traunda(self):
        print(f"{self.name} usa traunda!")
        return 
    
    def rakunda(self):
        print(f"{self.name} usa rakunda!")
        return
    
    def sonic_punch(self):
        print(f"{self.name} usa sonic punch!")
        return
    
    def sukunda(self):
        print(f"{self.name} usa sukunda!")
        return
    
