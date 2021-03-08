import os
import asyncio
import aiohttp
import discord
import platform
import discord.ext as ext
import discord.ext.commands as commands

githash = ""

class Pramual(commands.Bot) :
	def __init__(self, *args, **kwargs) :
		# Config
		self.name = "UnnamedBot"
		self.command_prefix = "@@@" # IDK
		self.initial_game = discord.Game("Running !")
		self.initial_status = discord.Status.online
		self.token = os.environ.get("PRAMUAL_TOKEN", None)
		self.custom_cogs = [
			"core" # Essential
		]

		###################################
		self.loop = asyncio.get_event_loop()
		self.session = aiohttp.ClientSession(loop=self.loop)

		super().__init__(**kwargs)

	def start_bot(self) :
		print(">> (!) Starting a bot . . .")
		try :
			if not self.token :
				print(">> {X} Token is invalid")
				return
			super().run(self.token)
		except discord.errors.HTTPException as e :
			print("(X) HTTP ERROR")
			print("	({}) {}".format(e.status, e.text))
			return


	async def close_bot(self) :
		print(">> (!) Shutting a bot down . . .")
		await self.session.close()
		await super().close()

	async def on_ready(self) :
		print(f'>> Login as "{self.user.name}" ({self.user.id})')
		print(f'>> Current Discord.py Version: {discord.__version__}')
		print(f'>> Current Python Version: {platform.python_version()}')

		for c in self.custom_cogs :
			cogn = "cogs." + c
			try :
				self.load_extension(c)
			except commands.errors.ExtensionNotFound as error :
				print(f">> {{X}} Extension \"{c}\" not found")
				continue
			except commands.errors.ExtensionFailed as error :
				# failed.
				print(f">> {{X}} Load Extension \"{c}\" Failed")
				error = getattr(error, 'original', error)
				traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

		# Game
		await self.change_presence(status=self.initial_status, activity=self.initial_game)

# Find Git hash. (optional)
gitf = ".git"
if os.path.isfile(".git") :
	module_folder = open(".git", "r").readline().strip()
	if module_folder.startswith("gitdir: ") :
		gitf = module_folder[8:]

if os.path.isfile(os.path.join(gitf, "HEAD")) :
	head = open(os.path.join(gitf, "HEAD"), "r", encoding="utf-8").readline().strip()
	if head.startswith("ref: ") :
		head = os.path.join(gitf, head[5:])
		if os.path.isfile(head) :
			githash = open(head, "r").readline().strip()
	else:
		githash = head
print(f">>> {githash} <<<")
