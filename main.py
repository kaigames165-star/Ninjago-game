import discord
from discord.ext import commands
import random
import asyncio
import os
import json
from difflib import SequenceMatcher

# --- Bot Configuration ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Data files
DATA_FILE = "players_data.json"
SHOP_FILE = "shop_items.json"

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Characters Database (57 Characters) ---
ninjago_cards = [
    # Legendary (50 Pts)
    {"name": "Garmadon", "image": "https://i.imgur.com/f9SZRtg.png", "rarity": "Legendary", "value": 50},
    {"name": "The Overlord", "image": "https://i.imgur.com/mIZzwmp.jpeg", "rarity": "Legendary", "value": 50},
    {"name": "Source Dragon of Motion", "image": "https://i.imgur.com/bwXnejz.jpeg", "rarity": "Legendary", "value": 50},
    {"name": "Arc Dragon of Balance", "image": "https://i.imgur.com/IIyc6ey.jpeg", "rarity": "Legendary", "value": 50},
    {"name": "Harumi", "image": "https://i.imgur.com/0EpGhTP.jpeg", "rarity": "Legendary", "value": 50},

    # Ultra-Rare (30 Pts)
    {"name": "Morro", "image": "https://i.imgur.com/IGu9naC.jpeg", "rarity": "Ultra-Rare", "value": 30},
    {"name": "Pythor", "image": "https://i.imgur.com/yNt3c0h.jpeg", "rarity": "Ultra-Rare", "value": 30},
    {"name": "Aspheera", "image": "https://i.imgur.com/hE48shG.jpeg", "rarity": "Ultra-Rare", "value": 30},
    {"name": "Vangelis", "image": "https://i.imgur.com/7w701Zc.jpeg", "rarity": "Ultra-Rare", "value": 30},
    {"name": "Master Chen", "image": "https://i.imgur.com/vnM6F7n.jpeg", "rarity": "Ultra-Rare", "value": 30},

    # Rare (20 Pts)
    {"name": "Lloyd", "image": "https://i.imgur.com/DVGrlB.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Kai", "image": "https://i.imgur.com/eYmxbCQ.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Jay", "image": "https://i.imgur.com/miVpzov.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Cole", "image": "https://i.imgur.com/nRFxh9y.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Zane", "image": "https://i.imgur.com/tgodQ7E.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Nya", "image": "https://i.imgur.com/JENM9xZ.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Skylor", "image": "https://i.imgur.com/xttbVTy.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Maya", "image": "https://i.imgur.com/kiE0CZN.jpeg", "rarity": "Rare", "value": 20},
    {"name": "Ray", "image": "https://i.imgur.com/cJsPTMT.jpeg", "rarity": "Rare", "value": 20},

    # Common (10 Pts)
    {"name": "Arin", "image": "https://i.imgur.com/ZZfcB9r.jpeg", "rarity": "Common", "value": 10},
    {"name": "Sora", "image": "https://i.imgur.com/x7IUMHB.jpeg", "rarity": "Common", "value": 10},
    {"name": "Frak", "image": "https://i.imgur.com/PPPowUh.jpeg", "rarity": "Common", "value": 10},
    {"name": "Gandalaria", "image": "https://i.imgur.com/RtgGl1x.jpeg", "rarity": "Common", "value": 10},
    {"name": "Jordana", "image": "https://i.imgur.com/oKjTFj7.jpeg", "rarity": "Common", "value": 10},
    {"name": "Riyu", "image": "https://i.imgur.com/WPB2r5w.jpeg", "rarity": "Common", "value": 10},
    {"name": "Rontu", "image": "https://i.imgur.com/6NSKZKt.jpeg", "rarity": "Common", "value": 10},
    {"name": "Egalt", "image": "https://i.imgur.com/GoxIIdt.jpeg", "rarity": "Common", "value": 10},
    {"name": "Zarkar", "image": "https://i.imgur.com/32z498a.jpeg", "rarity": "Common", "value": 10},
    {"name": "Thunderfang", "image": "https://i.imgur.com/kIsgN4M.jpeg", "rarity": "Common", "value": 10},
    {"name": "Ronin", "image": "https://i.imgur.com/Hq6TfxW.jpeg", "rarity": "Common", "value": 10},
    {"name": "Benthomaar", "image": "https://i.imgur.com/Cie5DBB.jpeg", "rarity": "Common", "value": 10},
    {"name": "Misako", "image": "https://i.imgur.com/VSLnFzC.jpeg", "rarity": "Common", "value": 10},
    {"name": "Cyrus Borg", "image": "https://i.imgur.com/PLXUzZT.jpeg", "rarity": "Common", "value": 10},
    {"name": "Dareth", "image": "https://i.imgur.com/1TvWYUS.jpeg", "rarity": "Common", "value": 10},
    {"name": "Dr. Julien", "image": "https://i.imgur.com/ER2yUDQ.jpeg", "rarity": "Common", "value": 10},
    {"name": "Ed", "image": "https://i.imgur.com/mmAyLCX.jpeg", "rarity": "Common", "value": 10},
    {"name": "Edna", "image": "https://i.imgur.com/ssbvcPN.jpeg", "rarity": "Common", "value": 10},
    {"name": "Lou", "image": "https://i.imgur.com/SrOqRzO.jpeg", "rarity": "Common", "value": 10},
    {"name": "Falcon", "image": "https://i.imgur.com/z7Klgge.jpeg", "rarity": "Common", "value": 10},
    {"name": "Clutch Powers", "image": "https://i.imgur.com/AKRlVcO.jpeg", "rarity": "Common", "value": 10},
    {"name": "Vania", "image": "https://i.imgur.com/YtZ7AeL.jpeg", "rarity": "Common", "value": 10},
    {"name": "Milton Dyer", "image": "https://i.imgur.com/Sfptdre.jpeg", "rarity": "Common", "value": 10},
    {"name": "Okino", "image": "https://i.imgur.com/8SET8ed.jpeg", "rarity": "Common", "value": 10},
    {"name": "Scott", "image": "https://i.imgur.com/tzXAwGt.jpeg", "rarity": "Common", "value": 10},
    {"name": "Blazey H. Speed", "image": "https://i.imgur.com/rTnSbG4.jpeg", "rarity": "Common", "value": 10},
    {"name": "Nelson", "image": "https://i.imgur.com/EOvcjQ0.jpeg", "rarity": "Common", "value": 10},
    {"name": "Antonia", "image": "https://i.imgur.com/bjnDPta.jpeg", "rarity": "Common", "value": 10},
    {"name": "Kataru", "image": "https://i.imgur.com/f0xrRrt.jpeg", "rarity": "Common", "value": 10},
    {"name": "Akita", "image": "https://i.imgur.com/r2Bi0qY.jpeg", "rarity": "Common", "value": 10},
    {"name": "Sally", "image": "https://i.imgur.com/bJyRnrc.jpeg", "rarity": "Common", "value": 10},
    {"name": "Ash", "image": "https://i.imgur.com/VKK4Oko.jpeg", "rarity": "Common", "value": 10},
    {"name": "Mystake", "image": "https://i.imgur.com/o34KpiB.jpeg", "rarity": "Common", "value": 10},
    {"name": "Police Commissioner", "image": "https://i.imgur.com/go1XbZN.jpeg", "rarity": "Common", "value": 10},
    {"name": "Echo Zane", "image": "https://i.imgur.com/8EoLMpO.jpeg", "rarity": "Common", "value": 10},
    {"name": "Fritz", "image": "https://i.imgur.com/lA6yiAJ.jpeg", "rarity": "Common", "value": 10},
    {"name": "Spitz", "image": "https://i.imgur.com/BUJHTPw.jpeg", "rarity": "Common", "value": 10},
    {"name": "Bonzle", "image": "https://i.imgur.com/fOSYpIl.jpeg", "rarity": "Common", "value": 10}
]

