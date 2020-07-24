_AK='3rd Place'
_AJ='2nd Place'
_AI='1st Place'
_AH='Leaderboard'
_AG='Time Took: {} || https://triviabot.tech/'
_AF='Want to get 1.5 times the amount of points? Vote for us using ;vote'
_AE='YOUR QUESTION'
_AD='token'
_AC='https://opentdb.com/api_token.php?command=request'
_AB='Now in '
_AA='reaction_add'
_A9='viprole'
_A8='lmao'
_A7='pog'
_A6='cmon'
_A5='kappa'
_A4='Invite Link'
_A3='correct_answer'
_A2='question'
_A1='take'
_A0='prefix'
_z='10'
_y='cartoons'
_x='anime'
_w='gadgets'
_v='comics'
_u='cars'
_t='animals'
_s='people'
_r='art'
_q='politics'
_p='history'
_o='geography'
_n='sports'
_m='myths'
_l='math'
_k='computers'
_j='science'
_i='boardgames'
_h='gaming'
_g='tv'
_f='musicals'
_e='music'
_d='film'
_c='books'
_b='Buy this gif in the shop!'
_a='<@'
_Z='True'
_Y='1.5x'
_X='set'
_W='general'
_V='https://cdn.discordapp.com/attachments/699123435514888243/715285709187186688/icons8-brain-96.png'
_U='The Correct Answer Was  '
_T='The Submitted Answer Was'
_S=' '
_R='This problem has already been answered'
_Q='results'
_P='Notice'
_O='The Question Was:'
_N='Answered Problem'
_M='get'
_L='Points'
_K='check'
_J='677343881351659570'
_I='692652688407527474'
_H='247594208779567105'
_G='give'
_F='null'
_E='data'
_D='ascii'
_C=None
_B=True
_A=False
import discord,base64
from operator import itemgetter
import requests,random,asyncio,psutil,urllib,datetime,random,sys,traceback,urllib.parse,urllib.request
from json import loads
from discord.ext.commands import has_permissions,MissingPermissions
from discord.ext import commands
from discord.utils import find
import time,redis,os,json,subprocess
from profanityfilter import ProfanityFilter
import homoglyphs as hg
pf=ProfanityFilter()
pf.set_censor('#')
homoglyphs=hg.Homoglyphs(languages={'en'},strategy=hg.STRATEGY_LOAD)
userspecific=_B
yesemoji='👍'
noemoji='👎'
numberemojis=['1️⃣','2️⃣','3️⃣','4️⃣']
categories={_W:'9',_c:_z,_d:'11',_e:'12',_f:'13',_g:'14',_h:'15',_i:'16',_j:'17',_k:'18',_l:'19',_m:'20',_n:'21',_o:'22',_p:'23',_q:'24',_r:'25',_s:'26',_t:'27',_u:'28',_v:'29',_w:'30',_x:'31',_y:'32'}
TOKEN=os.getenv('bottoken')
if TOKEN==_C:TOKEN=input('Token Please:')
redisurl=os.getenv('REDIS_URL')
if redisurl==_C:redisurl=input('Please enter the REDIS URL:')
dbl_token=os.getenv('DBL_TOKEN')
HEROKU_RELEASE_CREATED_AT=os.getenv('HEROKU_RELEASE_CREATED_AT')
HEROKU_RELEASE_VERSION=os.getenv('HEROKU_RELEASE_VERSION')
HEROKU_SLUG_COMMIT=os.getenv('HEROKU_SLUG_COMMIT')
HEROKU_SLUG_DESCRIPTION=os.getenv('HEROKU_SLUG_DESCRIPTION')
triviadb=redis.from_url(redisurl)
defaultprefix=os.getenv(_A0)
if defaultprefix==_C:defaultprefix=';'
def stop_copy(input):
	output=''
	for letter in input:
		if random.randint(1,9)==1:
			if letter==_S:new_letter=_S
			else:new_letters=hg.Homoglyphs().get_combinations(letter);new_letter=random.choice(new_letters)
		else:new_letter=letter
		output+=new_letter
	return output
async def determineprefix(bot,message):
	A='<@!%s> ';guild=message.guild
	if guild:return[tbprefix(_M,guild.id),bot.user.mention+_S,A%bot.user.id]
	else:return[defaultprefix,bot.user.mention+_S,A%bot.user.id]
def check(ctx):return lambda m:m.author==ctx.author and m.channel==ctx.channel
client=commands.Bot(command_prefix=determineprefix)
def checkvote(userid):
	try:headers={'Authorization':dbl_token};voteurl=requests.get('https://top.gg/api/bots/715047504126804000/check?userId='+str(userid),headers=headers).text;voted=int(loads(voteurl)['voted'])
	except:print(str(loads(voteurl)))
	if voted==1:return _B
	else:return _A
async def get_multi_reaction_answer(msg,author,ctx):
	def checkreaction(reaction,user):return(user.id==author.id or not userspecific)and reaction.message.id==msg.id and str(reaction.emoji)in numberemojis
	for numreact in numberemojis:await msg.add_reaction(numreact)
	try:reaction,user=await client.wait_for(_AA,timeout=20.0,check=checkreaction)
	except asyncio.TimeoutError:return _C
	return numberemojis.index(str(reaction.emoji))
