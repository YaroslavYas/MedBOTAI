import asyncio
import logging
import sys

from os import getenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import types, F


from variables import TOKEN
from openai_message import OpenAIMessage

import pytesseract
from PIL import Image
from io import BytesIO

dp = Dispatcher()


# Обработка команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Отправь мне текст или фото, и я помогу тебе.")


# Обработка текстовых сообщений
@dp.message(F.text)
async def text_message_handler(message: Message) -> None:
    response = OpenAIMessage(message.text).send_message()
    await message.answer(response)


# Обработка фотографий
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    # Получаем фото и информацию о файле
    photo = message.photo[-1]  # Берем самое большое разрешение фото
    file_info = await message.bot.get_file(photo.file_id)

    # Скачиваем файл через URL
    file = await message.bot.download_file(file_info.file_path)

    # Конвертируем загруженный файл в изображение
    image = Image.open(BytesIO(file.getvalue()))

    # Извлекаем текст с изображения с помощью pytesseract
    extracted_text = pytesseract.image_to_string(image)

    if not extracted_text.strip():
        await message.answer("Не удалось извлечь текст с изображения.")
        return

    # Отправляем извлеченный текст в ChatGPT для анализа
    try:
        response = OpenAIMessage(extracted_text).send_message()
        await message.answer(f"Текст с изображения: {extracted_text}\n\nОтвет ChatGPT: {response}")
    except Exception as e:
        await message.answer(f"Ошибка при обращении к ChatGPT: {str(e)}")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

