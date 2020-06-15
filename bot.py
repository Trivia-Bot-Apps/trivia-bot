# -*- coding: utf8 -*-
import smtplib
import discord
from operator import itemgetter
import requests
import random
import asyncio
import aiohttp
import urllib
import random
import urllib.parse, urllib.request, re
from discord import Game
from json import loads
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord.ext import commands, tasks
import sys
import time
import redis
import os
import json
import dbl
import logging
import subprocess

userspecific = True
yesemoji = '👍'
noemoji = '👎'
TOKEN = os.getenv('bottoken')
if TOKEN == None:
    TOKEN = input("Token Please:")

redisurl = os.getenv('REDIS_URL')
if redisurl == None:
    redisurl = input('Please enter the REDIS URL:')

dbl_token = os.getenv('DBL_TOKEN')

HEROKU_RELEASE_CREATED_AT = os.getenv('HEROKU_RELEASE_CREATED_AT')
HEROKU_RELEASE_VERSION = os.getenv('HEROKU_RELEASE_VERSION')
HEROKU_SLUG_COMMIT = os.getenv('HEROKU_SLUG_COMMIT')
HEROKU_SLUG_DESCRIPTION = os.getenv('HEROKU_SLUG_DESCRIPTION')

triviadb = redis.from_url(redisurl)

prefix = dbl_token = os.getenv('prefix')

if prefix == None:
    prefix = ";"
client = commands.Bot(command_prefix=prefix)

def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel

def checkvote(userid):
    headers = {'Authorization': dbl_token}
    voteurl = requests.get("https://top.gg/api/bots/715047504126804000/check?userId="+str(userid), headers = headers).text
    voted = int(loads(voteurl)["voted"])
    if voted == 1:
        return True
    else:
        return False

async def get_reaction_answer(msg, author, q, a, ctx):
    def checkreaction(reaction, user):
        return (user.id == author or not userspecific) and reaction.message.id == msg.id and str(reaction.emoji) in [yesemoji, noemoji]
    await msg.add_reaction(yesemoji)
    await msg.add_reaction(noemoji)
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=checkreaction)
    except asyncio.TimeoutError:
        try:
            await msg.clear_reactions()
        except:
            thisisfornothing = 1
        tbpoints("take", author, 1)
        qembed=discord.Embed(title="Answered Problem", description="This problem has expired", color=0xff0000)
        qembed.add_field(name="The Question Was:", value=str(q), inline=False)
        qembed.add_field(name="The Submitted Answer Was", value="Expired", inline=False)
        qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
        qembed.add_field(name="Points",value="You lost a point since this question expired! Sorry :(", inline=False)
        message = await msg.edit(embed=qembed)
    return [yesemoji, noemoji].index(str(reaction.emoji)) + 1

def tbpoints(statement, key, amount):
    if statement == "get":
        userid = key
        try:
            points = int(triviadb.hgetall("data")[userid.encode('ascii')])
        except:
            points = 0
        return points
    if statement == "give":
        userid = key
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode('ascii')] = int(bytedb[key].decode('ascii'))
        try:
            stringdb[userid] += int(amount)
        except:
            stringdb[userid] = int(amount)
        triviadb.hmset("data", stringdb)
    if statement == "take":
        userid = key
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode('ascii')] = int(bytedb[key].decode('ascii'))
        stringdb[str(userid)] -= int(amount)
        triviadb.hmset("data", stringdb)
    if statement == "set":
        userid = key
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode('ascii')] = int(bytedb[key].decode('ascii'))

        stringdb[userid] = int(amount)
        triviadb.hmset("data", stringdb)
    if statement == "data":
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode('ascii')] = int(bytedb[key].decode('ascii'))
        return stringdb

