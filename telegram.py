import asyncio
from aiogram import Bot, Dispatcher
from aiohttp import ClientError

from config import TOKEN, CHAT_ID


class TelegramHandler:

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    async def __aenter__(self):
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.bot.session.close()

    async def send_message(self, message, **kwargs):
        for tries in range(3):
            try:
                await self.bot.send_message(chat_id=self.chat_id, text=message, **kwargs)
                return
            except ClientError as e:
                print(f"Attempt {tries + 1} failed with error: {e}")
                await asyncio.sleep(1)

    async def send_message_up(self, url, down_time):
        message = (f"🟢 Monitor is UP: {url}\n"
                   f"It was down for {down_time}")
        await self.send_message(message)

    async def send_message_down(self, url, status_code, error_message, down_time):
        message = (f"🔴 Monitor is DOWN: {url}\n"
                   f"Status_code: {status_code}\n"
                   f"Error_message: {error_message}\n"
                   f"It was down for {down_time}")
        await self.send_message(message)


async def main():
    async with (TelegramHandler(token=TOKEN, chat_id=CHAT_ID)
                as telegram_handler):
        await telegram_handler.send_message_down(url='kazansky-cirq.ru', status_code=None, error_message=None, down_time=1)
        await telegram_handler.send_message_up(url='kazansky-cirq.ru', down_time=15)


if __name__ == "__main__":
    asyncio.run(main())
