# My summer project Discord bot
# By: Justin Vuu "jevuu"

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from random import randint
import json
import io
import asyncio

Client = discord.Client()
bot = commands.Bot(command_prefix = '.')
pilots = []

@bot.event
async def on_ready():
    print("AilurusBot ready for action!")

@bot.event
async def on_message(message):
    if message.content == "cookie":
        await bot.send_message(message.channel, ":cookie:")
    #Need this so our commands don't break:
    else:
        await bot.process_commands(message)

@bot.command(pass_context = True)
async def ping(ctx):
    await bot.say("Pong!")
    print ("user pinged")

@bot.command(pass_context = True)
async def add(ctx, a:int, b:int):
    total = a + b
    member = ctx.message.author
    nick:str
    if member.nick == None:
        nick = member.name
    else:
        nick = member.nick

    title:str = "Adding for "
    embed = discord.Embed(title = title + nick, description = total)
    await bot.say(embed = embed)

@bot.command(pass_context = True)
async def pick(ctx, *choices:str):
    choiceString:str = " ".join(choices)
    choiceList = choiceString.split(',') #Creates array of choices from content
    
    c:int = 0
    while c < len(choiceList):
        if choiceList[c] == "":
            del choiceList[c]
        else:
            c += 1

    name:str
    if ctx.message.author.nick == None:
        name = ctx.message.author.name
    else:
        name = ctx.message.author.nick

    title:str = "Choosing for "
    
    if len(choiceList) <= 1:
        embed = discord.Embed(title = title + name, description = "You need to give me more than once choice!", thumbnail = ctx.message.author.avatar_url)
    else:
        embed = discord.Embed(title = title + name, description = choiceList[randint(0,len(choiceList)-1)], thumbnail = ctx.message.author.avatar_url)
    await bot.say(embed = embed)


#GAME STUFF

@bot.command(pass_context = True)
async def playInf(ctx):
    title:str = "Infinite Skies registration for "
    name:str
    if ctx.message.author.nick == None:
        name = ctx.message.author.name
    else:
        name = ctx.message.author.nick

    pilotFound:bool = False
    for p in pilots:
        if p.userID == ctx.message.author.id:
            pilotFound = True
            break
    
    if pilotFound == False:
        newPilot = pilot(ctx.message.author.id)
        pilots.append(newPilot)
        fileName:str = ctx.message.author.id + ".json"
        with open(fileName, 'w') as output:
            json.dump(newPilot.__dict__, output)
        embed = discord.Embed(title = title + name, description = "Success! Welcome to the skies!")
    else:
        embed = discord.Embed(title = title + name, description = "You're already a pilot!")
    
    await bot.say(embed = embed)

@bot.command(pass_context = True)
async def modMoney(ctx, b:int):
    p = pilot("test")
    p.modMoney(b)

    await bot.say(p.money)
    
class pilot:

    def __init__(self, uid:str):
        self.userID:str = uid
        self.money:int = 10000
        self.activePlane:int = 0
        self.sortiesFlown:int = 0
    
    def modMoney(self, m:int):
        self.money += m

with open("config.json", 'r') as loadConfig:
    config = json.loads(loadConfig)

bot.run(config['key'])