@client.command()
async def trivia(ctx, category=None):
    global triviatoken
    if category == None:
        r = requests.get("https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="+str(triviatoken)).text
        lesspoints = False
    else:
        listofdata = {"general":"9","books":"10","film":"11","music":"12","musicals":"13","tv":"14","gaming":"15","boardgames":"16","science":"17","computers":"18","math":"19","myths":"20","sports":"21","geography":"22","history":"23","politics":"24","art":"25","people":"26","animals":"27","cars":"28","comics":"29","gadgets":"30","anime":"31","cartoons":"32"}
        try: categorynumber = listofdata[str(category)]
        except KeyError():
            r = requests.get("https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="+str(triviatoken)).text
            lesspoints = False
        else:
            r = requests.get("https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&category="+categorynumber+"&token="+str(triviatoken)).text
            lesspoints = True
    rc = loads(r)["response_code"]
    if rc != 0:
        n = requests.get("https://opentdb.com/api_token.php?command=request").text
        triviatoken = urllib.parse.unquote(loads(n)['token'])
        if category == None:
            r = requests.get("https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="+str(triviatoken)).text
            lesspoints = False
        else:
            listofdata = {"general":"9","books":"10","film":"11","music":"12","musicals":"13","tv":"14","gaming":"15","boardgames":"16","science":"17","computers":"18","math":"19","myths":"20","sports":"21","geography":"22","history":"23","politics":"24","art":"25","people":"26","animals":"27","cars":"28","comics":"29","gadgets":"30","anime":"31","cartoons":"32"}
            try: categorynumber = listofdata[str(category)]
            except KeyError():
                r = requests.get("https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="+str(triviatoken)).text
                lesspoints = False
            else:
                r = requests.get("https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&category="+categorynumber+"&token="+str(triviatoken)).text
                lesspoints = True
    q = urllib.parse.unquote(loads(r)['results'][0]['question'])
    a = urllib.parse.unquote(loads(r)['results'][0]['correct_answer'])
    b = q + a
    qembed=discord.Embed(title="YOUR QUESTION", description="Use the below reactions to answer this true/false question.", color=0xff0000)
    qembed.add_field(name="Question:", value=str(q), inline=False)
    qembed.add_field(name=yesemoji, value="For true", inline=True)
    qembed.add_field(name=noemoji, value="For false", inline=True)
    diduservote = checkvote(ctx.message.author.id)
    if not diduservote:
        qembed.add_field(name="Notice:", value="Want to get 2x Points? Vote for us using ;vote", inline=False)
    msg = await ctx.send(embed=qembed)
    answer = await get_reaction_answer(msg, ctx.message.author.id, q, a, ctx)
    uid = ctx.message.author.id
    if answer == 1:
        textanswer = yesemoji
    else:
        textanswer = noemoji
    if diduservote:
        multiplier = 2
    else:
        multiplier = 1
    if lesspoints:
        pointstogive = 1 * multiplier
        message = " (Chose a category)"
        if diduservote:
            message = " (Chose a category and voted)"
    else:
        pointstogive = 2 * multiplier
        message = " (Didn't chose a category)"
        if diduservote:
            message = " (Didn't chose a category and voted)"

    if a == "True":
        if answer == 1:
            tbpoints("give", str(uid), pointstogive)
            try:
                await msg.clear_reactions()
            except:
                hahalols = 1
            qembed=discord.Embed(title="Answered Problem", description="This problem has already been answered", color=0xff0000)
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(name="The Submitted Answer Was", value=textanswer, inline=False)
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(name="Points",value="You got "+str(pointstogive)+" point(s)! Nice Job!"+message, inline=False)
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("✅")
        elif answer == 2:
            tbpoints("give", str(uid), -1)
            try:
                await msg.clear_reactions()
            except:
                chatgoesboom = 12
            qembed=discord.Embed(title="Answered Problem", description="This problem has already been answered", color=0xff0000)
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(name="The Submitted Answer Was", value=textanswer, inline=False)
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(name="Points",value="You lost 1 point! Sorry :(", inline=False)
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("❌")
    elif a == "False":
        if answer == 1:
            tbpoints("give", str(uid), -1)
            try:
                await msg.clear_reactions()
            except:
                waitwhat = 9
            qembed=discord.Embed(title="Answered Problem", description="This problem has already been answered", color=0xff0000)
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(name="The Submitted Answer Was", value=textanswer, inline=False)
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(name="Points",value="You lost 1 point! Sorry :(", inline=False)
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("❌")
        elif answer == 2:
            tbpoints("give", str(uid), pointstogive)
            try:
                await msg.clear_reactions()
            except:
                finaloneyay = 1993
            qembed=discord.Embed(title="Answered Problem", description="This problem has already been answered", color=0xff0000)
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(name="The Submitted Answer Was", value=textanswer, inline=False)
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(name="Points",value="You got "+str(pointstogive)+" point(s)! Nice Job!"+message, inline=False)
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("✅")

@client.command(aliases=['debug'])
async def triviadebug(ctx):
    data = tbpoints("data",0,0)
    datalist = data.items()
    await ctx.send(str(data))

