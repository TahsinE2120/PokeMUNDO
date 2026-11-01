import aiohttp  # Eşzamansız HTTP istekleri için bir kütüphane
import random

class Pokemon:
    pokemons = {}
    
    # Nesne başlatma (kurucu)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(200, 1000)
        self.power = random.randint(30, 120)
        
        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer]

    async def get_name(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenkron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'  
        async with aiohttp.ClientSession() as session:  
            async with session.get(url) as response:  
                if response.status == 200:
                    data = await response.json()  
                    return data['forms'][0]['name']  
                else:
                    return "Pikachu"  

    async def info(self):
        # Pokémon hakkında bilgi döndüren bir metot (Sınıf adını da ekledik)
        if not self.name:
            self.name = await self.get_name()  
            
        # Sınıf adını belirleme
        class_name = "Standart Pokémon"
        if isinstance(self, Wizard):
            class_name = "Sihirbaz (Wizard)"
        elif isinstance(self, Fighter):
            class_name = "Dövüşçü (Fighter)"
            
        return f"Pokémon'un türü: **{class_name}**\nPokémon'unuzun ismi: {self.name}\nCanı: {self.hp}\nGücü: {self.power}"  
          
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
        # Hedef Wizard (Sihirbaz) ise kalkan mekaniği kontrolü
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return f"@{enemy.pokemon_trainer}'nin Sihirbaz Pokémon'u kalkan kullandı ve gelen **{self.power}** hasarı tamamen engelledi! 🛡️"

        # Normal hasar hesaplama ve uygulama
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı ({self.power} hasar).\n@{enemy.pokemon_trainer}'nin kalan sağlık durumu: {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi! 🏆"

class Wizard(Pokemon):
    pass

class Fighter(Pokemon):
    async def attack(self, enemy):
        super_attack = random.randint(15, 60)
        self.power += super_attack  # Geçici olarak gücü artırıyoruz
        
        # Üst sınıfın attack metodunu çağırıyoruz
        result = await super().attack(enemy)
        
        self.power -= super_attack  # Gücü eski haline geri alıyoruz
        
        return result + f"\n💥 Dövüşçü Pokémon süper saldırı kullandı! Eklenen ekstra güç: {super_attack}"