async def get_reaction_answer(msg,author,q,a,ctx):
	def checkreaction(reaction,user):return(user.id==author or not userspecific)and reaction.message.id==msg.id and str(reaction.emoji)in[yesemoji,noemoji]
	await msg.add_reaction(yesemoji);await msg.add_reaction(noemoji)
	try:reaction,user=await client.wait_for(_AA,timeout=20.0,check=checkreaction)
	except asyncio.TimeoutError:
		try:await msg.clear_reactions()
		except:thisisfornothing=1
		tbpoints(_A1,author,1);qembed=discord.Embed(title=_N,description='This problem has expired',color=16711680);qembed.add_field(name=_O,value=str(q),inline=_A);qembed.add_field(name=_T,value='Expired',inline=_A);qembed.add_field(name=_U,value=a,inline=_A);qembed.add_field(name=_L,value='You lost a point since this question expired! Sorry :(',inline=_A);message=await msg.edit(embed=qembed)
	return [yesemoji,noemoji].index(str(reaction.emoji))+1
def tbpoints(statement,key,amount):
	if statement==_M:
		userid=key
		try:points=float(triviadb.hgetall(_E)[userid.encode(_D)])
		except:points=0
		return points
	if statement==_G:
		userid=key;bytedb=triviadb.hgetall(_E);stringdb={}
		for key in bytedb.keys():stringdb[key.decode(_D)]=float(bytedb[key].decode(_D))
		try:stringdb[userid]+=float(amount)
		except:stringdb[userid]=float(amount)
		triviadb.hmset(_E,stringdb)
	if statement==_A1:
		userid=key;bytedb=triviadb.hgetall(_E);stringdb={}
		for key in bytedb.keys():stringdb[key.decode(_D)]=float(bytedb[key].decode(_D))
		stringdb[str(userid)]-=float(amount);triviadb.hmset(_E,stringdb)
	if statement==_X:
		userid=key;bytedb=triviadb.hgetall(_E);stringdb={}
		for key in bytedb.keys():stringdb[key.decode(_D)]=float(bytedb[key].decode(_D))
		stringdb[userid]=float(amount);triviadb.hmset(_E,stringdb)
	if statement==_E:
		bytedb=triviadb.hgetall(_E);stringdb={}
		for key in bytedb.keys():stringdb[key.decode(_D)]=float(bytedb[key].decode(_D))
		return stringdb
def tbperms(statement,user,key):
	C='1';B='-data';A='-'
	if statement==_K:
		try:
			bytedata=triviadb.hgetall(str(user)+A+str(key)+B);data={}
			for key in bytedata.keys():data[key.decode(_D)]=bytedata[key].decode(_D)
			if data[C]==C:return _B
			else:return _A
		except:return _A
	if statement==_G:triviadb.hmset(str(user)+A+str(key)+B,{1:1})
def tbprefix(statement,guild,setto=_C):
	A='-prefix'
	if statement==_M:
		try:
			bytedata=triviadb.hgetall(str(guild)+A);data={}
			for key in bytedata.keys():data[key.decode(_D)]=bytedata[key].decode(_D)
			return data[_A0]
		except:return defaultprefix
	elif statement==_X and not setto==_C:triviadb.hmset(str(guild)+A,{_A0:setto})
@client.event
async def on_guild_join(guild):
	r=215;g=91;b=69;general=find(lambda x:x.name==_W,guild.text_channels)
	if general and general.permissions_for(guild.me).send_messages:embed=discord.Embed(title='Thank you for adding Trivia Bot!',description='Please do ;help for info and ;trivia to start playing!',color=discord.Colour.from_rgb(r,g,b));embed.set_thumbnail(url=_V);await general.send(embed=embed)
	channel=client.get_channel(0xa0735969f000032);embed=discord.Embed(title='New Server! Name: {} '.format(guild.name),description=_AB+str(len(client.guilds))+' servers! New server owned by <@{}> with {} members'.format(guild.owner.id,len(guild.members)),color=discord.Colour.from_rgb(r,g,b));embed.set_thumbnail(url=_V);await channel.send(embed=embed)
@client.event
async def on_guild_remove(guild):r=215;g=91;b=69;channel=client.get_channel(0xa0735969f000032);embed=discord.Embed(title='RIP removed from server. Name: {} '.format(guild.name),description=_AB+str(len(client.guilds))+' servers. Server owned by <@{}> with {} members'.format(guild.owner.id,len(guild.members)),color=discord.Colour.from_rgb(r,g,b));embed.set_thumbnail(url=_V);await channel.send(embed=embed)
@client.command()
@commands.guild_only()
async def setprefix(ctx,prefix):
	error=_A
	try:tbprefix(_X,ctx.guild.id,prefix)
	except Exception:traceback.print_exc();error=_B
	if not error:await ctx.message.add_reaction(yesemoji);await ctx.send('Set guild prefix to {}'.format(prefix))
	else:await ctx.message.add_reaction(noemoji);await ctx.send('There was an issue setting your prefix!'.format(prefix))
