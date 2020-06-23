# -*- coding: utf8 -*-
import smtplib
import discord
from operator import itemgetter
import requests
import random
import asyncio
import aiohttp
import psutil
import urllib
import random
import sys
import traceback
import urllib.parse, urllib.request, re
from discord import Game
from json import loads
from discord.ext.commands import Bot, has_permissions, MissingPermissions
from discord.ext import commands, tasks
from discord.utils import find
import sys
import time
import redis
import os
import json
import dbl
import logging
import subprocess

userspecific = True
yesemoji = "👍"
noemoji = "👎"
numberemojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
categories = {
    "general": "9",
    "books": "10",
    "film": "11",
    "music": "12",
    "musicals": "13",
    "tv": "14",
    "gaming": "15",
    "boardgames": "16",
    "science": "17",
    "computers": "18",
    "math": "19",
    "myths": "20",
    "sports": "21",
    "geography": "22",
    "history": "23",
    "politics": "24",
    "art": "25",
    "people": "26",
    "animals": "27",
    "cars": "28",
    "comics": "29",
    "gadgets": "30",
    "anime": "31",
    "cartoons": "32",
}
TOKEN = os.getenv("bottoken")
if TOKEN == None:
    TOKEN = input("Token Please:")

redisurl = os.getenv("REDIS_URL")
if redisurl == None:
    redisurl = input("Please enter the REDIS URL:")

dbl_token = os.getenv("DBL_TOKEN")

HEROKU_RELEASE_CREATED_AT = os.getenv("HEROKU_RELEASE_CREATED_AT")
HEROKU_RELEASE_VERSION = os.getenv("HEROKU_RELEASE_VERSION")
HEROKU_SLUG_COMMIT = os.getenv("HEROKU_SLUG_COMMIT")
HEROKU_SLUG_DESCRIPTION = os.getenv("HEROKU_SLUG_DESCRIPTION")

triviadb = redis.from_url(redisurl)

defaultprefix = os.getenv("prefix")

if defaultprefix == None:
    defaultprefix = ";"

async def determineprefix(bot, message):
    guild = message.guild
    if guild:
        return [tbprefix("get", guild.id), bot.user.mention + ' ', '<@!%s> ' % bot.user.id]
    else:
        return [defaultprefix, bot.user.mention + ' ', '<@!%s> ' % bot.user.id]
def check(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel
client = commands.Bot(command_prefix=determineprefix)

def checkvote(userid):
    try:
        headers = {"Authorization": dbl_token}
        voteurl = requests.get(
            "https://top.gg/api/bots/715047504126804000/check?userId=" + str(userid),
            headers=headers,
        ).text
        voted = int(loads(voteurl)["voted"])
    except:
        print(str(loads(voteurl)))
    if voted == 1:
        return True
    else:
        return False


async def get_multi_reaction_answer(msg, author, ctx):
    def checkreaction(reaction, user):
        return (
            (user.id == author.id or not userspecific)
            and reaction.message.id == msg.id
            and str(reaction.emoji) in numberemojis
        )

    for numreact in numberemojis:
        await msg.add_reaction(numreact)
    try:
        reaction, user = await client.wait_for(
            "reaction_add", timeout=20.0, check=checkreaction
        )
    except asyncio.TimeoutError:
        return None
    return numberemojis.index(str(reaction.emoji))


async def get_reaction_answer(msg, author, q, a, ctx):
    def checkreaction(reaction, user):
        return (
            (user.id == author or not userspecific)
            and reaction.message.id == msg.id
            and str(reaction.emoji) in [yesemoji, noemoji]
        )

    await msg.add_reaction(yesemoji)
    await msg.add_reaction(noemoji)
    try:
        reaction, user = await client.wait_for(
            "reaction_add", timeout=20.0, check=checkreaction
        )
    except asyncio.TimeoutError:
        try:
            await msg.clear_reactions()
        except:
            thisisfornothing = 1
        tbpoints("take", author, 1)
        qembed = discord.Embed(
            title="Answered Problem",
            description="This problem has expired",
            color=0xFF0000,
        )
        qembed.add_field(name="The Question Was:", value=str(q), inline=False)
        qembed.add_field(name="The Submitted Answer Was", value="Expired", inline=False)
        qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
        qembed.add_field(
            name="Points",
            value="You lost a point since this question expired! Sorry :(",
            inline=False,
        )
        message = await msg.edit(embed=qembed)
    return [yesemoji, noemoji].index(str(reaction.emoji)) + 1


# returns correct emoji


def tbpoints(statement, key, amount):
    if statement == "get":
        userid = key
        try:
            points = float(triviadb.hgetall("data")[userid.encode("ascii")])
        except:
            points = 0
        return points
    if statement == "give":
        userid = key
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode("ascii")] = float(bytedb[key].decode("ascii"))
        try:
            stringdb[userid] += float(amount)
        except:
            stringdb[userid] = float(amount)
        triviadb.hmset("data", stringdb)
    if statement == "take":
        userid = key
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode("ascii")] = float(bytedb[key].decode("ascii"))
        stringdb[str(userid)] -= float(amount)
        triviadb.hmset("data", stringdb)
    if statement == "set":
        userid = key
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode("ascii")] = float(bytedb[key].decode("ascii"))

        stringdb[userid] = float(amount)
        triviadb.hmset("data", stringdb)
    if statement == "data":
        bytedb = triviadb.hgetall("data")
        stringdb = {}
        for key in bytedb.keys():
            stringdb[key.decode("ascii")] = float(bytedb[key].decode("ascii"))
        return stringdb


