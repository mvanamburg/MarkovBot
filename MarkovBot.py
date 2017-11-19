import os
import discord
import asyncio
import markovify

client = discord.Client()

def mchain(parse):
    text_model = markovify.NewlineText(parse)
    return(str(text_model.make_short_sentence(140)))

@client.event
async def on_ready():
    print('Logged in as'+ ' '+ client.user.name)
@client.event
async def on_message(message):
    if message.content.startswith('!markov') and message.author != client.user:

        markov_target = message.content[len('!markov'):].strip()

        if bool(markov_target)==False:
            print("No target specified.")
            await client.send_message(message.channel, ("No target specified."))
        else:
            print (markov_target)

            updating_archive = open('updating_archive.log', 'w', encoding='utf-8')

            async for message in client.logs_from(message.channel, limit=500):
                updating_archive.write(str(message.author)[:-5]+' '+str(message.content)+'\n')

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
                await client.send_message(message.channel, ("This person does not exist in my archives. Remember that names are case sensitive."))
                os.remove(markov_target+'.log')
                print ("Useless log file deleted")
            else:
                markov_output = open(markov_target+'.log', 'r', encoding='utf-8').read()
                await client.send_message(message.channel, (mchain(markov_output)))
                print ("Generation successful!")

#Definitely didnt steal this part
if __name__ == '__main__':
    with open("creds") as f:
        creds = f.readlines()[0].strip()
client.run(creds)
