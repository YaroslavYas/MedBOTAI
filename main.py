import asyncio
import logging
import sys
from os import getenv
import openai
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from variables import TOKEN, API_KEY

dp = Dispatcher()


@dp.message()
async def command_start_handler(message: Message) -> None:
    openai.api_key = API_KEY

    def ask_medical_bot(user_input):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain the process of photosynthesis."}
            ]
        )

        print(response['choices'][0]['message']['content'])
        return response['choices'][0]['message']['content']

    answer = ask_medical_bot(message.answer)
    await message.answer(answer)
    print(answer)



async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