@client.command(aliases=['top'])
async def globalleaderboard(ctx):
    data = tbpoints("data",0,0)
    datalist = data.items()
    sorteddata = sorted(datalist,key=itemgetter(1),reverse=True)
    try:
        firstuserid = int(sorteddata[0][0])
    except:
        firstuserid = "null"
    try:
        seconduserid = int(sorteddata[1][0])
    except:
        seconduserid = "null"
    try:
        thirduserid = int(sorteddata[2][0])
    except:
        thirduserid = "null"
    try:
        firstpoints = data[str(firstuserid)]
    except:
        firstpoints = "null"
    try:
        secondpoints = data[str(seconduserid)]
    except:
        secondpoints = "null"
    try:
        thirdpoints = data[str(thirduserid)]
    except:
        thirdpoints = "null"
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(
        title='Leaderboard',
        description='Top Globally',
        color=discord.Colour.from_rgb(r, g, b),
    )
    data = str(data)
    user1 = client.get_user(firstuserid)
    user2 = client.get_user(seconduserid)
    user3 = client.get_user(thirduserid)
    firstmessage = "{0} with {1} points".format(str(user1),str(firstpoints))
    secondmessage = "{0} with {1} points".format(str(user2),str(secondpoints))
    thirdmessage = "{0} with {1} points".format(str(user3),str(thirdpoints))
    embed.add_field(name='1st Place', value=firstmessage)
    embed.add_field(name='2nd Place', value=secondmessage)
    embed.add_field(name='3rd Place', value=thirdmessage)
    await ctx.send(embed=embed)


@client.command(aliases=['servertop'])
async def serverleaderboard(ctx):
    data = tbpoints("data",0,0)
    server_members=[]
    first_found=False
    second_found=False
    third_found=False
    datalist = data.items()
    sorteddata = sorted(datalist,key=itemgetter(1),reverse=True)
    for id in ctx.guild.members:
        id = id.id
        server_members.append(str(id))
    server_members = sorted(server_members, key=lambda x:data.get(x,0), reverse=True)
    try:
        firstuserid = server_members[0]
    except:
        firstuserid = "null"
    try:
        seconduserid = server_members[1]
    except:
        seconduserid = "null"
    try:
        thirduserid = server_members[2]
    except:
        thirduserid = "null"
    try:
        firstpoints = data[firstuserid]
    except:
        firstpoints = "null"
    try:
        secondpoints = data[seconduserid]
    except:
        secondpoints = "null"
    try:
        thirdpoints = data[thirduserid]
    except:
        thirdpoints = "null"
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(
        title='Leaderboard',
        description='Top in this Server',
        color=discord.Colour.from_rgb(r, g, b),
    )
    data = str(data)
    firstmessage = "<@" + str(firstuserid) + "> with " + str(firstpoints) + " points!"
    secondmessage = "<@" + str(seconduserid) + "> with " + str(secondpoints) + " points!"
    thirdmessage = "<@" + str(thirduserid) + "> with " + str(thirdpoints) + " points!"
    embed.add_field(name='1st Place', value=firstmessage)
    embed.add_field(name='2nd Place', value=secondmessage)
    embed.add_field(name='3rd Place', value=thirdmessage)
    await ctx.send(embed=embed)

@client.command()
async def points(ctx):
    r = 215
    g = 91
    b = 69
    uid = ctx.message.author.id
    username = "<@"+str(uid)+">"
    current_points = tbpoints("get",str(uid),0)
    embed = discord.Embed(
        title='Your Points',
        description='The amount of points you have.',
        color=discord.Colour.from_rgb(r, g, b),
    )
    embed.add_field(name='Username', value=username)
    embed.add_field(name='Points', value=current_points)
    await ctx.send(embed=embed)

@client.command()
async def vote(ctx):
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(
        title='Vote for Trivia Bot',
        description='Voting for Trivia Bot grants you a 2x points multiplier for 12 hours! (Please wait 5 minutes after voting)',
        color=discord.Colour.from_rgb(r, g, b),
    )
    embed.add_field(name='top.gg', value='https://top.gg/bot/715047504126804000/vote')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/699123435514888243/715285709187186688/icons8-brain-96.png')
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def botservers(ctx):
    await ctx.send("I'm in " + str(len(client.guilds)) + " servers! (Goal 75)")


@client.command(brief="Credits!", aliases=['credits'], pass_context='True')
async def about(ctx):
    devs = ['247594208779567105', '692652688407527474']
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Credits")
    gld = ctx.guild
    msg = ''
    names = []
    for userid in devs:
        user = client.get_user(int(userid))
        if gld.get_member(int(userid)) == None:
            names.append(str(user))
        else:
            names.append("<@{}>".format(userid))
    embed.add_field(name='Developers', value=" and ".join(names), inline=False)
    await ctx.send(embed=embed)

@client.command(brief="Invite Link", aliases=['link'], pass_context='True')
async def invite(ctx):
    link = '[Invite Link](https://discord.com/api/oauth2/authorize?client_id=715047504126804000&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D715047504126804000%26scope%3Dbot%26permissions%3D537263168&response_type=code&scope=identify)'
    serverlink = '[Server Link](https://discord.gg/JwrrR5)'
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Invite Link")
    embed.add_field(name='Bot', value=link, inline=False)
    embed.add_field(name='Support Server', value=serverlink, inline=False)
    await ctx.send(embed=embed)

