# My summer project Discord bot
# By: Justin Vuu "jevuu"

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from random import randint
import json
import io
import os
import asyncio

class pilot:

    def __init__(self, uid:str, m:int = 10000, aP:int = 0, sF:int = 0, xp:int = 0):
        self.userID:str = uid
        self.money:int = m
        self.activePlane:int = aP
        self.sortiesFlown:int = sF
        self.experience:int = xp
    
    def modMoney(self, m:int):
        self.money += m


Client = discord.Client()
bot = commands.Bot(command_prefix = '.')
with open("Config/config.json") as loadConfig:
    config = json.load(loadConfig)
iSPilotsPath = "InfSkies/Pilots/"
iSDataPath = "InfSkies/Data/"
pilots = []
for filename in os.listdir(iSPilotsPath):
    with open(iSPilotsPath + filename) as loadPilot:
        lp = json.load(loadPilot)
    p = pilot(lp["userID"],lp["money"],lp["activePlane"],lp["sortiesFlown"])
    pilots.append(p)

async def bg_task_savePilots():
    await bot.wait_until_ready()
    while not bot.is_closed:
        await asyncio.sleep(5) # task runs every 5 seconds
        for p in pilots:
            filename:str = p.userID + ".json"
            with open(iSPilotsPath + filename, 'w') as output:
                json.dump(p.__dict__, output)
        print("Saved all pilot data!")

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

##Player data modification

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
        with open(iSPilotsPath + fileName, 'w') as output:
            json.dump(newPilot.__dict__, output)
        embed = discord.Embed(title = title + name, description = "Success! Welcome to the skies!")
    else:
        embed = discord.Embed(title = title + name, description = "You're already a pilot!")
    await bot.say(embed = embed)

@bot.command(pass_context = True)
async def modMoney(ctx, m:int):
    for p in pilots:
        if p.userID == ctx.message.author.id:
            pI = pilots.index(p)
            break
    
    pilots[pI].money += m

    title:str = "Modifying money for "
    name:str
    if ctx.message.author.nick == None:
        name = ctx.message.author.name
    else:
        name = ctx.message.author.nick
    embed = discord.Embed(title = title + name, description = pilots[pI].money)
    await bot.say(embed = embed)

##Player data retrieval

@bot.command(pass_context = True)
async def pilotInfo(ctx):
    members = ctx.message.mentions
    if len(members) == 1:
        title:str = "Pilot info for "
        name:str
        if members[0].nick == None:
            name = members[0].name
        else:
            name = members[0].nick
        
        pilotFound:bool = False
        for p in pilots:
            if p.userID == members[0].id:
                pI = pilots.index(p)
                pilotFound = True
                break

        if pilotFound == True:
            embed = discord.Embed(title = title + name)
            embed.set_thumbnail(url = members[0].avatar_url)
            embed.add_field(name = "Aircraft", value = pilots[pI].activePlane)
            embed.add_field(name = "Sorties", value = pilots[pI].sortiesFlown, inline = True)
            embed.add_field(name = "Credits", value = pilots[pI].money)
            embed.add_field(name = "Experience", value = pilots[pI].experience, inline = True)
        else:
            embed = discord.Embed(title = title + name, description = "They are not an active pilot!")

    elif len(members) > 1:
        embed = discord.Embed(title = "Pilot Lookup Error", description = "I can only search one pilot.")
    else:
        embed = discord.Embed(title = "Pilot Lookup Error", description = "You need to mention an active pilot.")

    #member = discord.Server.get_member(uid)
    await bot.say(embed = embed)

bot.loop.create_task(bg_task_savePilots())
bot.run(config["token"])