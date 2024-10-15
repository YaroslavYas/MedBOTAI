FROM python:3

# Устанавливаем tesseract и необходимые зависимости
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev


WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]