@client.command()
async def bottedservers(ctx):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:
		await ctx.send('Servers with only 1 person:')
		for guild in client.guilds:
			if len(guild.members)<3:await ctx.send('{} owned by <@{}>'.format(str(guild.name),str(guild.owner.id)))
@client.command()
async def delete(ctx,channel_id,message_id):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:channel=client.get_channel(int(channel_id));msg=await channel.fetch_message(message_id);await msg.delete()
@client.command()
async def trivia(ctx,category=_C):
	if random.randint(1,3)>1:await multichoice(ctx,category)
	else:await truefalse(ctx,category)
@client.command(aliases=['tf'])
async def truefalse(ctx,category=_C):
	E='You lost 1 point! Sorry :(';D=' point(s)! Nice Job!';C='You got ';B=' (Voted)';A='https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986';command_startup=time.perf_counter();global triviatoken
	if category==_C:r=requests.get(A).text;lesspoints=_A
	else:
		listofdata={_W:'9',_c:_z,_d:'11',_e:'12',_f:'13',_g:'14',_h:'15',_i:'16',_j:'17',_k:'18',_l:'19',_m:'20',_n:'21',_o:'22',_p:'23',_q:'24',_r:'25',_s:'26',_t:'27',_u:'28',_v:'29',_w:'30',_x:'31',_y:'32'}
		try:categorynumber=listofdata[str(category)]
		except KeyError():r=requests.get(A).text;lesspoints=_A
		else:r=requests.get('https://opentdb.com/api.php?amount=1&type=boolean&encode=url3986&category='+categorynumber).text;lesspoints=_B
	rc=loads(r)['response_code']
	if rc!=0:
		n=requests.get(_AC).text;triviatoken=urllib.parse.unquote(loads(n)[_AD])
		if category==_C:r=requests.get(A).text;lesspoints=_A
		else:
			listofdata={_W:'9',_c:_z,_d:'11',_e:'12',_f:'13',_g:'14',_h:'15',_i:'16',_j:'17',_k:'18',_l:'19',_m:'20',_n:'21',_o:'22',_p:'23',_q:'24',_r:'25',_s:'26',_t:'27',_u:'28',_v:'29',_w:'30',_x:'31',_y:'32'}
			try:categorynumber=listofdata[str(category)]
			except KeyError():r=requests.get(A).text;lesspoints=_A
			else:r=requests.get(A+categorynumbe).text;lesspoints=_B
	q=urllib.parse.unquote(loads(r)[_Q][0][_A2]);a=urllib.parse.unquote(loads(r)[_Q][0][_A3]);b=q+a
	if tbpoints(_M,str(ctx.message.author.id),0)>5000:q=stop_copy(q)
	qembed=discord.Embed(title=_AE,description='Use the below reactions to answer this true/false question.',color=16711680);qembed.add_field(name='Question:',value=str(q),inline=_A);qembed.add_field(name=yesemoji,value='For true',inline=_B);qembed.add_field(name=noemoji,value='For false',inline=_B)
	try:diduservote=checkvote(ctx.message.author.id)
	except:diduservote=_A
	if not diduservote:qembed.add_field(name='Notice:',value=_AF,inline=_A)
	command_send=time.perf_counter();time_used=str(round(command_send-command_startup,5));qembed.set_footer(text=_AG.format(time_used));msg=await ctx.send(embed=qembed);answer=await get_reaction_answer(msg,ctx.message.author.id,q,a,ctx);uid=ctx.message.author.id
	if answer==1:textanswer=yesemoji
	else:textanswer=noemoji
	if diduservote:multiplier=1.5
	else:multiplier=1
	if tbperms(_K,ctx.message.author.id,_Y):mult2=1.5
	else:mult2=1
	if lesspoints:
		pointstogive=1*multiplier*mult2;message=''
		if diduservote:message=B
	else:
		pointstogive=1*multiplier*mult2;message=''
		if diduservote:message=B
	if a==_Z:
		if answer==1:
			tbpoints(_G,str(uid),pointstogive)
			try:await msg.clear_reactions()
			except:hahalols=1
			qembed=discord.Embed(title=_N,description=_R,color=16711680);qembed.add_field(name=_O,value=str(q),inline=_A);qembed.add_field(name=_T,value=textanswer,inline=_A);qembed.add_field(name=_U,value=a,inline=_A);qembed.add_field(name=_L,value=C+str(pointstogive)+D+message,inline=_A);message=await msg.edit(embed=qembed);await msg.add_reaction('✅')
		elif answer==2:
			tbpoints(_G,str(uid),-1)
			try:await msg.clear_reactions()
			except:chatgoesboom=12
			qembed=discord.Embed(title=_N,description=_R,color=16711680);qembed.add_field(name=_O,value=str(q),inline=_A);qembed.add_field(name=_T,value=textanswer,inline=_A);qembed.add_field(name=_U,value=a,inline=_A);qembed.add_field(name=_L,value=E,inline=_A);message=await msg.edit(embed=qembed);await msg.add_reaction('❌')
	elif a=='False':
		if answer==1:
			tbpoints(_G,str(uid),-1)
			try:await msg.clear_reactions()
			except:waitwhat=9
			qembed=discord.Embed(title=_N,description=_R,color=16711680);qembed.add_field(name=_O,value=str(q),inline=_A);qembed.add_field(name=_T,value=textanswer,inline=_A);qembed.add_field(name=_U,value=a,inline=_A);qembed.add_field(name=_L,value=E,inline=_A);message=await msg.edit(embed=qembed);await msg.add_reaction('❌')
		elif answer==2:
			tbpoints(_G,str(uid),pointstogive)
			try:await msg.clear_reactions()
			except:finaloneyay=1993
			qembed=discord.Embed(title=_N,description=_R,color=16711680);qembed.add_field(name=_O,value=str(q),inline=_A);qembed.add_field(name=_T,value=textanswer,inline=_A);qembed.add_field(name=_U,value=a,inline=_A);qembed.add_field(name=_L,value=C+str(pointstogive)+D+message,inline=_A);message=await msg.edit(embed=qembed);await msg.add_reaction('✅')
