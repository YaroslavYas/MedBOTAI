from io import BytesIO

import openai
from PIL import Image
from pytesseract import pytesseract

from variables import API_KEY


class OpenAIMessage:
    def __init__(self):
        openai.api_key = API_KEY

    def send_message(self, message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Please, answer only in medical topics."},
                    {"role": "user", "content": message}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(e)
            return 'Something went wrong'


    def send_image(self, file):
        image = Image.open(BytesIO(file.getvalue()))
        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():
            return "Не удалось извлечь текст с изображения."
        try:
            return self.send_message(extracted_text)
            # return f"Текст с изображения: {extracted_text}\n\nОтвет ChatGPT: {extracted_text}"
        except Exception as e:
            return f"Ошибка при обращении к ChatGPT: {str(e)}"