def tbperms(statement, user, key):
    if statement == "check":
        try:
            bytedata = triviadb.hgetall(str(user) + "-" + str(key) + "-data")
            data = {}
            for key in bytedata.keys():
                data[key.decode("ascii")] = bytedata[key].decode("ascii")
            if data["1"] == "1":
                return True
            else:
                return False
        except:
            return False
    if statement == "give":
        triviadb.hmset(str(user) + "-" + str(key) + "-data", {1: 1})

def tbprefix(statement, guild, setto=None):
    if statement == "get":
        try:
            bytedata = triviadb.hgetall(str(guild) + "-prefix")
            data = {}
            for key in bytedata.keys():
                data[key.decode("ascii")] = bytedata[key].decode("ascii")
            return data["prefix"]
        except:
            return defaultprefix
    elif statement == "set" and not setto == None:
        triviadb.hmset(str(guild)+ "-prefix", {"prefix":setto})

def tbbroadcast(statement, guild, setto=None):
    if statement == "get":
        try:
            bytedata = triviadb.hgetall(str(guid) + "-broadcast")
            data = {}
            for key in bytedata.keys():
                data[key.decode("ascii")] = bytedata[key].decode("ascii")
            if data["broadcast"] == "1":
                return True
            else:
                return False
        except:
            return False
    elif statement == "set" and not setto == None:
        triviadb.hmset(str(guild) + "-broadcast", {"broadcast":setto})

