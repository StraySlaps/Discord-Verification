import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

GUILD_ID = 936959862955462717
VERIFY_CHANNEL_ID = 938303446036148264
VERIFY_ROLE_NAME = "Verified"
 
    @bot.event
    async def on_ready():
        print(f"Bot is ready. Logged in as {bot.user}")
 
    @bot.event
    async def on_member_join(member):
        guild = member.guild
        channel = guild.get_channel(VERIFY_CHANNEL_ID)
  
        if channel:
            msg = await channel.send(f"""Welcome {member.mention}!
    Please click ✅ to verify that you agree to the rules...
    (RULES GO HERE)
    """)
            await msg.add_reaction("✅")
    
            def check(reaction, user):
                return (
                    user == member and
                    str(reaction.emoji) == "✅" and
                    reaction.message.id == msg.id
                )
   
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=300.0, check=check)
                role = discord.utils.get(guild.roles, name=VERIFY_ROLE_NAME)
                if role:
                    await member.add_roles(role)
                    await channel.send(f"{member.mention} has been verified ✅")
                else:
                    await channel.send("Verification role not found.")
            except:
                await channel.send(f"{member.mention} didn't verify in time ⏰")
  
    keep_alive()
