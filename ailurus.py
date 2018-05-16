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

    def __init__(self, uid:str, m:int = 10000, aP:str = "FA18ADV", sF:int = 0, xp:int = 0):
        self.userID:str = uid
        self.money:int = m
        self.activePlane:str = aP
        self.sortiesFlown:int = sF
        self.experience:int = xp
    
    def modMoney(self, m:int):
        self.money += m

class plane:

    def __init__(self, pid:str, name:str, role:str, dsc:str, prk:str, man:int, dfc:int, sth:int, gun:int, msl:int, sp1:str, sp1n:int, sp2:str, sp2n:int, cst:int):
        self.planeID:str = pid
        self.name:str = name
        self.role:str = role
        self.desc:str = dsc
        self.perkID:str = prk
        self.manoeuvrability:int = man
        self.defense:int = dfc
        self.stealth:int = sth
        self.gunAmmo:int = gun
        self.mslAmmo:int = msl
        self.sp1:str = sp1
        self.sp1Ammo:int = sp1n
        self.sp2:str = sp2
        self.sp2Ammo:int = sp2n
        self.cost:int = cst
        
class perk:
    def __init__(self, prkID:str, name:str, desc:str = "No description entered"):
        self.perkID:str = prkID
        self.name:str = name
        self.desc:str = desc

Client = discord.Client()
bot = commands.Bot(command_prefix = '.')
with open("Config/config.json") as loadConfig:
    config = json.load(loadConfig)

iSPilotsPath = "InfSkies/Pilots/"
iSPlanesPath = "InfSkies/Data/Planes/"
iSPerksPath = "InfSkies/Data/Perks/"

planes = []
for filename in os.listdir(iSPlanesPath):
    with open(iSPlanesPath + filename) as loadPlane:
        lp = json.load(loadPlane)
    pl = plane(lp["planeID"],lp["name"],lp["role"],lp["desc"],lp["perkID"],lp["manoeuvrability"],lp["defense"],lp["stealth"],lp["gunAmmo"],lp["mslAmmo"],lp["sp1"],lp["sp1Ammo"],lp["sp2"],lp["sp2Ammo"],lp["cost"])
    planes.append(pl)

perks = []
for filename in os.listdir(iSPerksPath):
    with open(iSPerksPath + filename) as loadPerk:
        lp = json.load(loadPerk)
    pl = perk(lp["perkID"],lp["name"],lp["desc"])
    perks.append(pl)

pilots = []
for filename in os.listdir(iSPilotsPath):
    with open(iSPilotsPath + filename) as loadPilot:
        lp = json.load(loadPilot)
    p = pilot(lp["userID"],lp["money"],lp["activePlane"],lp["sortiesFlown"],lp["experience"])
    pilots.append(p)

#=================
#General functions
#=================

def getName(author):
    authorName:str      #Get message author's name or nick
    if author.nick == None:
        authorName = author.name
    else:
        authorName = author.nick
    return authorName

#==================================
#Bot commands and event start below
#==================================

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

    name:str = getName(ctx.message.author)

    title:str = "Choosing for "
    
    if len(choiceList) <= 1:
        embed = discord.Embed(title = title + name, description = "You need to give me more than once choice!", thumbnail = ctx.message.author.avatar_url)
    else:
        embed = discord.Embed(title = title + name, description = choiceList[randint(0,len(choiceList)-1)], thumbnail = ctx.message.author.avatar_url)
    await bot.say(embed = embed)

#======================
# ROOM MANAGEMENT STUFF
#======================

## Defining a room
class room:
    def __init__(self, name:str, game:str, owner:str, members:str = None):
        self.name:str = name
        self.game:str = game
        self.owner:str = owner
        if members is None:
            self.members = []
        else:
            self.members = members

rooms = []      #A list of room objects

## ROOM COMMANDS

### MANAGING ROOMS