@client.event
async def on_guild_join(guild):
    r = 215
    g = 91
    b = 69
    general = find(lambda x: x.name == "general", guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        embed = discord.Embed(
            title="Thank you for adding Trivia Bot!",
            description="Please do ;help for info and ;trivia to start playing!",
            color=discord.Colour.from_rgb(r, g, b),
        )
        embed.add_field(
            name = "Opt-in for announcements", value = "If you would like to opt-in for Trivia Bot updates/announcements, please do `;opt` to toggle it on as it is disabled by default. **Note: This is reccomended as Trivia Bot is in Beta and we have a huge update almost every day**"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/699123435514888243/715285709187186688/icons8-brain-96.png"
        )
        await general.send(embed=embed)
    channel = client.get_channel(722605186245197874)
    embed = discord.Embed(
        title="New Server! Name: {} ".format(guild.name),
        description="Now in "
        + str(len(client.guilds))
        + " servers! New server owned by <@{}> with {} members".format(
            guild.owner.id, len(guild.members)
        ),
        color=discord.Colour.from_rgb(r, g, b),
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/699123435514888243/715285709187186688/icons8-brain-96.png"
    )
    await channel.send(embed=embed)

@client.command()
@commands.guild_only()
async def setprefix(ctx, prefix):
    error = False
    try:
        tbprefix("set", ctx.guild.id, prefix)
    except Exception:
        traceback.print_exc()
        error = True
    if not error:
        await ctx.message.add_reaction(yesemoji)
        await ctx.send("Set guild prefix to {}".format(prefix))
    else:
        await ctx.message.add_reaction(noemoji)
        await ctx.send("There was an issue setting your prefix!".format(prefix))

@client.command()
@commands.guild_only()
async def opt(ctx):
    if tbbroadcast("get", ctx.guild.id):
        tbbroadcast("set", ctx.guild.id, "0")
    else:
        tbbroadcast("set", ctx.guild.id, "1")

@client.command()
async def bottedservers(ctx):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        await ctx.send("Servers with only 1 person:")
        for guild in client.guilds:
            if len(guild.members) < 3:
                await ctx.send("{} owned by <@{}>".format(str(guild.name), str(guild.owner.id)))

@client.command()
async def trivia(ctx, category=None):
    if random.randint(1, 3) > 1:
        await multichoice(ctx, category)
    else:
        await truefalse(ctx, category)


@client.command(aliases=["tf"])
async def truefalse(ctx, category=None):
    global triviatoken
    if category == None:
        r = requests.get(
            "https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="
            + str(triviatoken)
        ).text
        lesspoints = False
    else:
        listofdata = {
            "general": "9",
            "books": "10",
            "film": "11",
            "music": "12",
            "musicals": "13",
            "tv": "14",
            "gaming": "15",
            "boardgames": "16",
            "science": "17",
            "computers": "18",
            "math": "19",
            "myths": "20",
            "sports": "21",
            "geography": "22",
            "history": "23",
            "politics": "24",
            "art": "25",
            "people": "26",
            "animals": "27",
            "cars": "28",
            "comics": "29",
            "gadgets": "30",
            "anime": "31",
            "cartoons": "32",
        }
        try:
            categorynumber = listofdata[str(category)]
        except KeyError():
            r = requests.get(
                "https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="
                + str(triviatoken)
            ).text
            lesspoints = False
        else:
            r = requests.get(
                "https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&category="
                + categorynumber
                + "&token="
                + str(triviatoken)
            ).text
            lesspoints = True
    rc = loads(r)["response_code"]
    if rc != 0:
        n = requests.get("https://opentdb.com/api_token.php?command=request").text
        triviatoken = urllib.parse.unquote(loads(n)["token"])
        if category == None:
            r = requests.get(
                "https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="
                + str(triviatoken)
            ).text
            lesspoints = False
        else:
            listofdata = {
                "general": "9",
                "books": "10",
                "film": "11",
                "music": "12",
                "musicals": "13",
                "tv": "14",
                "gaming": "15",
                "boardgames": "16",
                "science": "17",
                "computers": "18",
                "math": "19",
                "myths": "20",
                "sports": "21",
                "geography": "22",
                "history": "23",
                "politics": "24",
                "art": "25",
                "people": "26",
                "animals": "27",
                "cars": "28",
                "comics": "29",
                "gadgets": "30",
                "anime": "31",
                "cartoons": "32",
            }
            try:
                categorynumber = listofdata[str(category)]
            except KeyError():
                r = requests.get(
                    "https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&token="
                    + str(triviatoken)
                ).text
                lesspoints = False
            else:
                r = requests.get(
                    "https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&category="
                    + categorynumber
                    + "&token="
                    + str(triviatoken)
                ).text
                lesspoints = True
    q = urllib.parse.unquote(loads(r)["results"][0]["question"])
    a = urllib.parse.unquote(loads(r)["results"][0]["correct_answer"])
    b = q + a
    qembed = discord.Embed(
        title="YOUR QUESTION",
        description="Use the below reactions to answer this true/false question.",
        color=0xFF0000,
    )
    qembed.add_field(name="Question:", value=str(q), inline=False)
    qembed.add_field(name=yesemoji, value="For true", inline=True)
    qembed.add_field(name=noemoji, value="For false", inline=True)
    try:
        diduservote = checkvote(ctx.message.author.id)
    except:
        diduservote = False
    if not diduservote:
        qembed.add_field(
            name="Notice:",
            value="Want to get 1.5 times the amount of points? Vote for us using ;vote",
            inline=False,
        )
    msg = await ctx.send(embed=qembed)
    answer = await get_reaction_answer(msg, ctx.message.author.id, q, a, ctx)
    uid = ctx.message.author.id
    if answer == 1:
        textanswer = yesemoji
    else:
        textanswer = noemoji
    if diduservote:
        multiplier = 1.5
    else:
        multiplier = 1
    if tbperms("check", ctx.message.author.id, "1.5x"):
        mult2 = 1.5
    else:
        mult2 = 1

    if lesspoints:
        pointstogive = 1 * multiplier * mult2
        message = ""
        if diduservote:
            message = " (Voted)"
    else:
        pointstogive = 1 * multiplier * mult2
        message = ""
        if diduservote:
            message = " (Voted)"

    if a == "True":
        if answer == 1:
            tbpoints("give", str(uid), pointstogive)
            try:
                await msg.clear_reactions()
            except:
                hahalols = 1
            qembed = discord.Embed(
                title="Answered Problem",
                description="This problem has already been answered",
                color=0xFF0000,
            )
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(
                name="The Submitted Answer Was", value=textanswer, inline=False
            )
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(
                name="Points",
                value="You got " + str(pointstogive) + " point(s)! Nice Job!" + message,
                inline=False,
            )
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("✅")
        elif answer == 2:
            tbpoints("give", str(uid), -1)
            try:
                await msg.clear_reactions()
            except:
                chatgoesboom = 12
            qembed = discord.Embed(
                title="Answered Problem",
                description="This problem has already been answered",
                color=0xFF0000,
            )
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(
                name="The Submitted Answer Was", value=textanswer, inline=False
            )
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(
                name="Points", value="You lost 1 point! Sorry :(", inline=False
            )
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("❌")
    elif a == "False":
        if answer == 1:
            tbpoints("give", str(uid), -1)
            try:
                await msg.clear_reactions()
            except:
                waitwhat = 9
            qembed = discord.Embed(
                title="Answered Problem",
                description="This problem has already been answered",
                color=0xFF0000,
            )
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(
                name="The Submitted Answer Was", value=textanswer, inline=False
            )
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(
                name="Points", value="You lost 1 point! Sorry :(", inline=False
            )
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("❌")
        elif answer == 2:
            tbpoints("give", str(uid), pointstogive)
            try:
                await msg.clear_reactions()
            except:
                finaloneyay = 1993
            qembed = discord.Embed(
                title="Answered Problem",
                description="This problem has already been answered",
                color=0xFF0000,
            )
            qembed.add_field(name="The Question Was:", value=str(q), inline=False)
            qembed.add_field(
                name="The Submitted Answer Was", value=textanswer, inline=False
            )
            qembed.add_field(name="The Correct Answer Was  ", value=a, inline=False)
            qembed.add_field(
                name="Points",
                value="You got " + str(pointstogive) + " point(s)! Nice Job!" + message,
                inline=False,
            )
            message = await msg.edit(embed=qembed)
            await msg.add_reaction("✅")


@client.command(aliases=["multi", "multiplechoice", "multiple"])
async def multichoice(ctx, category=None):
    if not category in categories.keys():
        r = requests.get(
            "https://opentdb.com/api.php?amount=1&type=multiple&encode=url3986&token="
            + str(triviatoken)
        ).text
    else:
        r = requests.get(
            "https://opentdb.com/api.php?amount=1&type=multiple&encode=url3986&category="
            + str(categories[category])
            + "&token="
            + str(triviatoken)
        ).text
    r = json.loads(r)
    q = urllib.parse.unquote(r["results"][0]["question"])
    answers = [urllib.parse.unquote(r["results"][0]["correct_answer"])] + [
        urllib.parse.unquote(x) for x in r["results"][0]["incorrect_answers"]
    ]
    random.shuffle(answers)
    correct = answers.index(urllib.parse.unquote(r["results"][0]["correct_answer"]))
    uid = ctx.author.id
    qembed = discord.Embed(
        title="YOUR QUESTION FROM CATEGORY " + category.upper()
        if category in categories.keys()
        else "YOUR QUESTION",
        description="Use the below reactions to answer this multiple choice question:\n"
        + q
        + "\n\n\n"
        + "\n\n".join([numberemojis[qnum] + " " + answers[qnum] for qnum in range(4)]),
        color=0xFF0000,
    )
    msg = await ctx.send(embed=qembed)
    answered = await get_multi_reaction_answer(msg, ctx.author, ctx)
    if answered == None:
        qembed = discord.Embed(
            title="Answered Problem",
            description="This problem has already been answered",
            color=0xFF0000,
        )
        if category in categories.keys():
            qembed.add_field(
                name="The Chosen Category Was:", value=str(category), inline=False
            )
        qembed.add_field(name="The Question Was:", value=str(q), inline=False)
        qembed.add_field(
            name="The Submitted Answer Was:",
            value="EXPIRED (you lost 1 point)",
            inline=False,
        )
        qembed.add_field(
            name="The Correct Answer Was:", value=answers[correct], inline=False
        )
        message = await msg.edit(embed=qembed)
        qembed.add_field(name="Points", value="You lost 1 point!", inline=False)
        tbpoints("give", str(uid), -1)
    else:
        try:
            diduservote = checkvote(ctx.message.author.id)
        except:
            diduservote = False
        pointstogive = 1 if category in categories.keys() else 2
        if diduservote:
            mult = 1.5
        else:
            mult = 1
        if tbperms("check", ctx.message.author.id, "1.5x"):
            mult2 = 1.5
        else:
            mult2 = 1
        pointstogive = pointstogive * mult * mult2
        await msg.clear_reactions()
        if answered == correct:
            await msg.add_reaction("✅")
            tbpoints("give", str(uid), float(pointstogive))
            pointchange = pointstogive
        else:
            await msg.add_reaction("❌")
            tbpoints("give", str(uid), -0.5 if category in categories.keys() else -1.0)
            pointchange = -0.5 if category in categories.keys() else -1.0
        qembed = discord.Embed(
            title="Answered Problem",
            description="This problem has already been answered",
            color=0xFF0000,
        )
        if category in categories.keys():
            qembed.add_field(
                name="The Chosen Category Was:", value=str(category), inline=False
            )
        qembed.add_field(name="The Question Was:", value=str(q), inline=False)
        qembed.add_field(
            name="The Submitted Answer Was:", value=answers[answered], inline=False
        )
        qembed.add_field(
            name="Points",
            value="You {0} {1} point{2}!".format(
                "lost" if pointchange < 0 else "gained",
                str(abs(pointchange)).replace(".0", ""),
                "s" if abs(pointchange) > 1 else "",
            ),
            inline=False,
        )
        qembed.add_field(
            name="The Correct Answer Was:", value=answers[correct], inline=False
        )
        if not diduservote:
            qembed.add_field(
                name="Tip:",
                value="Want to get 1.5 times the amount of points? Vote for us using ;vote",
                inline=False,
            )
        message = await msg.edit(embed=qembed)


@client.command(aliases=["debug"])
async def triviadebug(ctx):
    data = tbpoints("data", 0, 0)
    datalist = data.items()
    await ctx.send(str(data))

@client.command(pass_context=True, aliases=["stats", "botinfo"])
async def botstatus(ctx):

    start = time.perf_counter()
    message = await ctx.send('Pinging...')
    await message.delete()
    end = time.perf_counter()
    duration = (end - start) * 100
    embed=discord.Embed(title=f"**{client.user.name}** Stats ", color=0x2f3136)
    embed.add_field(name="Python", value=(f"{sys.version}"), inline=True)
    embed.add_field(name='Discord.py', value=f"{discord.__version__}", inline=True)
    embed.add_field(name="Bot latency", value=("{} ms (ws: {} ms)".format(round(duration), round(client.latency * 1000))), inline=False)
    embed.add_field(name="Users", value=(f"{len(client.users)}"), inline=True)
    embed.add_field(name="Guilds", value=(f"{len(client.guilds)}"), inline=True)
    embed.add_field(name="Shards", value=(f"{client.shard_count}"), inline=True)
    embed.add_field(name="CPU", value="{}%".format(round(psutil.cpu_percent())), inline=False)
    embed.add_field(name="RAM usage", value="{}% | {} / {}mb".format(round(psutil.virtual_memory().percent), round(psutil.virtual_memory().used/1048576), round(psutil.virtual_memory().total/1048576)), inline=True)


    await ctx.send(embed=embed)

@client.command(aliases=["top"])
async def globalleaderboard(ctx):
    data = tbpoints("data", 0, 0)
    datalist = data.items()
    sorteddata = sorted(datalist, key=itemgetter(1), reverse=True)
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
        title="Leaderboard",
        description="Top Globally",
        color=discord.Colour.from_rgb(r, g, b),
    )
    data = str(data)
    user1 = client.get_user(firstuserid)
    user2 = client.get_user(seconduserid)
    user3 = client.get_user(thirduserid)
    firstmessage = "{0} with {1} points".format(str(user1), str(firstpoints))
    secondmessage = "{0} with {1} points".format(str(user2), str(secondpoints))
    thirdmessage = "{0} with {1} points".format(str(user3), str(thirdpoints))
    embed.add_field(name="1st Place", value=firstmessage, inline=False)
    embed.add_field(name="2nd Place", value=secondmessage, inline=False)
    embed.add_field(name="3rd Place", value=thirdmessage, inline=False)
    await ctx.send(embed=embed)


