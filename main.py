import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# قائمة الـ 18 شخصية التي أرسلتها (مرتبة وجاهزة)
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
    {"name": "Jordana", "image": "https://i.imgur.com/oKjTFj7.jpeg"},
    {"name": "Riyu", "image": "https://i.imgur.com/WPB2r5w.jpeg"},
    {"name": "source dragon of motion", "image": "https://i.imgur.com/bwXnejz.jpeg"},
    {"name": "Arc dragon of balance", "image": "https://i.imgur.com/IIyc6ey.jpeg"},
    {"name": "rontu", "image": "https://i.imgur.com/6NSKZKt.jpeg"},
    {"name": "egalt", "image": "https://i.imgur.com/GoxIIdt.jpeg"},
    {"name": "zarkar", "image": "https://i.imgur.com/32z498a.jpeg"},
    {"name": "thunderfang", "image": "https://i.imgur.com/kIsgN4M.jpeg"}
]

@bot.event
async def on_ready():
    print(f'✅ البوت يعمل الآن باسم: {bot.user}')

@bot.command()
async def spawn(ctx):
    card = random.choice(ninjago_cards)
    embed = discord.Embed(
        title="⚡ بطاقة نينجاغو جديدة ظهرت!",
        description="اكتب اسم الشخصية للإمساك بها!",
        color=discord.Color.blue()
    )
    embed.set_image(url=card['image'])
    await ctx.send(embed=embed)
    
    # رسالة مساعدة لك كمبرمج (سيتم مسحها لاحقاً)
    print(f"تم إظهار بطاقة: {card['name']}")

# جلب التوكن من النظام (مهم جداً للاستضافة)
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("خطأ: لم يتم العثور على التوكن في إعدادات الاستضافة!")
