import discord
from discord.ext import commands
from config import token
from logic import Pokemon, Wizard, Fighter
import random
import asyncio

intents = discord.Intents.default()  
intents.messages = True             
intents.message_content = True       
intents.guilds = True               

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')  

@bot.command()
async def go(ctx):
    author = ctx.author.name  
    if author not in Pokemon.pokemons:  
        chance = random.randint(1, 3)  
        if chance == 1:
            pokemon = Pokemon(author)  
        elif chance == 2:
            pokemon = Wizard(author)  
        elif chance == 3:
            pokemon = Fighter(author)  
            
        await ctx.send(await pokemon.info())  
        image_url = await pokemon.show_img()  
        if image_url:
            embed = discord.Embed()  
            embed.set_image(url=image_url)  
            await ctx.send(embed=embed)  
        else:
            await ctx.send("Pokémon görüntüsü yüklenemedi.")  
    else:
        await ctx.send("Zaten bir Pokémon oluşturmuşsun! Öncekini kaybettikten sonra yeni açabilirsin.")  

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None  
    if target:  
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            attacker = Pokemon.pokemons[ctx.author.name]  
            enemy = Pokemon.pokemons[target.name]  
            
            await ctx.send(f"⚔️ **{attacker.pokemon_trainer}** ile **{enemy.pokemon_trainer}** arasındaki Pokémon savaşı başladı! 🚀")
            
            # Sıralı otomatik döngü (Loop)
            current_attacker = attacker
            current_enemy = enemy
            
            while attacker.hp > 0 and enemy.hp > 0:
                # Saldırı gerçekleştir
                result_text, is_dead = await current_attacker.attack(current_enemy)
                await ctx.send(result_text)
                
                # Hedefin görselini ve güncel durumunu gösterelim (isteğe bağlı ama hoş durur)
                image_url = await current_enemy.show_img()
                if image_url:
                    embed = discord.Embed(description=f"@{current_enemy.pokemon_trainer} Pokémon Durumu")
                    embed.set_image(url=image_url)
                    await ctx.send(embed=embed)

                if is_dead or current_enemy.hp <= 0:
                    break
                
                # Sırayı değiştir
                current_attacker, current_enemy = current_enemy, current_attacker
                await asyncio.sleep(1.5) # Turlar arası 1.5 saniye bekleme süresi
            
            # Kazanan ve kaybedeni belirleme
            if attacker.hp > 0:
                winner = attacker
                loser_name = target.name
                winner_name = ctx.author.name
            else:
                winner = enemy
                winner_name = target.name
                loser_name = ctx.author.name
                
            # Ödül ve cezalar
            winner.max_hp += 0 # İsteğe bağlı max can sabit kalabilir
            winner.hp = winner.max_hp  # Canı fullenir
            winner.power += 20         # 20 güç bonusu kazanır
            
            # Kaybedenin Pokémon'unu silme (Death / Delete)
            if loser_name in Pokemon.pokemons:
                del Pokemon.pokemons[loser_name]
                
            await ctx.send(f"🎉 **Tebrikler @{winner_name}!** Savaşı kazandın ve ödül olarak **+20 güç** kazandın! Pokémon'unun canı tamamen yenilendi.")
            await ctx.send(f"💀 @{loser_name} adlı kullanıcının Pokémon'u öldü. Yeniden savaşmak için **!go** yazarak yeni bir Pokémon çağırabilirsin!")
            
        else:
            await ctx.send("Savaş için her iki tarafın da hayatta olan bir Pokémon sahibi olması gerekir!")  
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin. Örn: `!attack @kullanici`")  

bot.run(token)