@client.command(aliases=["servertop"])
async def serverleaderboard(ctx):
    data = tbpoints("data", 0, 0)
    server_members = []
    first_found = False
    second_found = False
    third_found = False
    datalist = data.items()
    sorteddata = sorted(datalist, key=itemgetter(1), reverse=True)
    for id in ctx.guild.members:
        id = id.id
        server_members.append(str(id))
    server_members = sorted(server_members, key=lambda x: data.get(x, 0), reverse=True)
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
        title="Leaderboard",
        description="Top in this Server",
        color=discord.Colour.from_rgb(r, g, b),
    )
    data = str(data)
    firstmessage = "<@" + str(firstuserid) + "> with " + str(firstpoints) + " points!"
    secondmessage = (
        "<@" + str(seconduserid) + "> with " + str(secondpoints) + " points!"
    )
    thirdmessage = "<@" + str(thirduserid) + "> with " + str(thirdpoints) + " points!"
    embed.add_field(name="1st Place", value=firstmessage, inline=False)
    embed.add_field(name="2nd Place", value=secondmessage, inline=False)
    embed.add_field(name="3rd Place", value=thirdmessage, inline=False)
    await ctx.send(embed=embed)


@client.command()
async def points(ctx):
    r = 215
    g = 91
    b = 69
    uid = ctx.message.author.id
    username = "<@" + str(uid) + ">"
    current_points = tbpoints("get", str(uid), 0)
    embed = discord.Embed(
        title="Your Points",
        description="The amount of points you have.",
        color=discord.Colour.from_rgb(r, g, b),
    )
    embed.add_field(name="Username", value=username)
    embed.add_field(name="Points", value=current_points)
    await ctx.send(embed=embed)