@client.command(aliases=['multi','multiplechoice','multiple'])
async def multichoice(ctx,category=_C):
	C='The Correct Answer Was:';B='The Submitted Answer Was:';A='The Chosen Category Was:';command_startup=time.perf_counter()
	if not category in categories.keys():r=requests.get('https://opentdb.com/api.php?amount=1&type=multiple&encode=url3986').text
	else:r=requests.get('https://opentdb.com/api.php?amount=1&type=multiple&encode=url3986&category='+str(categories[category])).text
	r=json.loads(r);q=urllib.parse.unquote(r[_Q][0][_A2])
	if tbpoints(_M,str(ctx.message.author.id),0)>800:q=stop_copy(q)
	answers=[urllib.parse.unquote(r[_Q][0][_A3])]+[urllib.parse.unquote(x)for x in r[_Q][0]['incorrect_answers']];random.shuffle(answers);correct=answers.index(urllib.parse.unquote(r[_Q][0][_A3]));uid=ctx.author.id;qembed=discord.Embed(title='YOUR QUESTION FROM CATEGORY '+category.upper()if category in categories.keys()else _AE,description='Use the below reactions to answer this multiple choice question:\n'+q+'\n\n\n'+'\n\n'.join([numberemojis[qnum]+_S+answers[qnum]for qnum in range(4)]),color=16711680);command_send=time.perf_counter();time_used=str(round(command_send-command_startup,5));qembed.set_footer(text=_AG.format(time_used));msg=await ctx.send(embed=qembed);answered=await get_multi_reaction_answer(msg,ctx.author,ctx)
	if answered==_C:
		qembed=discord.Embed(title=_N,description=_R,color=16711680)
		if category in categories.keys():qembed.add_field(name=A,value=str(category),inline=_A)
		qembed.add_field(name=_O,value=str(q),inline=_A);qembed.add_field(name=B,value='EXPIRED (you lost 1 point)',inline=_A);qembed.add_field(name=C,value=answers[correct],inline=_A);message=await msg.edit(embed=qembed);qembed.add_field(name=_L,value='You lost 1 point!',inline=_A);tbpoints(_G,str(uid),-1)
	else:
		try:diduservote=checkvote(ctx.message.author.id)
		except:diduservote=_A
		pointstogive=1 if category in categories.keys()else 2
		if diduservote:mult=1.5
		else:mult=1
		if tbperms(_K,ctx.message.author.id,_Y):mult2=1.5
		else:mult2=1
		pointstogive=pointstogive*mult*mult2
		try:await msg.clear_reactions()
		except:print('someone didnt give me perms to clear messages. not poggers')
		if answered==correct:await msg.add_reaction('✅');tbpoints(_G,str(uid),float(pointstogive));pointchange=pointstogive
		else:await msg.add_reaction('❌');tbpoints(_G,str(uid),-0.5 if category in categories.keys()else-1.0);pointchange=-0.5 if category in categories.keys()else-1.0
		qembed=discord.Embed(title=_N,description=_R,color=16711680)
		if category in categories.keys():qembed.add_field(name=A,value=str(category),inline=_A)
		qembed.add_field(name=_O,value=str(q),inline=_A);qembed.add_field(name=B,value=answers[answered],inline=_A);qembed.add_field(name=_L,value='You {0} {1} point{2}!'.format('lost'if pointchange<0 else'gained',str(abs(pointchange)).replace('.0',''),'s'if abs(pointchange)>1 else''),inline=_A);qembed.add_field(name=C,value=answers[correct],inline=_A)
		if not diduservote:qembed.add_field(name='Tip:',value=_AF,inline=_A)
		message=await msg.edit(embed=qembed)
