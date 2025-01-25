import tweepy
import openai
import requests
from pytrends.request import TrendReq
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

# Функция получения трендов из Google Trends
def get_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(["cryptocurrency", "bitcoin", "memecoin"], cat=0, timeframe='now 1-d', geo='US')
    trends = pytrends.related_queries()
    trending_topics = []

    for keyword in ["cryptocurrency", "bitcoin", "memecoin"]:
        if keyword in trends:
            queries = trends[keyword]["top"]
            if queries is not None:
                trending_topics.extend(queries["query"].tolist())

    return trending_topics[:5]

# Функция получения криптовалютных новостей с CoinGecko
def get_crypto_news():
    url = "https://api.coingecko.com/api/v3/news"
    response = requests.get(url)
    if response.status_code == 200:
        news = response.json()["data"]
        return [article["title"] for article in news[:5]]
    else:
        return ["No news available."]

# Функция генерации шутки на основе трендов и новостей
def generate_meme_text(trend, news):
    prompt = f"Создай смешной мем про криптовалюту, включая {trend} и новость: {news}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Функция публикации мема в Twitter
def post_meme():
    trends = get_google_trends()
    news = get_crypto_news()

    if trends and news:
        meme_text = generate_meme_text(trends[0], news[0])
        api.update_status(status=f"{meme_text}\n\n#Crypto #Meme #Trends")
        print("Мем успешно опубликован!")
    else:
        print("Не удалось получить тренды или новости.")

if __name__ == "__main__":
    post_meme()