#Creating a room
@bot.command(pass_context = True)
async def makeroom(ctx, *msg:str):
    msgString = " ".join(msg)
    msgList = msgString.split(', ')
    newRoom = room(msgList[1], msgList[0], ctx.message.author.id)
    newRoom.members.append(ctx.message.author.id)
    rooms.append(newRoom)

    #authorName:str      #Get message author's name or nick
    #if ctx.message.author.nick == None:
    #    authorName = ctx.message.author.name
    #else:
    #    authorName = ctx.message.author.nick

    authorName:str = getName(ctx.message.author)

    await bot.send_message(ctx.message.channel, "Your room has been created, {}!".format(authorName))
    embed = discord.Embed(title = "Room Details")
    embed.add_field(name = "Name", value = newRoom.name, inline = False)
    embed.add_field(name = "Game", value = newRoom.game)
    for m in ctx.message.server.members:
        if m.id is newRoom.owner:
            roomOwner:str
            if m.nick == None:
                roomOwner = m.name
            else:
                roomOwner = m.nick
    embed.add_field(name = "Host", value = roomOwner)
    memnum:int = 0
    embedMembers:str = ""
    for rM in newRoom.members:
        memnum += 1
        for m in ctx.message.server.members:
            if m.id is rM:
                roomMember:str
                if m.nick == None:
                    roomMember = m.name
                else:
                    roomMember = m.nick
        embedMembers += "{}:\t{} \n".format(memnum, roomMember)
    embed.add_field(name = "Members", value = embedMembers, inline = False)
    await bot.say(embed = embed)

#Closing a room
@bot.command(pass_context = True)
async def closeroom(ctx):
    authorName:str = getName(ctx.message.author)

    if len(ctx.message.mentions) >= 1:
        if ctx.message.author.server_permissions.administrator is True or ctx.message.author.server_permissions.manage_server is True:
            findOwner = ctx.message.mentions[0].id
        else:
            findOwner = None
    else:
        findOwner = ctx.message.author.id

    if findOwner is not None:
        roomFound:bool = False

        for r in rooms:
            if r.owner is findOwner:
                del rooms[rooms.index(r)]
                roomFound = True
                break

        if roomFound is True:
            await bot.send_message(ctx.message.channel, "The room has been closed, {}".format(authorName))
        else:
            await bot.send_message(ctx.message.channel, "You don't have a room, {}".format(authorName))         
    else:
        await bot.send_message(ctx.message.channel, "You do not have permission to close other's rooms, {}".format(authorName))

#Joining rooms
@bot.command(pass_context = True)
async def joinroom(ctx):
    authorName:str = getName(ctx.message.author)
    
    if len(ctx.message.mentions) >= 1:
        findOwner = ctx.message.mentions[0].id
    else:
        findOwner = None

    if findOwner is not None:
        roomFound:bool = False

        for r in rooms:
            if r.owner is findOwner:
                roomFound = True
                alreadyInRoom:bool = False

                for rM in r.members:
                    if rM is ctx.message.author.id:
                        alreadyInRoom = True
                        break
                
                if alreadyInRoom is False:
                    r.members.append(ctx.message.author.id)
                    embed = discord.Embed(title = "Room Details")
                    embed.add_field(name = "Name", value = r.name, inline = False)
                    embed.add_field(name = "Game", value = r.game)
                    for m in ctx.message.server.members:
                        if m.id is r.owner:
                            roomOwner:str
                            if m.nick == None:
                                roomOwner = m.name
                            else:
                                roomOwner = m.nick
                    embed.add_field(name = "Host", value = roomOwner)
                    memnum:int = 0
                    embedMembers:str = ""
                    for rM in r.members:
                        memnum += 1
                        for m in ctx.message.server.members:
                            if m.id is rM:
                                roomMember:str
                                if m.nick == None:
                                    roomMember = m.name
                                else:
                                    roomMember = m.nick
                        embedMembers += "{}:\t{} \n".format(memnum, roomMember)
                    embed.add_field(name = "Members", value = embedMembers, inline = False)
                    await bot.say(embed = embed)
                else:
                    await bot.send_message(ctx.message.channel, "You are already in the room, {}".format(authorName))

                break
        
        if roomFound is False:
            await bot.send_message(ctx.message.channel, "No room found, {}".format(authorName))
    else:
        await bot.send_message(ctx.message.channel, "You need to mention the room's host to join them, {}".format(authorName))