@client.command(aliases=['debug'])
async def triviadebug(ctx):data=tbpoints(_E,0,0);datalist=data.items();await ctx.send(str(data))
@client.command(pass_context=_B,aliases=['botstats','botinfo'])
async def botstatus(ctx):start=time.perf_counter();message=await ctx.send('Pinging...');await message.delete();end=time.perf_counter();duration=(end-start)*100;embed=discord.Embed(title=f"**{client.user.name}** Stats ",color=3092790);embed.add_field(name='Python',value=f"{sys.version}",inline=_B);embed.add_field(name='Discord.py',value=f"{discord.__version__}",inline=_B);embed.add_field(name='Bot latency',value='{} ms (ws: {} ms)'.format(round(duration),round(client.latency*1000)),inline=_A);embed.add_field(name='Users',value=f"{len(client.users)}",inline=_B);embed.add_field(name='Guilds',value=f"{len(client.guilds)}",inline=_B);embed.add_field(name='Shards',value=f"{client.shard_count}",inline=_B);embed.add_field(name='CPU',value='{}%'.format(round(psutil.cpu_percent())),inline=_A);embed.add_field(name='RAM usage',value='{}% | {} / {}mb'.format(round(psutil.virtual_memory().percent),round(psutil.virtual_memory().used/1048576),round(psutil.virtual_memory().total/1048576)),inline=_B);await ctx.send(embed=embed)
@client.command(aliases=['top'])
async def globalleaderboard(ctx):
	A='{0} with {1} points';data=tbpoints(_E,0,0);datalist=data.items();sorteddata=sorted(datalist,key=itemgetter(1),reverse=_B);i=0;found=_A
	try:
		while not found:
			if sorteddata[i][0]==str(ctx.message.author.id):position='You are position #'+str(int(i)+1)+'!';found=_B
			else:i+=1
	except:position='You have not played trivia yet :('
	try:firstuserid=int(sorteddata[0][0])
	except:firstuserid=_F
	try:seconduserid=int(sorteddata[1][0])
	except:seconduserid=_F
	try:thirduserid=int(sorteddata[2][0])
	except:thirduserid=_F
	try:firstpoints=data[str(firstuserid)]
	except:firstpoints=_F
	try:secondpoints=data[str(seconduserid)]
	except:secondpoints=_F
	try:thirdpoints=data[str(thirduserid)]
	except:thirdpoints=_F
	r=215;g=91;b=69;embed=discord.Embed(title=_AH,description='Top Globally',color=discord.Colour.from_rgb(r,g,b));data=str(data);user1=pf.censor(str(client.get_user(firstuserid)));user2=pf.censor(str(client.get_user(seconduserid)));user3=pf.censor(str(client.get_user(thirduserid)));firstmessage=A.format(str(user1),str(firstpoints));secondmessage=A.format(str(user2),str(secondpoints));thirdmessage=A.format(str(user3),str(thirdpoints));embed.add_field(name=_AI,value=firstmessage,inline=_A);embed.add_field(name=_AJ,value=secondmessage,inline=_A);embed.add_field(name=_AK,value=thirdmessage,inline=_A);embed.add_field(name='Your Position',value=position,inline=_A);await ctx.send(embed=embed)
@client.command(aliases=['servertop'])
async def serverleaderboard(ctx):
	B=' points!';A='> with ';data=tbpoints(_E,0,0);server_members=[];first_found=_A;second_found=_A;third_found=_A;datalist=data.items();sorteddata=sorted(datalist,key=itemgetter(1),reverse=_B)
	for id in ctx.guild.members:id=id.id;server_members.append(str(id))
	server_members=sorted(server_members,key=lambda x:data.get(x,0),reverse=_B)
	try:firstuserid=server_members[0]
	except:firstuserid=_F
	try:seconduserid=server_members[1]
	except:seconduserid=_F
	try:thirduserid=server_members[2]
	except:thirduserid=_F
	try:firstpoints=data[firstuserid]
	except:firstpoints=_F
	try:secondpoints=data[seconduserid]
	except:secondpoints=_F
	try:thirdpoints=data[thirduserid]
	except:thirdpoints=_F
	r=215;g=91;b=69;embed=discord.Embed(title=_AH,description='Top in this Server',color=discord.Colour.from_rgb(r,g,b));data=str(data);firstmessage=_a+str(firstuserid)+A+str(firstpoints)+B;secondmessage=_a+str(seconduserid)+A+str(secondpoints)+B;thirdmessage=_a+str(thirduserid)+A+str(thirdpoints)+B;embed.add_field(name=_AI,value=firstmessage,inline=_A);embed.add_field(name=_AJ,value=secondmessage,inline=_A);embed.add_field(name=_AK,value=thirdmessage,inline=_A);await ctx.send(embed=embed)
