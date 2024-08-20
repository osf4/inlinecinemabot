import asyncio
from datetime import timedelta
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from movies_cacher.default_cacher import DefaultMoviesCacher
from page_requester.default_requester import DefaultPageRequester
from scraper.bendery_scraper import BenderyScraper
from telegram import inline_handlers, handlers

from config import Config

async def main():
    config = Config.load()

    bot = Bot(config.token,
              default = DefaultBotProperties(
                  parse_mode = ParseMode.MARKDOWN
              ))
    
    dp = Dispatcher(storage = MemoryStorage())

    dp.include_routers(
        handlers.router,
        inline_handlers.router,
    ),

    page_requester = DefaultPageRequester()
    scraper = BenderyScraper()
    cacher = DefaultMoviesCacher(period = config.cache_expire_time,
                                 scraper = scraper,
                                 page_requester = page_requester)

    await bot.delete_webhook(drop_pending_updates = True)
    await dp.start_polling(bot, 
                           cacher = cacher)
    
    await page_requester.close()

    
if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())