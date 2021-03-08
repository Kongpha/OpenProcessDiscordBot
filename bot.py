import asyncio
from Pai.pai import PaiEx

bot = PaiEx()
loop = asyncio.get_event_loop()

print("Starting a Task...")
try :

	bot.start_bot()
	#main_task = loop.create_task(bot.start_bot())
	#loop.run_until_complete(main_task)
#except (KeyboardInterrupt, RuntimeError) :
#	print("<X> KeyboardInterrupt or RuntimeError !")
finally :
	print("(!) Closing a loop . . .")
	#loop.close()