@client.command()
async def points(ctx):r=215;g=91;b=69;uid=ctx.message.author.id;username=_a+str(uid)+'>';current_points=tbpoints(_M,str(uid),0);embed=discord.Embed(title='Your Points',description='The amount of points you have.',color=discord.Colour.from_rgb(r,g,b));embed.add_field(name='Username',value=username);embed.add_field(name=_L,value=current_points);await ctx.send(embed=embed)
@client.command()
async def vote(ctx):r=215;g=91;b=69;embed=discord.Embed(title='Vote for Trivia Bot',description='Voting for Trivia Bot grants you a 1.5x points multiplier for 12 hours! (Please wait 5 minutes after voting)',color=discord.Colour.from_rgb(r,g,b));embed.add_field(name='top.gg',value='https://top.gg/bot/715047504126804000/vote');embed.set_thumbnail(url=_V);await ctx.send(embed=embed)
@client.command()
async def stats(ctx):A='utf-8';r=215;g=91;b=69;data_string=str(ctx.message.author.name)+'#'+str(ctx.message.author.discriminator);data_bytes=data_string.encode(A);encoded=base64.urlsafe_b64encode(data_bytes);encoded=encoded.decode(A);embed=discord.Embed(title='Your stats webpage!',description='[Stats - TriviaBot.tech](https://stats.triviabot.tech/user/'+str(ctx.message.author.id)+'/'+encoded+')',color=discord.Colour.from_rgb(r,g,b));embed.set_thumbnail(url=_V);await ctx.send(embed=embed)
@client.command(pass_context=_B)
async def botservers(ctx):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:await ctx.send("I'm in "+str(len(client.guilds))+' servers!')
	else:await ctx.send('This command is admin-only')
'NOTCIE: TO COMPLY WITH GPL3, THE CREDITS SECTION MUST NOT BE REMOVED'
@client.command(brief='Credits!',aliases=['credits'],pass_context=_Z)
async def about(ctx):
	devs=[_H,_I,_J];r=215;g=91;b=69;embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name='Credits');gld=ctx.guild;msg='';names=[]
	for userid in devs:
		user=client.get_user(int(userid))
		if gld.get_member(int(userid))==_C:names.append(str(user))
		else:names.append('<@{}>'.format(userid))
	embed.add_field(name='Originally Coded by',value=' , '.join(names),inline=_A);await ctx.send(embed=embed)
@client.command(brief=_A4,aliases=['link'],pass_context=_Z)
async def invite(ctx):link='[Invite Link](https://discord.com/api/oauth2/authorize?client_id=715047504126804000&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3D715047504126804000%26scope%3Dbot%26permissions%3D537263168&response_type=code&scope=identify)';serverlink='[Server Link](https://discord.gg/UHQ33Qe)';r=215;g=91;b=69;embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=_A4);embed.add_field(name='Bot',value=link,inline=_A);embed.add_field(name='Support Server',value=serverlink,inline=_A);await ctx.send(embed=embed)
@client.command(brief=_A4,aliases=[_A2],pass_context=_Z)
async def feedback(ctx):link='[Feedback Link (We will reply to every message.)](https://github.com/gubareve/trivia-bot/issues/new/choose)';r=215;g=91;b=69;embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name='Feedback Link');embed.add_field(name='Link',value=link,inline=_A);await ctx.send(embed=embed)
@client.remove_command('help')
@client.command(pass_context=_B)
async def help(ctx):r=215;g=91;b=69;embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name='Trivia Bot Command List');embed.add_field(name='`;vote       `',value='Vote for Trivia Bot!     ',inline=_B);embed.add_field(name='`;trivia     `',value='Play Trivia!             ',inline=_B);embed.add_field(name='`;top        `',value='Global Trivia Leaderboard',inline=_B);embed.add_field(name='`;points     `',value='List your points         ',inline=_B);embed.add_field(name='`;servertop  `',value='Server Trivia Leaderboard',inline=_B);embed.add_field(name='`;invite     `',value='Invite Link              ',inline=_B);embed.add_field(name='`;credits    `',value='Credits!                 ',inline=_B);embed.add_field(name='`;categories `',value='List avalible categories!',inline=_B);embed.add_field(name='`;ping       `',value='Displays Ping            ',inline=_B);embed.add_field(name='`;feedback   `',value='Shows Feedback Link!     ',inline=_B);embed.add_field(name='`;version    `',value='Shows current version    ',inline=_B);embed.add_field(name='`;multichoice`',value='Multiple choice question ',inline=_B);embed.add_field(name='`;truefalse  `',value='True/False question      ',inline=_B);embed.add_field(name='`;shop       `',value='Visit the trivia shop!   ',inline=_B);embed.add_field(name='`;setprefix   `',value='Set the guild prefix    ',inline=_B);embed.set_footer(text='Command invoked by {} || https://triviabot.tech/'.format(ctx.message.author.name));await ctx.send(embed=embed)
@client.command(pass_context=_B)
async def shop(ctx):r=215;g=91;b=69;embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name='Trivia Bot Points Shop');embed.add_field(name='`;buy viprole       `',value='Buy the vip role in the support sever! (250 points). Must do ;givemevip to activate once purchased.',inline=_B);embed.add_field(name='`;buy 1.5x       `',value='Buy a 1.5x point multiplier! (2000 points). Stacks multiplicatively with voting',inline=_B);embed.add_field(name='`;buy pog       `',value='Pog gif (;pog) (25 points)',inline=_B);embed.add_field(name='`;buy kappa       `',value="Kappa gif (;kappa) for people who don't understand sarcasm (25 points)",inline=_B);embed.add_field(name='`;buy lmao       `',value='Laugh (;lmao) at people with this gif (25 points)',inline=_B);embed.add_field(name='`;buy cmon       `',value='That one kid with the bad pun (;cmon) (25 points)',inline=_B);await ctx.send(embed=embed)
@client.command()
async def kappa(ctx):
	if tbperms(_K,ctx.message.author.id,_A5):embed=discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/724068633591939143/724086311144783943/kappa.gif');await ctx.send(embed=embed)
	else:await ctx.send(_b)
