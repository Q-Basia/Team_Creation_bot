import asyncio
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
TOKEN = os.environ.get("DISCORD_TOKEN")

COUNT = 0
# This line sets the prefix for any user activatable commands
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents = intents)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# @tasks.loop(count=1) 
# async def get_roles():
#     '''runs one time and prints all roles to stdout'''
#     await bot.wait_until_ready() # waits for bot to be ready
#     guild = bot.get_guild() # gets the guild object from an ID
#     roles = guild.roles # list of roles in guild
#     print('\n'.join(r.name for r in roles))  # prints the role names,
@bot.command(name = 'guilds')
async def get_roles(ctx):
    guild = ctx.guild
    roles = guild.roles
    print(roles)
    return roles

# This is the default code for allowing users to designated themselves into a team
@bot.command()
async def team(ctx):
    author = ctx.message.author
    guild = ctx.guild
    print(guild.get_role(1061456201986093156))
    # Finds the required roles needed in the guild
    participant = get(guild.roles, name = "Participant")
    sponsors = get(guild.roles, name = "Sponsor")
    mentors = get(guild.roles, name = "Mentor")
    volunteer = get(guild.roles, name = "Volunteer")
    basic = get(guild.roles, name = "@everyone")
    # checks to make sure command is issued in a team-create channel
    if ctx.message.channel.name == "team-create":
        # print(author.roles)
        # create list of "safe" roles - ones that don't belong to a team
        safe_roles = [1041047068342505472, 1041047068342505478, 1041065878701228087, 1050670927387574356, 1056462651166822483, 1041047068342505477, 1041047068342505476, 1041047068342505475, 1060082626741944392, 1041047068342505474, 1050642225673027624, 1056309816756285450, 1056314455857823784, 1061075633725263882, 1061588375007678514, 1061588681225424916, 1061588806660264017]
        has_team = False
        # loop through the user's roles
        for role in author.roles:
            print(role.id)
            if role.id not in safe_roles:
                # they're already in a team!
                has_team = True
        if has_team:
            return await ctx.send(f'Hey {ctx.author.mention}! You are already in a team!')
        # creates the name of the team from the message sent
        role_name = ctx.message.content.split(maxsplit = 1)[1].split('<', maxsplit = 1)[0]
        role_name = role_name.strip()
        # checks to see if team already exists and creates a new team if the team does not exist
        if get(ctx.guild.roles, name = role_name):
            await ctx.send(f'Hey {ctx.author.mention}, Team {role_name} has already been taken please use another one')
        else:
            # Creates a category, voice channel, and text channel for the team
            cat = await ctx.guild.create_category(name= role_name)
            # Makes the role
            new_role = await ctx.guild.create_role(name=role_name, mentionable = True, colour = discord.Colour(0x808080))
            # Privatizes channel so that only the team that made it can see it along with sponsor/mentor/volunteers
            await cat.set_permissions(participant, read_messages=False)
            await cat.set_permissions(basic, read_messages=False)
            await cat.set_permissions(sponsors, read_messages=True)
            await cat.set_permissions(mentors, read_messages=True)
            await cat.set_permissions(volunteer, read_messages=True)
            await cat.set_permissions(new_role, read_messages=True)
            # Creates the text and voice channel
            await ctx.guild.create_text_channel(name=role_name, category = cat)
            await ctx.guild.create_voice_channel(name=role_name, category=cat)
            # Gets team members
            members = ctx.message.mentions
            await author.add_roles(new_role)
            print(author)
            # Adds the created role to all team members
            for i in members:
                print(i)         
                has_team = False       
                for role in i.roles:
                    
                    print(role.id)
                    if role.id not in safe_roles:
                        # they're already in a team!
                        has_team = True
                if has_team:
                    await ctx.send(f'Hey {ctx.author.mention}! {i.name} is already in a team and so they were not added to the team')
                else:
                    await i.add_roles(new_role)
                # print(i)
            await ctx.send(f'Hey {ctx.author.mention}, Your team {role_name} has been created!')


bot.run(TOKEN)