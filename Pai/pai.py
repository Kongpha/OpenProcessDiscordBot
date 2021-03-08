import os
import discord
from pramual.pramual import Pramual

class PaiEx(Pramual) :
	def __init__(self, *args, **kwargs) :
		super().__init__(command_prefix="::")
		self.name = "PaiEx"
		self.initial_game = discord.Game("!!!")
		self.initial_status = discord.Status.dnd
		self.token = os.environ.get("PaiExperimental", None)
