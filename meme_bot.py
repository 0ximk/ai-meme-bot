import tweepy
import openai
import os

# Получаем API-ключи из переменных окружения
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Настройка API-ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Авторизация в Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Функция для получения популярных твитов по криптовалютам (на бесплатном тарифе)
def get_popular_tweets():
    query = "crypto OR bitcoin OR ethereum OR memecoin"
    tweets = api.search_tweets(q=query, count=3, result_type="popular", lang="en")
    return [tweet.text for tweet in tweets]

# Функция генерации текста мема с помощью OpenAI
def generate_meme_text(topic):
    prompt = f"Создай смешной твит про {topic} в одном предложении"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Функция публикации текста мема в Twitter
def post_meme():
    tweets = get_popular_tweets()
    if tweets:
        meme_text = generate_meme_text(tweets[0])
        api.update_status(status=f"{meme_text}\n\n#Crypto #Meme")
        print("Text meme successfully posted!")
    else:
        print("No trending tweets found.")

if __name__ == "__main__":
    post_meme()