@client.command()
async def cmon(ctx):
	if tbperms(_K,ctx.message.author.id,_A6):embed=discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/724068633591939143/724131734131834930/cmon.gif');await ctx.send(embed=embed)
	else:await ctx.send(_b)
@client.command()
async def pog(ctx):
	if tbperms(_K,ctx.message.author.id,_A7):embed=discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/724068633591939143/724087526347767918/pog.gif');await ctx.send(embed=embed)
	else:await ctx.send(_b)
@client.command()
async def lmao(ctx):
	if tbperms(_K,ctx.message.author.id,_A8):embed=discord.Embed().set_image(url='https://cdn.discordapp.com/attachments/724068633591939143/724087324022931586/lmao.gif');await ctx.send(embed=embed)
	else:await ctx.send(_b)
@client.command(aliases=['gamble'])
async def doubleornothing(ctx,points=_C):await ctx.send('This command has been disabled. It may be back in the future.')
@client.command(pass_context=_B)
async def buy(ctx,product=_C):
	A='Store';r=215;g=91;b=69
	if product==_C:embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=A);embed.add_field(name=_P,value='`You have not specified a item. Please do ;shop for info.`',inline=_B)
	else:
		products=[_Y,_A9,_A7,_A5,_A8,_A6];prices={_Y:2000,_A9:250,_A7:25,_A8:25,_A6:25,_A5:25}
		if product in products:
			userpoints=tbpoints(_M,str(ctx.message.author.id),0)
			if userpoints>=prices[product]:
				if not tbperms(_K,str(ctx.message.author.id),product):tbperms(_G,ctx.message.author.id,product);embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=A);embed.add_field(name=_P,value='`Purchased!`',inline=_B);tbpoints(_A1,str(ctx.message.author.id),prices[product])
				else:embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=A);embed.add_field(name=_P,value='`You have already bought this product!`',inline=_B)
			else:embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=A);embed.add_field(name=_P,value='`Not enough points. Please do ;shop for info.`',inline=_B)
		else:embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=A);embed.add_field(name=_P,value='`Incorrect item. Please do ;shop for info.`',inline=_B)
	await ctx.send(embed=embed)
@client.command(pass_context=_B)
async def givemevip(ctx,product=_C):
	A='VIP-ROLE';r=215;g=91;b=69
	if tbperms(_K,ctx.message.author.id,_A9):viprole=ctx.guild.get_role(0xa09b190dfc20067);await ctx.message.author.add_roles(viprole);embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=A);embed.add_field(name=_P,value='`Done, role granted`',inline=_B)
	else:embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name=A);embed.add_field(name=_P,value='`You do not have permission to do this. Buy this command using ;shop`',inline=_B)
	await ctx.send(embed=embed)
@client.command(pass_context=_B,name='categories')
async def _categories(ctx):
	r=215;g=91;b=69;embed=discord.Embed(color=discord.Colour.from_rgb(r,g,b));embed.set_author(name='List of Categories')
	for category in categories.keys():embed.add_field(name=category,value='`;trivia '+category+'`',inline=_B)
	await ctx.send(embed=embed)
@client.command(aliases=['Clear'],brief='Clear Messages')
@has_permissions(manage_messages=_B)
async def clear(ctx,amount):amount=int(amount)+1;await ctx.channel.purge(limit=amount)
@clear.error
async def clear_error(ctx,error):
	if isinstance(error,MissingPermissions):await ctx.send('Sorry, you do not have permissions to clear messages!')
@client.command(pass_context=_B)
async def ping(ctx):ping=round(client.latency*1000);embed=discord.Embed(title=_C,description='Ping: {}'.format(str(ping)),color=14113605);await ctx.send(embed=embed)
@client.command(pass_context=_B)
async def website(ctx):embed=discord.Embed(title=_C,description='[TriviaBot](https://triviabot.tech/)',color=14113605);await ctx.send(embed=embed)
@client.command(pass_context=_B)
async def info(ctx,user=_C):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:
		if user is _C:await ctx.send('Please input a user.')
		else:await ctx.send("The user's name is: {}".format(user.name)+"\nThe user's ID is: {}".format(user.id)+"\nThe user's current status is: {}".format(user.status)+"\nThe user's highest role is: {}".format(user.top_role)+'\nThe user joined at: {}'.format(user.joined_at))
