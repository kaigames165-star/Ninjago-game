import discord
from discord.ext import commands
import random
import os
import asyncio

# Bot Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# 🏆 Full Characters List (18 characters)
ninjago_cards = [
    {"name": "lloyd", "image": "https://i.imgur.com/DVGrlrB.jpeg"},
    {"name": "kai", "image": "https://i.imgur.com/eYmxbCQ.jpeg"},
    {"name": "jay", "image": "https://i.imgur.com/miVpzov.jpeg"},
    {"name": "cole", "image": "https://i.imgur.com/nRFxh9y.jpeg"},
    {"name": "zane", "image": "https://i.imgur.com/tgodQ7E.jpeg"},
    {"name": "nya", "image": "https://i.imgur.com/JENM9xZ.jpeg"},
    {"name": "arin", "image": "https://i.imgur.com/ZZfcB9r.jpeg"},
    {"name": "sora", "image": "https://i.imgur.com/x7IUMHB.jpeg"},
    {"name": "frak", "image": "https://i.imgur.com/PPPowUh.jpeg"},
    {"name": "gandalaria", "image": "https://i.imgur.com/RtgGl1x.jpeg"},
    {"name": "jordana", "image": "https://i.imgur.com/oKjTFj7.jpeg"},
    {"name": "riyu", "image": "https://i.imgur.com/WPB2r5w.jpeg"},
    {"name": "source dragon of motion", "image": "https://i.imgur.com/bwXnejz.jpeg"},
    {"name": "arc dragon of balance", "image": "https://i.imgur.com/IIyc6ey.jpeg"},
    {"name": "rontu", "image": "https://i.imgur.com/6NSKZKt.jpeg"},
    {"name": "egalt", "image": "https://i.imgur.com/GoxIIdt.jpeg"},
    {"name": "zarkar", "image": "https://i.imgur.com/32z498a.jpeg"},
    {"name": "thunderfang", "image": "https://i.imgur.com/kIsgN4M.jpeg"}
]

@bot.event
async def on_ready():
    print(f'✅ {bot.user} is online!')

@bot.command()
async def character(ctx):
    game_scores = {}
    winning_score = 5
    game_on = True
    
    await ctx.send(f"🎮 **Game Started!** First to reach **{winning_score} points** wins!")
    
    while game_on:
        card = random.choice(ninjago_cards)
        embed = discord.Embed(title="⚔️ Who is this character?", color=discord.Color.gold())
        embed.set_image(url=card['image'])
        await ctx.send(embed=embed)
        
        def check(m):
            # البوت هنا يسمع فقط الإجابة الصحيحة وفي نفس القناة
            return m.channel == ctx.channel and m.content.lower() == card['name'].lower() and not m.author.bot
        
        try:
            # ينتظر 10 ثواني للإجابة الصحيحة
            msg = await bot.wait_for('message', check=check, timeout=10.0)
            
            user_id = msg.author.id
            game_scores[user_id] = game_scores.get(user_id, 0) + 1
            
            # يرسل رسالة فقط في حال كانت الإجابة صحيحة
            await ctx.send(f"✅ **{msg.author.display_name}**, you have guessed the character! You have now **{game_scores[user_id]}** points.")
            
            if game_scores[user_id] >= winning_score:
                await ctx.send(f"🏆 **{msg.author.mention} YOU HAVE WON THE GAME!** 🏆")
                game_on = False
            else:
                await asyncio.sleep(2) 
                
        except asyncio.TimeoutError:
            # إذا لم يكتب أحد الإجابة الصحيحة خلال الوقت المحدد
            await ctx.send(f"⌛ **Time's up!** It was **{card['name']}**.")
            await asyncio.sleep(2)

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
 
