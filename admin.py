 # -*- coding: utf8 -*-

 # 
 # This file is part of the Trivia Bot distribution (https://github.com/gubareve/trivia-bot).
 # Copyright (c) 2020 gubareve.
 # 
 # This program is free software: you can redistribute it and/or modify  
 # it under the terms of the GNU General Public License as published by  
 # the Free Software Foundation, version 3.
 #
 # This program is distributed in the hope that it will be useful, but 
 # WITHOUT ANY WARRANTY; without even the implied warranty of 
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 # General Public License for more details.
 #
 # To comply with the credit section of the GNU license, anyone 
 # modifying this file must not remove the credit command.
 #
 # You should have received a copy of the GNU General Public License 
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

from operator import itemgetter
import random
import urllib.parse, urllib.request
from discord.ext import commands
import sys
import redis
import os

TOKEN = os.getenv("bottoken")
if TOKEN == None:
    TOKEN = input("Other Bot Token Please:")

redisurl = os.getenv("REDIS_URL")

if redisurl == None:
    redisurl = input("Please enter the REDIS URL:")

triviadb = redis.from_url(redisurl)

client = commands.Bot(command_prefix="jjsfjdif")


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


def main():
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
        fourthuserid = int(sorteddata[3][0])
    except:
        fourthuserid = "null"
    try:
        fifthuserid = int(sorteddata[4][0])
    except:
        fifthuserid = "null"
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
    try:
        fourthpoints = data[str(fourthuserid)]
    except:
        fourthpoints = "null"
    try:
        fifthpoints = data[str(fifthuserid)]
    except:
        fifthpoints = "null"
    data = str(data)
    user1 = client.get_user(firstuserid)
    user2 = client.get_user(seconduserid)
    user3 = client.get_user(thirduserid)
    user4 = client.get_user(fourthuserid)
    user5 = client.get_user(fifthuserid)
    firstmessage = "{0} with {1} points ({2})".format(
        str(user1), str(firstpoints), str(firstuserid)
    )
    secondmessage = "{0} with {1} points ({2})".format(
        str(user2), str(secondpoints), str(seconduserid)
    )
    thirdmessage = "{0} with {1} points ({2})".format(
        str(user3), str(thirdpoints), str(thirduserid)
    )
    fourthmessage = "{0} with {1} points ({2})".format(
        str(user4), str(fourthpoints), str(fourthuserid)
    )
    fifthmessage = "{0} with {1} points ({2})".format(
        str(user5), str(fifthpoints), str(fifthuserid)
    )
    print(firstmessage)
    print(secondmessage)
    print(thirdmessage)
    print(fourthmessage)
    print(fifthmessage)
    print()
    print("Options:")
    print("(1) Set User Points")
    print("(2) Give User Points")
    print("(3) Get User Points")
    print("(4) Debug")
    print("(5) Exit")
    while True:
        choice = float(input(">>  "))
        if choice == 1:
            userid = str(input("User ID:\n"))
            tbpoints("set", userid, input("Amount:\n"))
            print("Success. The Operation Has Been Completed")
        if choice == 2:
            userid = str(input("User ID:\n"))
            tbpoints("give", userid, input("Amount:\n"))
            print("Success. The Operation Has Been Completed")
        if choice == 3:
            userid = str(input("User ID:\n"))
            print("The User Has " + str(tbpoints("get", userid, 0)) + " Points")
        if choice == 4:
            data = tbpoints("data", 0, 0)
            datalist = data.items()
            print(str(data))
        if choice == 5:
            sys.exit()

        print()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    main()


client.run(TOKEN)
