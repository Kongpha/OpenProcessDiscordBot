import discord
from discord.ext.commands import *

async def anyuser_convert(ctx, obj) :
	passed = 1
	result = None
	if not obj :
		return (ctx.author, 0)
	try :
		while True :
			result = await MemberConverter().convert(ctx, obj)
	except BadArgument :
		# Search begin and end
		if not str(obj).isdigit() :
			n = str(obj)
			for m in ctx.guild.members :
				if m.display_name.startswith(n) or m.name.startswith(n) :
					return (m, passed)
		passed += 1
		try :
			result = await UserConverter().convert(ctx, obj)
		except BadArgument :
			passed += 1
			result = ctx.bot.get_user(obj)
			if result == None :
				passed += 1
				try :
					result = await ctx.bot.fetch_user(obj)
				except discord.NotFound as e :
					return (e, -1)
				except discord.HTTPException as e:
					return (e, -2)
	return (result, passed)

async def anyuser_check(ctx, object) :
	r, passed = await anyuser_convert(ctx,object)
	if passed < 0 :
		err = embed_em(ctx, ctx.bot.stringstack["ObjectNotFoundFromObject"].format(ctx.bot.stringstack["Model"]["User"], str(object)))
		#err.description = "```{}```".format(result.text)
		err.set_footer(text="{} : {} : {}".format(r.status, r.code, passed))
		await ctx.send(embed=err)
		return None
	return r

async def anyuser_safecheck(ctx, object, get_passed=False) :
	r, passed = await anyuser_convert(ctx,object)
	if passed < 0 :
		return ctx.author
		if not get_passed :
			return ctx.author
		else :
			return (0, ctx.author)
	if not get_passed :
		return r
	else :
		return (r, passed)
