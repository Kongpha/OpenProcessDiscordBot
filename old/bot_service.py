import asyncio

from pramual import Pramual

loop = asyncio.get_event_loop()

bot_th = Pramual(command_prefix='::', std='PramualTH', loop=loop, timezone="Asia/Bangkok", log_ch=530055377249894421, err_ch=568682030817345556)
bot_en = Pramual(command_prefix="''", std='PramualEN', loop=loop, timezone=None, log_ch=530055377249894421, err_ch=568682030817345556)

print("Starting a Task...")
loop.create_task(bot_th.run_bot())
loop.create_task(bot_en.run_bot())
loop.run_until_complete(task)
loop.run_forever()