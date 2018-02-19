import os
import discord
from discord.ext import commands
import asyncio
import markovify

description = 'Zbot2.0.'
bot = commands.Bot(command_prefix='!', description=description)

def mchain(parse):
        text_model = markovify.NewlineText(parse)
        return(str(text_model.make_short_sentence(140)))

async def markov_gen(author, channel, message_contents, bot):

    if len(message_contents) > 1:
        markov_target = message_contents[1]
        if author != bot:
            print (markov_target)

            updating_archive = open('updating_archive.log', 'w', encoding='utf-8')

            async for message_contents in bot.logs_from(channel, limit=500):
                updating_archive.write(str(author)+' '+str(message_contents)+'\n')

            updating_archive.close()

            markov_target_parsed = open(markov_target+'.log', 'w', encoding='utf-8')

            number_of_lines = 0
            updating_archive = open('updating_archive.log', 'r', encoding='utf-8')
            for line in updating_archive:
                if line.startswith(markov_target):
                    markov_target_parsed.write(str(line[len(markov_target):].strip()+'\n'))
                    number_of_lines += 1

            markov_target_parsed.close()
            updating_archive.close()

            print (str(number_of_lines) + ' lines containing '+(str(markov_target)))
            if number_of_lines == 0:
                await bot.say("This person does not exist in my archives. Remember that names are case sensitive.")
                os.remove(markov_target+'.log')
                print ("Useless log file deleted")
            else:
                markov_output = open(markov_target+'.log', 'r', encoding='utf-8').read()
                await bot.say(mchain(markov_output))
                print ("Generation successful!")
    else:
        await bot.say("No target specified.")
