import pymysql
import aiomysql
from time import time
import datetime
from discord import NotFound, Forbidden

async def fetchall(bot, sql, plist = None) :
	try :
		connection = await bot.connect_db()
	except pymysql.err.OperationalError :
		return -1
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, plist)
			s = time()
			used = s - f
			print('[MySQL Query] Query Executed')
			r = await cursor.fetchall()
			await bot.use_query(sql, r, used, cursor.rowcount)
			return {
				"result" : r,
				"time" : used,
				"rows" : cursor.rowcount
			}
	except aiomysql.Error as e:
		print('[MySQL Query] Query Failed to execute')
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')

async def fetchone(bot, sql, plist = None) :
	try :
		connection = await bot.connect_db()
	except pymysql.err.OperationalError :
		return -1
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, plist)
			s = time()
			used = s - f
			print('[MySQL Query] Query Executed')
			r = await cursor.fetchone()
			await bot.use_query(sql, r, used, cursor.rowcount)
			return {
				"result" : r,
				"time" : used,
				"rows" : cursor.rowcount
			}
	except aiomysql.Error as e:
		print('[MySQL Query] Query Failed to execute')
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')

async def commit(bot, sql, plist = None) :
	try :
		connection = await bot.connect_db()
	except pymysql.err.OperationalError :
		return -1
	if not connection :
		return
	try :
		async with connection.cursor() as cursor :
			f = time()
			await cursor.execute(sql, plist)
			s = time()
			used = s - f
		print('[MySQL Query] Query Executed')
		await bot.use_query(sql, {}, used, cursor.rowcount)
		await connection.commit()
		return used
	except aiomysql.Error as e:
		print('[MySQL Query] Query Failed to execute')
		return None
	finally :
		connection.close()
		print('[MySQL Query] Query Connection Closed')








async def qcheck_guild(bot, guild) :
	a = await fetchone(bot, "SELECT EXISTS(SELECT 1 FROM discord_guild WHERE snowflake=%s LIMIT 1) AS ex", guild.id)
	return a["result"]["ex"]

async def qinsert_guild(bot, guild) :
	if not (await qcheck_guild(bot, guild)) :
		return await commit(bot, "INSERT INTO `discord_guild` (`snowflake`, `name`, `added_at`, `updated_at`, `owner_snowflake`, `supported`) VALUES (%s, %s, %s, %s, %s, 0)", (guild.id, guild.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), guild.owner_id))
	else :
		return False

async def qget_guild(bot, guild, ll) :
	if (await qcheck_guild(bot, guild)) :
		return await fetchone(bot, "SELECT {} FROM discord_user WHERE snowflake = %s".format(','.join(ll)))
	else :
		return False

async def qcheck_profile(bot, user) :
	a = await fetchone(bot, "SELECT EXISTS(SELECT 1 FROM discord_user WHERE snowflake=%s LIMIT 1) AS ex", user.id)
	return a["result"]["ex"]

async def qinsert_profile(bot, user) :
	if not (await qcheck_profile(bot, user)) :
		return await commit(bot, "INSERT INTO `discord_user` (`snowflake`, `username`, `added_at`, `credits`, `owner`, `commands`) VALUES (%s, %s, %s, 0, 0, 0)", (user.id, user.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
	else :
		return False

async def qget_profile(bot, user, ll) :
	if (await qcheck_profile(bot, user)) :
		return await fetchone(bot, "SELECT {} FROM discord_user WHERE snowflake = %s".format(",".join(ll)), user.id)
	else :
		return False

async def qupdate_profile(bot, user, dct) :
	if (await qcheck_profile(bot, user)) :
		k = []
		l = []
		for key, value in dct.items() :
			k.append(key)
			l.append(value)
		l.append(guild.id)
		str = ",".join(["{}=%s".format(key) for key in k])
		return await commit(bot, "UPDATE `discord_guild` SET {} WHERE snowflake = %s".format(str), (l))

async def qupdate_guild(bot, guild, dct) :
	if (await qcheck_guild(bot, guild)) :
		k = []
		l = []
		for key, value in dct.items() :
			k.append(key)
			l.append(value)
		l.append(guild.id)
		str = ",".join(["{}=%s".format(key) for key in k])
		return await commit(bot, "UPDATE `discord_guild` SET {} WHERE snowflake = %s".format(str), (l))

async def qupdate_profile_record(bot, user) :
	if (await qcheck_profile(bot, user)) :
		return await qupdate_profile(bot, user, {'username':user.name, 'updated_at':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

async def qupdate_all_profile_record(bot) :
	al = await qget_user_id_list(bot)
	strall = ""
	namelist = []
	for s in al['result'] :
		try :
			us = await bot.fetch_user(s['snowflake'])
		except NotFound :
			strall += "UPDATE `discord_user` SET `missing`=1, `updated_at`=NOW() WHERE snowflake = {};".format(s['snowflake'])
		else :
			strall += "UPDATE `discord_user` SET `username`=%s, `updated_at`=NOW() WHERE snowflake = {};".format(s['snowflake'])
			namelist.append(us.name)
	return await commit(bot, strall, namelist)









async def qupdate_guild_record(bot, guild) :
	if (await qcheck_guild(bot, guild)) :
		return await qupdate_guild(bot, guild, {'name':guild.name, 'owner_snowflake':guild.owner_id})

async def qupdate_all_guild_record(bot) :
	al = await qget_guild_id_list(bot)
	strall = ""
	ad = []
	prm = []
	for s in al['result'] :
		gu = bot.get_guild(s['snowflake'])
		if gu == None :
			strall += "UPDATE `discord_guild` SET `missing`=1, `updated_at`=NOW() WHERE snowflake = {};".format(gu.owner_id, s['snowflake'])
		else :
			strall += "UPDATE `discord_guild` SET `name`=%s, `updated_at`=NOW() WHERE snowflake = {};".format(gu.owner_id, s['snowflake'])
			prm.append(gu.name)
		ad.append(s['snowflake'])
	for gu in bot.guilds :
		if gu.id not in ad :
			strall += "INSERT INTO `discord_guild` (`snowflake`, `name`, `added_at`, `updated_at`, `owner_snowflake`, `supported`) VALUES (%s, %s, %s, %s, %s, 0);"
			prm.extend([gu.id, gu.name, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), gu.owner_id])

	return await commit(bot, strall, prm)

async def qget_user_id_list(bot, addid = False) :
	return await fetchall(bot, "SELECT {}snowflake FROM discord_user".format("id," if addid else ''))
async def qget_guild_id_list(bot, addid = False) :
	return await fetchall(bot, "SELECT {}snowflake FROM discord_guild".format("id," if addid else ''))
