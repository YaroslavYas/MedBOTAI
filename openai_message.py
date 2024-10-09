import openai

from variables import API_KEY


class OpenAIMessage:
    def __init__(self, text):
        self.text = text

    def send_message(self):
        openai.api_key = API_KEY

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Please, answer only in medical topics."},
                    {"role": "user", "content": self.text}
                ]
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            print(e)
            return 'Something went wrong'
