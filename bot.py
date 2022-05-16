import asyncio
import os

import aioschedule
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from utils.functions import *
from handlers.ap_handlers import *
from handlers.user_handlers import *

bot_key = os.getenv("BOT_TOKEN")
bot = Bot(bot_key)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def scheduler():
    aioschedule.every().minute.do(checkNewQuoteVK)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(*args, **kwargs):
    if args:
        print(*args)
    if kwargs:
        print(**kwargs)
    asyncio.create_task(scheduler())

register_user_handlers(dp, bot)
register_ap_handlers(dp, bot)

executor.start_polling(dispatcher=dp, on_startup=on_startup)
