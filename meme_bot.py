import tweepy
import openai
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# Получение API-ключей из переменных окружения
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Установка API-ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Авторизация в Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Функция получения трендов Twitter
def get_trending_topics():
    trends = api.get_place_trends(id=1)  # 1 = глобальные тренды
    trending_topics = [trend["name"] for trend in trends[0]["trends"][:5]]
    return trending_topics

# Функция генерации текста мема с помощью OpenAI GPT
def generate_meme_text(topic):
    prompt = f"Создай смешной мем про {topic} в двух строчках"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Функция создания изображения мема
def create_meme(text):
    img_url = "https://i.imgflip.com/1bij.jpg"  # Популярный шаблон
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((50, 50), text, font=font, fill="white")
    img.save("meme.jpg")
    return "meme.jpg"

# Функция публикации мема в Twitter
def post_meme():
    topics = get_trending_topics()
    topic = topics[0]  # Берем первый тренд
    meme_text = generate_meme_text(topic)
    meme_path = create_meme(meme_text)
    api.update_status_with_media(status=f"Вот свежий мем про {topic}!", filename=meme_path)
    print("Мем успешно опубликован!")

if __name__ == "__main__":
    post_meme()
