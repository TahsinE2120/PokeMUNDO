import aiohttp
import random

class Pokemon:
    pokemons = {}
    
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.max_hp = random.randint(200, 1000) # Maksimum canı saklıyoruz
        self.hp = self.max_hp
        self.power = random.randint(30, 120)
        
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  
        async with aiohttp.ClientSession() as session:  
            async with session.get(url) as response:  
                if response.status == 200:
                    data = await response.json()  
                    return data['forms'][0]['name']  
                else:
                    return "Pikachu"  

    async def info(self):
        if not self.name:
            self.name = await self.get_name()  
            
        class_name = "Standart Pokémon"
        if isinstance(self, Wizard):
            class_name = "Sihirbaz (Wizard)"
        elif isinstance(self, Fighter):
            class_name = "Dövüşçü (Fighter)"
            
        return f"Pokémon'un türü: **{class_name}**\nPokémon'unuzun ismi: {self.name}\nCanı: {self.hp}/{self.max_hp}\nGücü: {self.power}"  
          
    async def show_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  
        async with aiohttp.ClientSession() as session:  
            async with session.get(url) as response:  
                if response.status == 200:
                    data = await response.json()  
                    return data['sprites']['front_default']  
                else:
                    return None  

    async def attack(self, enemy):
        # Wizard kalkan kontrolü
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return f"🛡️ @{enemy.pokemon_trainer}'nin Sihirbaz Pokémon'u kalkan kullandı ve gelen **{self.power}** hasarı tamamen engelledi!", False

        # Hasar verme
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"⚔️ @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı ({self.power} hasar).\n@{enemy.pokemon_trainer}'nin kalan canı: **{enemy.hp}/{enemy.max_hp}**", False
        else:
            enemy.hp = 0
            return f"🏆 @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi!", True

class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_attack = random.randint(15, 60)
        self.power += super_attack  
        
        # Üst sınıfın attack metodunu çağırıyoruz (dönüşleri güncelledik)
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                self.power -= super_attack
                return f"🛡️ @{enemy.pokemon_trainer}'nin Sihirbaz Pokémon'u kalkan kullandı ve hasarı engelledi!\n💥 Dövüşçü Pokémon süper saldırı denedi ama başarısız oldu! Eklenen güç: {super_attack}", False

        if enemy.hp > self.power:
            enemy.hp -= self.power
            res = f"⚔️ @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı.\n@{enemy.pokemon_trainer}'nin kalan canı: **{enemy.hp}/{enemy.max_hp}**\n💥 Dövüşçü Pokémon süper saldırı kullandı! Eklenen ekstra güç: {super_attack}"
            self.power -= super_attack
            return res, False
        else:
            enemy.hp = 0
            self.power -= super_attack
            return f"🏆 @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi!\n💥 Dövüşçü Pokémon süper saldırı kullandı! Eklenen ekstra güç: {super_attack}", True