@client.command()
async def vote(ctx):
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(
        title="Vote for Trivia Bot",
        description="Voting for Trivia Bot grants you a 1.5x points multiplier for 12 hours! (Please wait 5 minutes after voting)",
        color=discord.Colour.from_rgb(r, g, b),
    )
    embed.add_field(name="top.gg", value="https://top.gg/bot/715047504126804000/vote")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/699123435514888243/715285709187186688/icons8-brain-96.png"
    )
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def botservers(ctx):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        await ctx.send("I'm in " + str(len(client.guilds)) + " servers!")
    else:
        await ctx.send("This command is admin-only")


"NOTCIE: TO COMPLY WITH GPL3, THE CREDITS SECTION MUST NOT BE REMOVED"


@client.command(brief="Credits!", aliases=["credits"], pass_context="True")
async def about(ctx):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Credits")
    gld = ctx.guild
    msg = ""
    names = []
    for userid in devs:
        user = client.get_user(int(userid))
        if gld.get_member(int(userid)) == None:
            names.append(str(user))
        else:
            names.append("<@{}>".format(userid))
    embed.add_field(name="Originally Coded by", value=" , ".join(names), inline=False)
    await ctx.send(embed=embed)


@client.command(brief="Invite Link", aliases=["link"], pass_context="True")
async def invite(ctx):
    link = "[Invite Link](https://discord.com/api/oauth2/authorize?client_id=715047504126804000&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D715047504126804000%26scope%3Dbot%26permissions%3D537263168&response_type=code&scope=identify)"
    serverlink = "[Server Link](https://discord.gg/UHQ33Qe)"
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Invite Link")
    embed.add_field(name="Bot", value=link, inline=False)
    embed.add_field(name="Support Server", value=serverlink, inline=False)
    await ctx.send(embed=embed)


