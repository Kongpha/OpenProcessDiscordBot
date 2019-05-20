import discord
from discord.ext import commands
import typing
from utils.cog import Cog
from utils.cog import loadInformation
from utils.template import *
from utils.check import *
import json

class Experimental(Cog) :
	pbot = None
	def __init__(self, bot) :
		pbot = bot

		super().__init__(bot)
		self.cog_hidden = True

	@commands.command()
	@IsOwnerBot()
	async def _shutdown(self, ctx) :
		await ctx.send("👋")
		u = ctx.author
		g = ctx.message.guild
		e = discord.Embed(title="Client was shutdowned by {0} ({1}) from guild {2} ({3})".format(u, u.id, g, g.id))
		e.color = 0xDD0000
		await self.bot.log_channel.send(embed=e)
		self.bot.loop.stop()
		await self.bot.close()

	@commands.command()
	@IsOwnerBot()
	async def _send(self, ctx, id, *, text : str) :
		channel = self.bot.get_channel(int(id)) or ctx.message.channel
		await channel.send(text)

	# @commands.command()
	# @IsOwnerBot()
	# async def _send_embed(self, ctx, id, *, embed : str) :
	# 	def _get(object, item) :
	# 		try :
	# 			return y[item]
	# 		except KeyError:
	# 			return ""
	#
	#
	#
	# 	y= json.loads(embed)
	# 	e = discord.Embed()
	# 	e.title = _get(y, "title") or ""
	# 	e.description = _get(y, "description") or ""
	# 	for i in _get(y, "items") :
	# 		e.add_field(name=_get(i, "name"), value=_get(i, "value"), inline=_get(i, ""))
	# 	channel = self.bot.get_channel(int(id)) or ctx.message.channel
	# 	await channel.send(embed=e)

	# @commands.command()
	# @IsOwnerBot()
	# async def _edit(self, ctx, id, *, text : str) :
	# 	channel = self.bot.get_channel(int(id)) or ctx.message.channel
	# 	await channel.send(text)

def setup(bot) :
	bot.add_cog(loadInformation(Experimental(bot)))