#Kick from room
@bot.command(pass_context = True)
async def roomkick(ctx):
    authorName:str = getName(ctx.message.author)
    
    authorID:str = ctx.message.author.id

    findMember:str      #Get the ID of the mentioned member we want to kick
    if len(ctx.message.mentions) >= 1:
        findMember = ctx.message.mentions[0].id
    else:
        findMember = None

    #If the member is found, search through rooms list for the author's room, then remove the
    #member we want to kick.
    if findMember is not None:
        roomFound:bool = False

        for r in rooms:
            if r.owner is authorID:
                roomFound = True
                memberFound:bool = False

                for rM in r.members:
                    if rM is findMember:
                        mbrIndex = r.members.index(rM)
                        memberFound = True
                        break
                
                if memberFound is True:
                    del r.members[mbrIndex]
                    await bot.send_message(ctx.message.channel, "The member has been removed, {}".format(authorName))
                    embed = discord.Embed(title = "Room Details")
                    embed.add_field(name = "Name", value = r.name, inline = False)
                    embed.add_field(name = "Game", value = r.game)
                    for m in ctx.message.server.members:
                        if m.id is r.owner:
                            roomOwner:str
                            if m.nick == None:
                                roomOwner = m.name
                            else:
                                roomOwner = m.nick
                    embed.add_field(name = "Host", value = roomOwner)
                    memnum:int = 0
                    embedMembers:str = ""
                    for rM in r.members:
                        memnum += 1
                        for m in ctx.message.server.members:
                            if m.id is rM:
                                roomMember:str
                                if m.nick == None:
                                    roomMember = m.name
                                else:
                                    roomMember = m.nick
                        embedMembers += "{}:\t{} \n".format(memnum, roomMember)
                    embed.add_field(name = "Members", value = embedMembers, inline = False)
                    await bot.say(embed = embed)
                else:
                    await bot.send_message(ctx.message.channel, "User is not in your room, {}".format(authorName))

                break
        
        if roomFound is False:
            await bot.send_message(ctx.message.channel, "You don't have a room, {}".format(authorName)) 
    else:
        await bot.send_message(ctx.message.channel, "You need to mention the member to kick them, {}".format(authorName))

### VIEWING ROOMS
@bot.command(pass_context = True)
async def viewroom(ctx):
    authorName:str = getName(ctx.message.author)

    if len(ctx.message.mentions) is 0:
        findOwner = ctx.message.author.id
    else:
        findOwner = ctx.message.mentions[0].id

    roomFound:bool = False
    for r in rooms:
        if r.owner is findOwner:
            embed = discord.Embed(title = "Room Details")
            embed.add_field(name = "Name", value = r.name, inline = False)
            embed.add_field(name = "Game", value = r.game)
            for m in ctx.message.server.members:
                if m.id is r.owner:
                    roomOwner:str
                    if m.nick == None:
                        roomOwner = m.name
                    else:
                        roomOwner = m.nick
            embed.add_field(name = "Host", value = roomOwner)
            memnum:int = 0
            embedMembers:str = ""
            for rM in r.members:
                memnum += 1
                for m in ctx.message.server.members:
                    if m.id is rM:
                        roomMember:str
                        if m.nick == None:
                            roomMember = m.name
                        else:
                            roomMember = m.nick
                embedMembers += "{}:\t{} \n".format(memnum, roomMember)
            embed.add_field(name = "Members", value = embedMembers, inline = False)
            roomFound = True
            await bot.say(embed = embed)
            break
    
    if roomFound is False:
        await bot.send_message(ctx.message.channel, "No room found, {}".format(authorName))


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
            for plane in planes:
                if plane.planeID == pilots[pI].activePlane:
                    planeName = plane.name
                    break

            embed = discord.Embed(title = title + name)
            embed.set_thumbnail(url = members[0].avatar_url)
            embed.add_field(name = "Aircraft", value = planeName)
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

