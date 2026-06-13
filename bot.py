import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
GUILD_ID = 1477447173120458782
CHANNEL_ID = 1497068548722266122

MAX_LEDEN = 25

ROLES = [
    "👑 Boss",
    "🧠 Underboss",
    "⚡ Righthand (Lead)",
    "🔥 Core",
    "⚙️ Operator",
    "🪖 Soldier",
    "🤝 Associate",
    "🔰 Prospect",
    "🏠 Hangaround"
]

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

message_id = None


async def maak_ledenlijst():
    guild = bot.get_guild(GUILD_ID)

    totaal = 0

    for role_name in ROLES:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            totaal += len(role.members)

    tekst = f"🔥 **SMOKE | LEDENLIJST {totaal}/{MAX_LEDEN}** 🔥\n\n"

    for role_name in ROLES:
        role = discord.utils.get(guild.roles, name=role_name)

        tekst += f"**{role_name}**\n\n"

        if role and len(role.members) > 0:
            leden = sorted(role.members, key=lambda lid: lid.display_name.lower())

            for lid in leden:
                tekst += f"{lid.mention}\n"

        tekst += "\n"

    return tekst


async def update_lijst():
    global message_id

    guild = bot.get_guild(GUILD_ID)
    channel = bot.get_channel(CHANNEL_ID)

    if guild is None or channel is None:
        return

    tekst = await maak_ledenlijst()

    if message_id:
        try:
            bericht = await channel.fetch_message(message_id)
            await bericht.edit(content=tekst)
            return
        except:
            pass

    bericht = await channel.send(tekst)
    message_id = bericht.id


@bot.event
async def on_ready():
    print(f"Ingelogd als {bot.user}")
    await update_lijst()


@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        await update_lijst()


@bot.event
async def on_member_join(member):
    await update_lijst()


@bot.event
async def on_member_remove(member):
    await update_lijst()


@bot.command()
async def refresh(ctx):
    await update_lijst()
    await ctx.send("✅ Ledenlijst bijgewerkt.", delete_after=5)


bot.run(TOKEN)