msg_count = {}

def is_similar(a, b):
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio() > 0.82

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - Full Database & Games Active')

@bot.event
async def on_message(message):
    if message.author.bot: return
    cid = str(message.channel.id)
    msg_count[cid] = msg_count.get(cid, 0) + 1
    if msg_count[cid] >= 25:
        msg_count[cid] = 0
        await spawn_event(message.channel)
    await bot.process_commands(message)

async def spawn_event(channel):
    rarity = random.choices(["Common", "Rare", "Ultra-Rare", "Legendary"], weights=[50, 30, 15, 5])[0]
    available_cards = [c for c in ninjago_cards if c['rarity'] == rarity]
    card = random.choice(available_cards if available_cards else ninjago_cards)

    embed = discord.Embed(title="⚡ A WILD CHARACTER APPEARED!", description="**Guess the character to catch it!**", color=discord.Color.blue())
    embed.set_image(url=card['image'])
    embed.set_footer(text="Time limit: 25 seconds")
    spawn_msg = await channel.send(embed=embed)

    def check(m):
        return m.channel == channel and not m.author.bot and is_similar(m.content, card['name'])

    try:
        winner = await bot.wait_for('message', check=check, timeout=25.0)
        data = load_json(DATA_FILE)
        uid = str(winner.author.id)
        if uid not in data: data[uid] = {"points": 0, "inventory": [], "items": []}
        data[uid]["points"] += card["value"]
        data[uid]["inventory"].append(card["name"])
        save_json(data, DATA_FILE)
        
        win_embed = discord.Embed(title="✅ CAUGHT!", description=f"{winner.author.mention} caught **{card['name']}**!\nRarity: `{card['rarity']}` | Points: `+{card['value']}`", color=discord.Color.green())
        await channel.send(embed=win_embed)
    except asyncio.TimeoutError:
        embed.title = "⌛ THE TIME IS UP!"
        embed.description = f"The character was **{card['name']}**. It disappeared!"
        embed.color = discord.Color.red()
        embed.set_image(url=None)
        await spawn_msg.edit(embed=embed)