@client.command(pass_context=_B)
async def servers(ctx):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:
		await ctx.send('Servers connected to:')
		for server in client.guilds:await ctx.send(server.name)
@client.command()
async def givepoints(ctx,member,points=0):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:tbpoints(_G,str(member.id),points);await ctx.send('Gave {} points to <@{}>'.format(points,str(member.id)))
@client.command()
async def setpoints(ctx,member,points=0):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:tbpoints(_X,str(member.id),points);await ctx.send("Set {} points as <@{}> 's point value'".format(points,str(member.id)))
@client.command(pass_context=_B)
async def uptime(ctx):
	now=datetime.datetime.utcnow();delta=now-start_time;hours,remainder=divmod(int(delta.total_seconds()),3600);minutes,seconds=divmod(remainder,60);days,hours=divmod(hours,24)
	if days:time_format='**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds.'
	else:time_format='**{h}** hours, **{m}** minutes, and **{s}** seconds.'
	uptime_stamp=time_format.format(d=days,h=hours,m=minutes,s=seconds);await ctx.send('{} has been up for {}'.format(client.user.name,uptime_stamp))
@client.command(pass_context=_B)
async def setplaying(ctx,message=_C):
	devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:
		if message==_C:await ctx.send('Nothing Provided')
		else:await client.change_presence(activity=discord.Activity(name=message,type=1))
	else:await ctx.send('You are not a admin :(')
@client.command(pass_context=_B,aliases=['eval','run'])
async def _eval(ctx,*,code='You need to input code.'):
	G='Error :interrobang: ';F='Input :inbox_tray:';E='Evaluation failed.';D='no ur not getting my db url die';C='no ur not getting my token die';B='```';A='```py\n';devs=[_H,_I,_J]
	if str(ctx.message.author.id)in devs:
		global_vars=globals().copy();global_vars['bot']=client;global_vars['ctx']=ctx;global_vars['message']=ctx.message;global_vars['author']=ctx.message.author;global_vars['channel']=ctx.message.channel;global_vars['server']=ctx.message.guild
		try:
			result=eval(code,global_vars,locals())
			if asyncio.iscoroutine(result):result=await result
			result=str(result);embed=discord.Embed(title='Evaluated successfully.',color=8454016);embed.add_field(name='**Input** :inbox_tray:',value=A+code+B,inline=_A);embed.add_field(name='**Output** :outbox_tray:',value=f"```diff\n+ {result}```".replace(f"{TOKEN}",C).replace(f"{redisurl}",D));await ctx.send(embed=embed)
		except Exception as error:error_value='```diff\n- {}: {}```'.format(type(error).__name__,str(error)).replace(f"{TOKEN}",C).replace(f"{redisurl}",D);embed=discord.Embed(title=E,color=16213599);embed.add_field(name=F,value=A+code+B,inline=_A);embed.add_field(name=G,value=error_value);await ctx.send(embed=embed);return
	else:embed=discord.Embed(title=E,color=16213599);embed.add_field(name=F,value=A+code+B,inline=_A);embed.add_field(name=G,value='```You are not a admin```');await ctx.send(embed=embed)
@client.command(pass_context=_B)
async def version(ctx,cmd=_C):
	try:link='https://github.com/gubareve/trivia-bot/tree/'+str(HEROKU_SLUG_COMMIT);link='[SRC]('+link+')';embed=discord.Embed(title=_C,description='Release: master/{}'.format(str(HEROKU_SLUG_COMMIT)),color=14113605);embed.add_field(name='`SOURCE`',value=link,inline=_A);embed.add_field(name='`SLUG_DESCRIPTION`',value=HEROKU_SLUG_DESCRIPTION,inline=_A);embed.add_field(name='`HEROKU_RELEASE_VERSION`',value=HEROKU_RELEASE_VERSION,inline=_A);embed.add_field(name='`HEROKU_RELEASE_CREATED_AT`',value=HEROKU_RELEASE_CREATED_AT,inline=_A);await ctx.send(embed=embed)
	except subprocess.CalledProcessError as e:await ctx.send(e.returncode);await ctx.send(e.output)
async def status_task():
	while _B:await client.change_presence(activity=discord.Activity(name='Trivia! | Use ;trivia',type=1));await asyncio.sleep(50);await client.change_presence(activity=discord.Activity(name='Trivia! | Use ;help',type=1));await asyncio.sleep(50)
@client.event
async def on_ready():client.loop.create_task(status_task());print('Logged in as');print(client.user.name);print(client.user.id);print('------');n=requests.get(_AC).text;global triviatoken;triviatoken=urllib.parse.unquote(loads(n)[_AD]);print('OPENTDB TOKEN --> '+triviatoken)
try:client.load_extension('cogs.topgg')
except:print('Top.gg Loading Failed')
start_time=datetime.datetime.utcnow()
try:client.load_extension('cogs.errors')
except:print('Error Cog Loading Failed')