@client.command(brief="Invite Link", aliases=["question"], pass_context="True")
async def feedback(ctx):
    link = "[Feedback Link (We will reply to every message.)](https://github.com/gubareve/trivia-bot/issues/new/choose)"
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Feedback Link")
    embed.add_field(name="Link", value=link, inline=False)
    await ctx.send(embed=embed)


@client.remove_command("help")
@client.command(pass_context=True)
async def help(ctx):
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Trivia Bot Command List")
    embed.add_field(
        name="`;vote       `", value="Vote for Trivia Bot!     ", inline=True
    )
    embed.add_field(
        name="`;trivia     `", value="Play Trivia!             ", inline=True
    )
    embed.add_field(
        name="`;top        `", value="Global Trivia Leaderboard", inline=True
    )
    embed.add_field(
        name="`;points     `", value="List your points         ", inline=True
    )
    embed.add_field(
        name="`;servertop  `", value="Server Trivia Leaderboard", inline=True
    )
    embed.add_field(
        name="`;invite     `", value="Invite Link              ", inline=True
    )
    embed.add_field(
        name="`;credits    `", value="Credits!                 ", inline=True
    )
    embed.add_field(
        name="`;categories `", value="List avalible categories!", inline=True
    )
    embed.add_field(
        name="`;ping       `", value="Displays Ping            ", inline=True
    )
    embed.add_field(
        name="`;feedback   `", value="Shows Feedback Link!     ", inline=True
    )
    embed.add_field(
        name="`;version    `", value="Shows current version    ", inline=True
    )
    embed.add_field(
        name="`;multichoice`", value="Multiple choice question ", inline=True
    )
    embed.add_field(
        name="`;truefalse  `", value="True/False question      ", inline=True
    )
    embed.add_field(
        name="`;shop       `", value="Visit the trivia shop!   ", inline=True
    )
#    embed.add_field(
#        name="`;gamble      `", value="Gamble for more points! ", inline=True
#    )
    embed.add_field(
        name="`;setprefix   `", value="Set the guild prefix    ", inline=True
    )
    embed.set_footer(text="Command invoked by {} || https://triviabot.tech/".format(ctx.message.author.name))
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def shop(ctx):
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="Trivia Bot Points Shop")
    embed.add_field(
        name="`;buy viprole       `",
        value="Buy the vip role in the support sever! (250 points). Must do ;givemevip to activate once purchased.",
        inline=True,
    )
    embed.add_field(
        name="`;buy 1.5x       `",
        value="Buy a 1.5x point multiplier! (2000 points). Stacks multiplicatively with voting",
        inline=True,
    )
    embed.add_field(
        name="`;buy pog       `",
        value="Pog gif (;pog) (25 points)",
        inline=True,
    )
    embed.add_field(
        name="`;buy kappa       `",
        value="Kappa gif (;kappa) for people who don't understand sarcasm (25 points)",
        inline=True,
    )
    embed.add_field(
        name="`;buy lmao       `",
        value="Laugh (;lmao) at people with this gif (25 points)",
        inline=True,
    )
    embed.add_field(
        name="`;buy cmon       `",
        value="That one kid with the bad pun (;cmon) (25 points)",
        inline=True,
    )
    await ctx.send(embed=embed)


