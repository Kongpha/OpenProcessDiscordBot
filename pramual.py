import asyncio, discord
import platform
import yaml
import sys
import traceback
import random
from discord.ext import commands
#import MySQLdb as mariadb

class NoToken(Exception):
	"""No Token was found or invalid token"""
	pass

class Pramual(commands.Bot) :
	pbot = None
	def __init__(self, *args, **kwargs) :
		command_prefix = kwargs.pop('command_prefix', commands.when_mentioned_or('::'))
		self.bot_name = kwargs.pop('name', "null")
		self.bot_description = kwargs.pop('description', "null")
		self.loop = kwargs.pop('loop', asyncio.get_event_loop())
		self.std = kwargs.pop('std', None)
		self.token = kwargs.pop('token', None)
		self.log_channel_id = kwargs.pop('log_ch', None)
		self.error_channel_id = kwargs.pop('err_ch', None)
		self.timezone = kwargs.pop('timezone', None)
		self.theme = kwargs.pop('theme', [0x9B59B6])
		self.lang = kwargs.pop('lang', None)
		self.cog_list = kwargs.pop('cog_list', None)
		self.owner_list = kwargs.pop('owner', None)
		#self.database_host = kwargs.pop('databaseHost', None)
		#self.database_username = kwargs.pop('databaseUsername', None)
		#self.database_password = kwargs.pop('databasePassword', None)
		#self.database_database = kwargs.pop('databaseDatabase', None)
		with open('i18n/{}.yml'.format(self.lang), encoding="utf8") as json_file :
			self.stringstack = yaml.safe_load(json_file)
		if self.token == None :
			raise NoToken("Invalid Token")
		super().__init__(command_prefix=command_prefix, *args, **kwargs)
		self.remove_command('help')
		pbot = self

	async def on_ready(self) :
		print(f'>> Login As "{self.user.name}" ({self.user.id})')
		print(f'>> Mode   : "{self.std}"')
		print('>> Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))

		self.log_channel = super().get_channel(self.log_channel_id)
		self.error_channel = super().get_channel(self.error_channel_id)

		for c in self.cog_list :
			self.load_extension(c)

		game = discord.Game(name="humans", type=discord.ActivityType.listening)

		self.change_presence(status=discord.Status.online, activity=game)

		#if all([self.database_host, self.database_username, self.database_password, self.database_database]) :
			# try:
			#mariadb_connection = mariadb.connect(host=self.database_host, user=self.database_username, passwd=self.database_password, db=self.database_database)
			# except mariadb.connector.Error as err:
			# 	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			# 		print("Something is wrong with your user name or password")
			# 	elif err.errno == errorcode.ER_BAD_DB_ERROR:
			# 		print("Database does not exist")
			# 	else:
			# 		print(err)
			# else:
			#print("Connected to Database")
			#cursor = mariadb_connection.cursor()


	def run_bot(self) :
		super().run(self.token)

	async def on_command(self, ctx):
		e = discord.Embed(title=f"Command : `{self.command_prefix}{ctx.command.name}`")
		e.description = f"Called to `{self.std}`"
		e.set_author(name='From {0} ({0.id})'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		e.add_field(name='Guild', value='`{0.name}` ({0.id})'.format(ctx.message.guild) if ctx.message.guild else 'Direct Message')
		e.add_field(name='Channel', value='`{0.name}` ({0.id})'.format(ctx.message.channel) if ctx.message.guild else 'DM with `{0.recipient}` ({0.id})'.format(ctx.message.channel))
		e.add_field(name='Message', value="("+str(ctx.message.id) + ")\n```" + ctx.message.clean_content + "```", inline=False)
		e.color = int(random.choice(self.theme))
		e.timestamp = ctx.message.created_at
		await self.log_channel.send(embed=e)

	async def on_command_error(self, ctx, error) :
		e = discord.Embed(title="Command Error : `{}{}`".format(self.command_prefix if ctx.command.name != None else "",ctx.command.name if ctx.command.name != None else "UNKNOWN"))
		e.description = f"Called to `{self.std}`"
		e.set_author(name='From {0} ({0.id})'.format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
		e.add_field(name='Guild', value='`{0.name}` ({0.id})'.format(ctx.message.guild) if ctx.message.guild else 'Direct Message')
		e.add_field(name='Channel', value='`{0.name}` ({0.id})'.format(ctx.message.channel) if ctx.message.guild else 'DM with `{0.recipient}` ({0.id})'.format(ctx.message.channel))
		e.add_field(name='Message', value="("+str(ctx.message.id) + ")\n```" + ctx.message.clean_content + "```", inline=False)
		e.color = 0xff0000
		e.timestamp = ctx.message.created_at

		error = getattr(error, 'original', error)

		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

		tb = error.__traceback__
		f = tb.tb_frame
		lineno = tb.tb_lineno
		filename = f.f_code.co_filename

		e.add_field(name='Expection', value="("+str(ctx.message.id) + ")\n```" + str(getattr(error, 'original', error)) + "```", inline=False)
		e.add_field(name='Filename', value=filename, inline=True)
		e.add_field(name='Line No.', value=lineno, inline=True)
		await self.error_channel.send(embed=e)
	async def on_member_join(self, member) :
		e = discord.Embed(title=self.stringstack["WelcomeUserToGuild"].format(member.mention, member.guild))
		e.description = "*{}*".format(self.stringstack["UserWasJoinedGuildNo"].format(display_name,len(member.guild.members)))
		e.color = 0x00AA80
		e.set_thumbnail(url=member.avatar_url)
		e.set_footer(text=member.id)

		await member.guild.system_channel.send(embed=e)

	async def on_member_remove(self, member) :
		e = discord.Embed(title=self.stringstack["UserWasLeftTheGuild"].format(member.mention, member.guild))
		e.description = "*{}*".format(self.stringstack["NowGuildHadNoMembersLeft"].format(len(member.guild.members)))
		e.color = 0xDD0000
		e.set_thumbnail(url=member.avatar_url)
		e.set_footer(text=member.id)

		await member.guild.system_channel.send(embed=e)
