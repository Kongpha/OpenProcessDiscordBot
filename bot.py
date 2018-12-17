import discord
import os
import platform
import math
import asyncio
import datetime
from discord.ext import commands

import random

ncfu_c = ["b", "c", "d","f","g","h","l","m","n","p","q","r","s","t","v","w","y","z"]
	
ncfu_C = ["b", "c", "ch", "d", "f", "g", "gh", "j", "k", "l", "llr", "m", "n", "nn", "p", "ph", "phpr", "q", "qu", "r", "rt", "rtm", "s", "sh", "t", "th", "v", "vm", "w", "wh", "y", "z"]

ncfu_v = ["a", "e", "i", "o", "u", "y"]

ncfu_V = ["a", "e", "i", "o", "u", "y", "ae", "ai", "au", "ay", "ea", "ee", "ei", "eu", "ey", "ia", "ie", "oe", "oi", "oo", "ou", "ui"]

ncfu_s = ["b", "d", "f", "g", "h", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "x", "y"]

ncfu_vS = ["ch", "ck", "rd", "ge", "ld", "le", "", "ang", "ar", "ard", "as", "ash", "at", "ath", "augh", "aw", "ban", "bel", "bur", "cer",
		"cha", "che", "dan", "dar", "del", "den", "dra", "dyn", "ech", "eld",
		"elm", "em", "en", "end", "eng", "enth", "er", "ess", "est", "et",
		"gar", "gha", "hat", "hin", "hon", "ia", "ight", "ild", "im", "ina",
		"ine", "ing", "ir", "is", "iss", "it", "kal", "kel", "kim", "kin",
		"ler", "lor", "lye", "mor", "mos", "nal", "ny", "nys", "old", "om",
		"on", "or", "orm", "os", "ough", "per", "pol", "qua", "que", "rad",
		"rak", "ran", "ray", "ril", "ris", "rod", "roth", "ryn", "sam",
		"say", "ser", "shy", "skel", "sul", "tai", "tan", "tas", "ther",
		"tia", "tin", "ton", "tor", "tur", "um", "und", "unt", "urn", "usk",
		"ust", "ver", "ves", "vor", "war", "wor", "yer"]

ncfu_S = ["ch", "ck", "rd", "ge", "ld", "le", "ng", "sh", "th", "gh",
		"ne", "ke", "mp", "ft", "mb", "dt", "ph", "rt", "pt", "mn",
		"nth", "dth", "rth", "mph", "rph", "nph", "st", "sh", "sk",
		"yth", "ythm", "yn", "yh", "lt", "ll", "rn"]

#print "Hello, Dcoder!"
#print S

def ncfu_genMonsGeneral() :
	result = random.choice([random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_C),random.choice(ncfu_C)])+ random.choice([random.choice(ncfu_v),random.choice(ncfu_V)]) + random.choice([random.choice(ncfu_s),random.choice(ncfu_s),random.choice(ncfu_S),random.choice(ncfu_s),"",random.choice(ncfu_vS)]) + random.choice([random.choice([random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_C),random.choice(ncfu_C)])+ random.choice([random.choice(ncfu_v),random.choice(ncfu_V)]) + random.choice([random.choice(ncfu_s),random.choice(ncfu_s),random.choice(ncfu_S),random.choice(ncfu_s),"",random.choice(ncfu_vS),""])]) + random.choice([random.choice([random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_c),random.choice(ncfu_C),random.choice(ncfu_C)])+ random.choice([random.choice(ncfu_v),random.choice(ncfu_V)]) + random.choice([random.choice(ncfu_s),random.choice(ncfu_s),random.choice(ncfu_S),random.choice(ncfu_s),"",random.choice(ncfu_vS),""])]) + random.choice(["proc","ator","","","","","","","","","",""])
	print("Generated : "+result)
	return result;

#print(ncfu_genMonsGeneral())

token = os.environ.get('BOT_TOKEN',None)
openprocch = os.environ.get('OPENPROC_CH',None)

bot = commands.Bot(command_prefix='<<?')
client = discord.Client()
# bot.remove_command("help")

async def status_task():
	await client.wait_until_ready()
	counter = 0
	lastdd = datetime.datetime.now()
	channel = discord.Object(id=openprocch)
	print("Starting Proc Status Task...")
	while not client.is_closed:
		await client.send_message(channel, "***ONE HOUR ONE NAME*** (mons)")
		for i in range(10) :
			await client.send_message(channel,"`" + ncfu_genMonsGeneral() + "`")
		counter += 10
		await client.send_message(channel, counter + " names generated. Since last deploy ("+ lastdd+")")
		print("names" + counter)
		await asyncio.sleep(3600)
	print("!!! WARNING : COUNTER MAYBE RESET")

@bot.event
async def on_ready():
	print('>> OpenProcess by gongpha')
	print('>> login as')
	print(bot.user.name)
	print(bot.user.id)
	print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

	activity = discord.Game(name="Processor")
	await client.change_presence(status=discord.Status.idle, activity=activity)
	
	# await client.change_presence(activity=discord.Activity(name=gameplay))
	client.loop.create_task(status_task())
	
@bot.command()
async def say(ctx):
	await ctx.send("I'm still here")
@bot.command()
async def ncfunamegenmons(ctx):
	await ctx.send(">> `"+ ncfu_genMonsGeneral() + "`")
@bot.command()
async def test(ctx):
	await ctx.send("I'm still here")
@bot.command()
async def add(ctx, a: int, b: int):
	await ctx.send(">> `" + str(a+b) + "`")
@bot.command()
async def sub(ctx, a: int, b: int):
	await ctx.send(">> `" + str(a-b) + "`")
@bot.command()
async def mul(ctx, a: int, b: int):
	await ctx.send(">> `" + str(a*b) + "`")
@bot.command()
async def div(ctx, a: int, b: int):
	await ctx.send(">> `" + str(a/b) + "`")
@bot.command()
async def sqrt(ctx, a: int):
	await ctx.send(">> `" + str(math.sqrt(a)) + "`")
@bot.command()
async def mod(ctx, a: int, b: int):
	await ctx.send(">> `" + str(a%b) + "`")


bot.run(token)