@bot.command(pass_context = True)
async def testPlane(ctx):
    testPerks = []
    testPlanes = []

    testPerk = perk("VERS", "Versatile", "Slightly increases MSL and gun damage against the more common target type.")
    testPerks.append(testPerk)

    testPerk = perk("JSTRIKE", "Joint Strike", "Increases damage relative to the number of allies.")
    testPerks.append(testPerk)

    testPerk = perk("30MM", "30mm Aesthetic", "Significantly increased gun damage.")
    testPerks.append(testPerk)

    testPerk = perk("NIGHT", "Night Striker", "Small chance to go unnoticed in a sortie.")
    testPerks.append(testPerk)

    testPerk = perk("SANIC", "Interceptor", "Reduces ground-based threat level.")
    testPerks.append(testPerk)

    for prk in testPerks:
        fileName:str = prk.perkID + ".json"
        with open(iSPerksPath + fileName, 'w') as output:
            json.dump(prk.__dict__, output)

    testPlane = plane("FA18ADV", "Advanced Super Hornet", "Multirole", "An experimental multirole fighter with CFTs and stealth", "VERS", 50, 50, 1, 560, 20, "AAM4", 10, "AGML", 10, "5000")
    testPlanes.append(testPlane)

    testPlane = plane("F35A", "F-35A Lightning II", "Multirole", "Advanced stealth aircraft designed to work in tandem with allied units", "JSTRIKE", 70, 60, 2, 400, 20, "AAML", 10, "GPBS", 10, "10000")
    testPlanes.append(testPlane)

    testPlane = plane("A10C", "A-10C Thunderbolt II", "Attacker", "The world's only gun with a plane accessory. The 30mm gun shreds ground targets with ease.", "30MM", 20, 90, 0, 1000, 20, "RKTL", 10, "UGBL", 10, "7000")
    testPlanes.append(testPlane)

    testPlane = plane("F117", "F-117A", "Attacker", "Stealth attacker used for precision strikes in enemy territory.", "NIGHT", 20, 70, 3, 0, 20, "GPBL", 10, "AGML", 10, "6000")
    testPlanes.append(testPlane)

    testPlane = plane("MIG31", "MiG-31", "Fighter", "Designed to intercept high speed threats, it can use its speed to get out of danger quickly.", "SANIC", 100, 40, 0, 0, 20, "AAML", 10, "AAM4", 10, "7000")
    testPlanes.append(testPlane)

    for pln in testPlanes:
        fileName:str = pln.planeID + ".json"
        with open(iSPlanesPath + fileName, 'w') as output:
            json.dump(pln.__dict__, output)

        for prk in perks:
            if prk.perkID == pln.perkID:
                perkName:str = prk.name
                break

        embed = discord.Embed(title = "Plane Info")
        embed.add_field(name = "Name", value = pln.name, inline = False)
        embed.add_field(name = "Role", value = pln.role)
        embed.add_field(name = "Perk", value = perkName)
        embed.add_field(name = "Manoeuvrability", value = pln.manoeuvrability)
        embed.add_field(name = "Defense", value = pln.defense)
        embed.add_field(name = "Stealth Level", value = pln.stealth)
        embed.add_field(name = "Gun Ammo", value = pln.gunAmmo)
        embed.add_field(name = "MSL Ammo", value = pln.mslAmmo)
        embed.add_field(name = "Sp. Weapon 1", value = "{}: {}".format(pln.sp1, pln.sp1Ammo))
        embed.add_field(name = "Sp. Weapon 2", value = "{}: {}".format(pln.sp2, pln.sp2Ammo))
        embed.add_field(name = "Cost", value = pln.cost)
        embed.add_field(name = "Description", value = pln.desc, inline = False)

        await bot.say(embed = embed)

@bot.command(pass_context = True)
async def seePlane(ctx, *plane:str):
    planeString:str = " ".join(plane)
    for p in planes:
        if p.name == planeString:

            for prk in perks:
                if prk.perkID == p.perk:
                    perk:str = prk.name
                    break

            embed = discord.Embed(title = "Plane Info")
            embed.add_field(name = "Name", value = p.name)
            embed.add_field(name = "Role", value = p.role)
            embed.add_field(name = "Description", value = p.desc)
            embed.add_field(name = "Perk", value = perk)
            embed.add_field(name = "Manoeuvrability", value = p.speed)
            embed.add_field(name = "Defense", value = p.defence)
            embed.add_field(name = "Stealth Level", value = p.stealth)
            embed.add_field(name = "Gun Ammo", value = p.gunAmmo)
            embed.add_field(name = "MSL Ammo", value = p.mslAmmo)
            embed.add_field(name = "Sp. Weapon 1", value = "{} {}".format(p.sp1, p.sp1Ammo))
            embed.add_field(name = "Sp. Weapon 2", value = "{} {}".format(p.sp2, p.sp2Ammo))
            embed.add_field(name = "Cost", value = p.cost)
        else:
            embed = discord.Embed(title = "Plane not found")
    await bot.say(embed = embed)

bot.loop.create_task(bg_task_savePilots())
bot.run(config["token"])