# --- Shop Commands ---
@bot.group(invoke_without_command=True)
async def shop(ctx):
    items = load_json(SHOP_FILE)
    embed = discord.Embed(title="🛒 Ninja Shop", description="Use `!buy <item_name>`", color=discord.Color.gold())
    if not items: embed.description = "The shop is empty."
    else:
        for name, price in items.items():
            embed.add_field(name=name, value=f"Price: {price} points", inline=False)
    await ctx.send(embed=embed)

@shop.command(name="add")
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def shop_add(ctx, price: int, *, name: str):
    items = load_json(SHOP_FILE)
    items[name] = price
    save_json(items, SHOP_FILE)
    await ctx.send(f"✅ Added **{name}** to shop for **{price}** points!")

@shop.command(name="remove")
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def shop_remove(ctx, *, name: str):
    items = load_json(SHOP_FILE)
    if name in items:
        del items[name]
        save_json(items, SHOP_FILE)
        await ctx.send(f"🗑️ Removed **{name}** from the shop.")
    else:
        await ctx.send("❌ Item not found.")

@bot.command()
async def buy(ctx, *, item_name: str):
    shop_items = load_json(SHOP_FILE)
    if item_name not in shop_items: return await ctx.send("❌ Item not in shop.")
    data = load_json(DATA_FILE)
    uid = str(ctx.author.id)
    user = data.get(uid, {"points": 0, "items": []})
    if user["points"] < shop_items[item_name]: return await ctx.send("❌ Not enough points.")
    user["points"] -= shop_items[item_name]
    user.setdefault("items", []).append(item_name)
    data[uid] = user
    save_json(data, DATA_FILE)
    await ctx.send(f"🛍️ You bought **{item_name}**!")

@bot.command()
async def inv(ctx):
    data = load_json(DATA_FILE)
    user = data.get(str(ctx.author.id), {"points": 0, "inventory": []})
    embed = discord.Embed(title=f"🎒 {ctx.author.name}'s Inventory", color=discord.Color.purple())
    embed.add_field(name="💰 Points", value=user["points"], inline=False)
    inv_list = {x: user["inventory"].count(x) for x in set(user["inventory"])}
    desc = "\n".join([f"• {name} (x{count})" for name, count in inv_list.items()]) if inv_list else "Empty."
    embed.description = desc[:2048]
    await ctx.send(embed=embed)

# --- Games ---
@bot.command()
async def rps(ctx, member: discord.Member):
    if member.bot or member == ctx.author: return await ctx.send("Challenge a friend!")
    await ctx.send(f"{member.mention}, {ctx.author.mention} challenged you! Type rock, paper, or scissors in my DMs.")
    choices = {}
    def check(m): return m.author in [ctx.author, member] and m.guild is None and m.content.lower() in ['rock', 'paper', 'scissors']
    while len(choices) < 2:
        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            choices[msg.author] = msg.content.lower()
            await msg.author.send(f"Chose: {msg.content}")
        except asyncio.TimeoutError: break
    if len(choices) < 2: return await ctx.send("Game timed out.")
    c1, c2 = choices[ctx.author], choices[member]
    if c1 == c2: res = "Draw!"
    elif (c1=='rock' and c2=='scissors') or (c1=='paper' and c2=='rock') or (c1=='scissors' and c2=='paper'):
        res = f"{ctx.author.name} Wins!"
    else: res = f"{member.name} Wins!"
    await ctx.send(f"Results:\n{ctx.author.name}: {c1}\n{member.name}: {c2}\n**{res}**")

@bot.command()
async def tictactoe(ctx, p2: discord.Member):
    if p2.bot or p2 == ctx.author: return await ctx.send("Invalid player!")
    board = ["⬜"]*9
    turn = ctx.author
    def show(): return f"{board[0]}{board[1]}{board[2]}\n{board[3]}{board[4]}{board[5]}\n{board[6]}{board[7]}{board[8]}"
    msg = await ctx.send(f"Turn: {turn.mention} (1-9)\n{show()}")
    for _ in range(9):
        def check(m): return m.author == turn and m.channel == ctx.channel and m.content.isdigit() and 1<=int(m.content)<=9 and board[int(m.content)-1]=="⬜"
        try:
            m = await bot.wait_for('message', check=check, timeout=30.0)
            board[int(m.content)-1] = "❌" if turn == ctx.author else "⭕"
            await m.delete()
            for c in [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]:
                if board[c[0]]==board[c[1]]==board[c[2]]!="⬜":
                    return await ctx.send(f"🎉 {turn.mention} Wins!\n{show()}")
            turn = p2 if turn == ctx.author else ctx.author
            await msg.edit(content=f"Turn: {turn.mention}\n{show()}")
        except asyncio.TimeoutError: return await ctx.send("Game timed out.")
    await ctx.send("Draw!")

bot.run(os.getenv('DISCORD_TOKEN'))