@client.command()
async def kappa(ctx):
    if tbperms("check", ctx.message.author.id, "kappa"):
        embed = discord.Embed().set_image(
            url="https://cdn.discordapp.com/attachments/724068633591939143/724086311144783943/kappa.gif"
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("Buy this gif in the shop!")


@client.command()
async def cmon(ctx):
    if tbperms("check", ctx.message.author.id, "cmon"):
        embed = discord.Embed().set_image(
            url="https://cdn.discordapp.com/attachments/724068633591939143/724131734131834930/cmon.gif"
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("Buy this gif in the shop!")


@client.command()
async def pog(ctx):
    if tbperms("check", ctx.message.author.id, "pog"):
        embed = discord.Embed().set_image(
            url="https://cdn.discordapp.com/attachments/724068633591939143/724087526347767918/pog.gif"
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("Buy this gif in the shop!")


@client.command()
async def lmao(ctx):
    if tbperms("check", ctx.message.author.id, "lmao"):
        embed = discord.Embed().set_image(
            url="https://cdn.discordapp.com/attachments/724068633591939143/724087324022931586/lmao.gif"
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("Buy this gif in the shop!")

@client.command(aliases=["gamble"])
async def doubleornothing(ctx, points=None):
#    r = 215
#    g = 91
#    b = 69
#    userpoints = tbpoints("get", str(ctx.message.author.id), 0)
#    if points == None:
#        embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
#        embed.set_author(name="Gambling")
#        embed.add_field(
#            name="Notice",
#            value="`Please specify how many points you would like to gamble`",
#        )
#
#    else:
#        if float(points) <= float(userpoints):
#            if random.randint(1, 10) <= 4:
#                embed = discord.Embed(color=discord.Colour.from_rgb(72, 232, 227))
#                embed.set_image(url="https://cdn.discordapp.com/attachments/716471303682523147/724374290786549840/coinflip.gif")
#                embed.set_author(name="Gambling")
#                embed.add_field(
#                    name="You won!",
#                    value="`You have won {} points! Poggers!`".format(points),
#                    inline=True,
#                )
#                tbpoints("give", str(ctx.message.author.id), points)
#
#            else:
#                embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
#                embed.set_image(url="https://cdn.discordapp.com/attachments/716471303682523147/724374290786549840/coinflip.gif")
#                embed.set_author(name="Gambling")
#                embed.add_field(
#                    name="You lost",
#                    value="`You have lost {} points, F in the chat`".format(points),
#                    inline=True,
#                )
#                tbpoints("take", str(ctx.message.author.id), points)
#        else:
#            embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
#            embed.set_image(url="https://cdn.discordapp.com/attachments/716471303682523147/724374290786549840/coinflip.gif")
#            embed.set_author(name="Gambling")
#            embed.add_field(
#                name="You don't have that much!",
#                value="`You don't have that many points!`".format(points),
#                inline=True,
#            )
    await ctx.send("This command has been disabled. It may be back in the future.")

@client.command(pass_context=True)
async def buy(ctx, product=None):
    r = 215
    g = 91
    b = 69
    if product == None:
        embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
        embed.set_author(name="Store")
        embed.add_field(
            name="Notice",
            value="`You have not specified a item. Please do ;shop for info.`",
            inline=True,
        )
    else:
        products = ["1.5x", "viprole", "pog", "kappa", "lmao", "cmon"]
        prices = {
            "1.5x": 2000,
            "viprole": 250,
            "pog": 25,
            "lmao": 25,
            "cmon": 25,
            "kappa": 25,
        }
        if product in products:
            userpoints = tbpoints("get", str(ctx.message.author.id), 0)
            if userpoints >= prices[product]:
                if not tbperms("check", str(ctx.message.author.id), product):
                    tbperms("give", ctx.message.author.id, product)
                    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
                    embed.set_author(name="Store")
                    embed.add_field(name="Notice", value="`Purchased!`", inline=True)
                    tbpoints("take", str(ctx.message.author.id), prices[product])
                else:
                    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
                    embed.set_author(name="Store")
                    embed.add_field(
                        name="Notice",
                        value="`You have already bought this product!`",
                        inline=True,
                    )
            else:
                embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
                embed.set_author(name="Store")
                embed.add_field(
                    name="Notice",
                    value="`Not enough points. Please do ;shop for info.`",
                    inline=True,
                )
        else:
            embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
            embed.set_author(name="Store")
            embed.add_field(
                name="Notice",
                value="`Incorrect item. Please do ;shop for info.`",
                inline=True,
            )
    await ctx.send(embed=embed)


@client.command(pass_context=True)
async def givemevip(ctx, product=None):
    r = 215
    g = 91
    b = 69
    if tbperms("check", ctx.message.author.id, "viprole"):
        viprole = ctx.guild.get_role(723304450957115495)
        await ctx.message.author.add_roles(viprole)
        embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
        embed.set_author(name="VIP-ROLE")
        embed.add_field(name="Notice", value="`Done, role granted`", inline=True)
    else:
        embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
        embed.set_author(name="VIP-ROLE")
        embed.add_field(
            name="Notice",
            value="`You do not have permission to do this. Buy this command using ;shop`",
            inline=True,
        )
    await ctx.send(embed=embed)


@client.command(pass_context=True, name="categories")
async def _categories(ctx):
    r = 215
    g = 91
    b = 69
    embed = discord.Embed(color=discord.Colour.from_rgb(r, g, b))
    embed.set_author(name="List of Categories")
    for category in categories.keys():
        embed.add_field(name=category, value="`;trivia " + category + "`", inline=True)
    await ctx.send(embed=embed)


@client.command(aliases=["Clear"], brief="Clear Messages")
@has_permissions(manage_messages=True)
async def clear(ctx, amount):
    amount = int(amount) + 1
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("Sorry, you do not have permissions to clear messages!")


@client.command(pass_context=True)
async def ping(ctx):
    ping = round(client.latency * 1000)
    embed = discord.Embed(
        title=None, description="Ping: {}".format(str(ping)), color=0xD75B45
    )
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def website(ctx):
    embed = discord.Embed(
        title=None, description="[TriviaBot](https://triviabot.tech/)", color=0xD75B45
    )
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def info(ctx, user: discord.Member = None):
    if user is None:
        await ctx.send("Please input a user.")
    else:
        await ctx.send(
            "The user's name is: {}".format(user.name)
            + "\nThe user's ID is: {}".format(user.id)
            + "\nThe user's current status is: {}".format(user.status)
            + "\nThe user's highest role is: {}".format(user.top_role)
            + "\nThe user joined at: {}".format(user.joined_at)
        )


@client.command(pass_context=True)
async def servers(ctx):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        await ctx.send("Servers connected to:")
        for server in client.guilds:
            await ctx.send(server.name)

@client.command(pass_context=True)
async def broadcast(ctx, *, message):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        for guild in client.guilds:
            if tbbroadcast("get", str(ctx.guild.id)):
                general = find(lambda x: x.name == "general", guild.text_channels)
                if general and general.permissions_for(guild.me).send_messages:
                    embed = discord.Embed(
                        title='Broadcast',
                        description=str(message),
                        color=0xD75B45,
                    )
                    await general.send(embed=embed)

@client.command()
async def givepoints(ctx, member: discord.Member, points=0):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        tbpoints("give", str(member.id), points)
        await ctx.send("Gave {} points to <@{}>".format(points, str(member.id)))

@client.command()
async def setpoints(ctx, member: discord.Member, points=0):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        tbpoints("set", str(member.id), points)
        await ctx.send("Set {} points as <@{}> 's point value'".format(points, str(member.id)))


@client.command(pass_context=True)
async def setplaying(ctx, message=None):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        if message == None:
            await ctx.send("Nothing Provided")
        else:
            await client.change_presence(
                activity=discord.Activity(name=message, type=1)
            )
    else:
        await ctx.send("You are not a admin :(")


@client.command(pass_context=True)
async def run(ctx, cmd=None):
    devs = ["247594208779567105", "692652688407527474", "677343881351659570"]
    if str(ctx.message.author.id) in devs:
        eval(cmd)
        await ctx.send("Eval Complete.")
    else:
        await ctx.send("Eval Complete. Syncing with 25,132 other bots")


@client.command(pass_context=True)
async def version(ctx, cmd=None):
    try:
        link = "https://github.com/gubareve/trivia-bot/tree/" + str(HEROKU_SLUG_COMMIT)
        link = "[SRC](" + link + ")"
        embed = discord.Embed(
            title=None,
            description="Release: master/{}".format(str(HEROKU_SLUG_COMMIT)),
            color=0xD75B45,
        )
        embed.add_field(name="`SOURCE`", value=link, inline=False)
        embed.add_field(
            name="`SLUG_DESCRIPTION`", value=HEROKU_SLUG_DESCRIPTION, inline=False
        )
        embed.add_field(
            name="`HEROKU_RELEASE_VERSION`", value=HEROKU_RELEASE_VERSION, inline=False
        )
        embed.add_field(
            name="`HEROKU_RELEASE_CREATED_AT`",
            value=HEROKU_RELEASE_CREATED_AT,
            inline=False,
        )
        await ctx.send(embed=embed)
    except subprocess.CalledProcessError as e:
        await ctx.send(e.returncode)
        await ctx.send(e.output)


async def status_task():
    while True:
        await client.change_presence(
            activity=discord.Activity(name="Trivia! | Use ;trivia", type=1)
        )
        await asyncio.sleep(50)
        await client.change_presence(
            activity=discord.Activity(name="Trivia! | Use ;help", type=1)
        )
        await asyncio.sleep(50)


@client.event
async def on_ready():
    # await client.change_presence(activity=discord.Activity(name=';help || Discord Trivia', type=3))
    client.loop.create_task(status_task())
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    n = requests.get("https://opentdb.com/api_token.php?command=request").text
    global triviatoken
    triviatoken = urllib.parse.unquote(loads(n)["token"])
    print("OPENTDB TOKEN --> " + triviatoken)


try:
    client.load_extension("cogs.topgg")
except:
    print("Top.gg Loading Failed")

try:
    client.load_extension("cogs.errors")
except:
    print("Error Cog Loading Failed")
client.run(TOKEN)
