
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

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7867027173:AAFY0VT0udiGKoXookbSkkiHqZvl4_Xj5QM'

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message()
async def command_start_handler(message: Message) -> None:
    openai.api_key = "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"

    def ask_medical_bot(user_input):
        # Используем правильный эндпоинт для чат-модели
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Или gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Explain the process of photosynthesis."}
            ]
        )

        # Вывод ответа
        print(response['choices'][0]['message']['content'])
        return response['choices'][0]['message']['content']

    # Пример запроса
    answer = ask_medical_bot(message.answer)
    await message.answer(answer)
    print(answer)


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     """
#     Handler will forward receive a message back to the sender
#
#     By default, message handler will handle all message types (like a text, photo, sticker etc.)
#     """
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

