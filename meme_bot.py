import tweepy
import openai
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Twitter API Keys (замени на свои)
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
ACCESS_TOKEN = 'your_access_token'
ACCESS_SECRET = 'your_access_secret'

# OpenAI API Key
OPENAI_API_KEY = 'your_openai_api_key'
openai.api_key = OPENAI_API_KEY

# Twitter API authorization
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Function to get trending topics
def get_trending_topics():
    trends = api.get_place_trends(id=1)
    trending_topics = [trend["name"] for trend in trends[0]["trends"][:5]]
    return trending_topics

# Function to generate meme text using GPT
def generate_meme_text(topic):
    prompt = f"Создай смешной мем про {topic} в двух строчках"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Function to create meme image
def create_meme(text):
    img_url = "https://i.imgflip.com/1bij.jpg"  # Популярный шаблон
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((50, 50), text, font=font, fill="white")
    img.save("meme.jpg")
    return "meme.jpg"

# Function to post meme to Twitter
def post_meme():
    topics = get_trending_topics()
    topic = topics[0] 
    meme_text = generate_meme_text(topic)
    meme_path = create_meme(meme_text)
    api.update_status_with_media(status=f"Вот свежий мем про {topic}!", filename=meme_path)
    print("Мем успешно опубликован!")

if __name__ == "__main__":
    post_meme()
