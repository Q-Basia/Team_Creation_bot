import discord
import os
from discord.channel import CategoryChannel
from discord.ext import commands
from discord.utils import find, get

# Following code loads the .env file located
# Can be commented out if the user wishes to use there own token
# just be sure to assign TOKEN your token value
from dotenv import load_dotenv
from dotenv.main import find_dotenv
load_dotenv(find_dotenv())
TOKEN = os.environ.get("TOKEN")

COUNT =0
# This line sets the prefix for any user activatable commands
client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# @client.event 
# async def on_typing(channel,user,when):
#     await channel.send(f'{user.mention} is a slow ass typer like hurry up you bitch, even my grandma is faster than you like come on!') 

# This is the default code for allowing users to designated themselves into a team
@client.command()
async def team(ctx):
    author = ctx.message.author
    # checks to make sure command is issued in a team-create channel
    if ctx.message.channel.name == "team-create":
        # creates the name of the team from the message sent
        role_name = ctx.message.content.split(maxsplit = 1)[1].split('<', maxsplit = 1)[0]
        role_check = get(ctx.guild.categories, name = role_name)
        # checks to see if team already exists and creates a new team if the team does not exist
        if role_check == None:
            await ctx.send(f'{ctx.author.mention}Your team {role_name} has been created!')
            cat = await ctx.guild.create_category(name= role_name)
            await ctx.guild.create_text_channel(name=role_name, category = cat)
            await ctx.guild.create_voice_channel(name=role_name, category=cat)
            role = await ctx.guild.create_role(name=role_name)
            members = ctx.message.mentions
            await author.add_roles(role)
            for i in members:
                await i.add_roles(role)
        else:
            await ctx.send(f'{ctx.author.mention}Team name has already been taken please use another one')

# Temp event to test bot functionallity for spammmed messages and confirming it doesn't miss anything
# @client.event
# async def on_message(message):
#     global COUNT
#     print(f"message logged #{COUNT}...")
#     COUNT+= 1
#     # await message.channel.send("message")

# Runs the bot with all applicable commands required   
client.run(TOKEN)
