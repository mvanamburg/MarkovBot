import discord
import asyncio
from discord.ext import commands
from modules.roll import roll_die
from modules.rolehandler import handle_color
from modules.rolehandler import create_roles
from modules.markov import markov_gen

description = 'Zbot2.0.'
bot = commands.Bot(command_prefix='!', description=description)

@bot.command(pass_context=True) #!color allows a user to change the color of their name.
async def color(ctx):
    message = ctx.message.content
    author = ctx.message.author
    server_roles = ctx.message.server.roles
    await handle_color(message, author, server_roles, bot)

@bot.command(pass_context=True) #!roll generates a random number in a user-defined range.
async def roll(ctx, roll_min = None, roll_max = None):
    if isinstance(roll_min, int) == True and isinstance(roll_min, int) == True:
        member = ctx.message.author
        output = roll_die(roll_min, roll_max)
        await bot.say('{0}'.format(member.mention) + str(output))
    else:
        await bot.say('Rolling requires two integer arguments.')

@bot.command(pass_context=True)
async def markov(ctx):#!markov uses markovify to generate sentences based on a user's discord messages.
    message_contents = str(ctx.message.content).split(' ')
    author = ctx.message.author
    channel = ctx.message.channel
    await markov_gen(author, channel, message_contents, bot)

@bot.event
async def on_ready():
    print('Logged in as'+ ' ' + bot.user.name)
    for server in bot.servers:
        await create_roles(server, bot)
        #await refresh_roles(server)

#Definitely didnt steal this part
if __name__ == '__main__':
    with open("creds") as f:
        creds = f.readlines()[0].strip()
bot.run(creds)