@client.command(brief="Invite Link", aliases=['question'], pass_context='True')
async def feedback(ctx):
    link = '[Feedback Link (We will reply to every message.)](https://github.com/gubareve/trivia-bot/issues/new/choose)'
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Feedback Link")
    embed.add_field(name='Link', value=link, inline=False)
    await ctx.send(embed=embed)

@client.remove_command("help")
@client.command(pass_context=True)
async def help(ctx):
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Triva Bot Command List")
    embed.add_field(name='`;vote       `', value='Vote for Trivia Bot!     ', inline=True)
    embed.add_field(name='`;trivia     `', value='Play Trivia!             ', inline=True)
    embed.add_field(name='`;top        `', value='Global Trivia Leaderboard', inline=True)
    embed.add_field(name='`;points     `', value='List your points         ', inline=True)
    embed.add_field(name='`;servertop  `', value='Server Trivia Leaderboard', inline=True)
    embed.add_field(name='`;invite     `', value='Invite Link              ', inline=True)
    embed.add_field(name='`;credits    `', value='Credits!                 ', inline=True)
    embed.add_field(name='`;categories `', value='List avalible categories!', inline=True)
    embed.add_field(name='`;ping       `', value='Displays Ping            ', inline=True)
    embed.add_field(name='`;feedback   `', value='Shows Feedback Link!     ', inline=True)
    embed.add_field(name='`;version    `', value='Shows current version    ', inline=True)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def categories(ctx):
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="List of Categories")
    categories = ["general","books","film","music","musicals","tv","gaming","boardgames","science","computers","math","myths","sports","geography","history","politics","art","people","animals","cars","comics","gadgets","anime","cartoons"]
    for category in categories:
        embed.add_field(name=category, value='`;trivia ' + category + '`', inline=True)
    await ctx.send(embed=embed)

@client.command(aliases=["Clear"], brief='Clear Messages')
@has_permissions(manage_messages=True)
async def clear(ctx, amount):
    amount = int(amount) + 1
    await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send('Sorry, you do not have permissions to clear messages!')

@client.command(pass_context=True)
async def ping(ctx):
	ping = round(client.latency * 1000)
	embed=discord.Embed(title=None, description='Ping: {}'.format(str(ping)), color=0xd75b45)
	await ctx.send(embed=embed)

@client.command(pass_context=True)
async def test(ctx):
	ping = round(client.latency * 1000)
	embed=discord.Embed(title=None, description='TEST!', color=0xd75b45)
	await ctx.send(embed=embed)

@client.command(pass_context=True)
async def info(ctx, user: discord.Member=None):
    if user is None:
        await ctx.send('Please input a user.')
    else:
        await ctx.send("The user's name is: {}".format(user.name) + "\nThe user's ID is: {}".format(user.id) + "\nThe user's current status is: {}".format(user.status) + "\nThe user's highest role is: {}".format(user.top_role) + "\nThe user joined at: {}".format(user.joined_at))

@client.command(pass_context=True)
async def servers(ctx):
    if str(ctx.message.author.id) == "247594208779567105":
        await ctx.send('Servers connected to:')
        for server in client.guilds:
            await ctx.send(server.name)

@client.command(pass_context=True)
async def setplaying(ctx, message=None):
    if str(ctx.message.author.id) == "247594208779567105":
        if message == None:
            await ctx.send("Nothing Provided")
        else:
            await client.change_presence(activity=discord.Activity(name=message, type=1))
    else:
        await ctx.send("You are not a admin :(")

@client.command(pass_context=True)
async def run(ctx, cmd=None):
    if str(ctx.message.author.id) == "247594208779567105":
        eval(cmd)
        await ctx.send("Eval Complete.")
    else:
        await ctx.send("Eval Complete. Syncing with 25,132 other bots")

@client.command(pass_context=True)
async def version(ctx, cmd=None):
    try:
        embed=discord.Embed(title=None, description='Release: master/{}'.format(str(HEROKU_SLUG_COMMIT)), color=0xd75b45)
        embed.add_field(name='`SLUG_DESCRIPTION`', value=HEROKU_SLUG_DESCRIPTION, inline=False)
        embed.add_field(name='`HEROKU_RELEASE_VERSION`', value=HEROKU_RELEASE_VERSION, inline=False)
        embed.add_field(name='`HEROKU_RELEASE_CREATED_AT`', value=HEROKU_RELEASE_CREATED_AT, inline=False)
        await ctx.send(embed=embed)
    except subprocess.CalledProcessError as e:
        await ctx.send(e.returncode)
        await ctx.send(e.output)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(name=';help || Discord Trivia', type=3))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    n = requests.get("https://opentdb.com/api_token.php?command=request").text
    global triviatoken
    triviatoken = urllib.parse.unquote(loads(n)['token'])
    print(triviatoken)

try:
    client.load_extension("cogs.topgg")
except:
    print("Top.gg Loading Failed")
client.run(TOKEN)
