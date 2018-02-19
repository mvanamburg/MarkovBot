import discord
import asyncio
from discord.ext import commands

description = 'Zbot2.0.'
bot = commands.Bot(command_prefix='!', description=description)

discord_colors = discord.Color.__dict__
colors = list(filter(lambda x: isinstance(discord_colors[x], classmethod), discord_colors))
colors.sort()

#This function gets called when the bot starts -- checks to see if roles for all colors exist and creates them if they do not.
async def create_roles(server, bot):
    print("Creating roles for " + server.name)
    role_names = list(map(lambda r: r.name, server.roles))
    to_create = list(filter(lambda x: x not in role_names, colors))

    for color in to_create:
            await bot.create_role(server, name=color, color=getattr(discord.Color, color)())
            print("Created " + color)

#!color calls this function -- Changes the color of the user's name.
async def handle_color(message, author, server_roles, bot):
    words = message.split(' ')
    if len(words) != 2:
        await bot.say('Available colors are:\n' + (', '.join(colors)))
    if len(words) == 2:
        if (words[1] not in colors):
            await bot.say('That is not a valid color.')
        else:

            print('Changing ' + author.name + '\'s color to ' + words[1])

            old_roles = list(filter(lambda r: r.name not in colors, author.roles))
            color_role = list(filter(lambda r: r.name == words[1], server_roles))[0]
            new_roles = old_roles + [color_role]

            await bot.replace_roles(author, *new_roles)
            await bot.say('Changed your color to ' + words[1])
