import tweepy
import openai
import requests
from pytrends.request import TrendReq
import os
import feedparser

# Получаем API-ключи из переменных окружения
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Logging environment variables to debug
print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")
print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
print(f"ACCESS_SECRET: {ACCESS_SECRET}")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

# Настройка API-ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Авторизация в Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Функция получения трендов из Google Trends
def get_google_trends():
    try:
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
    except Exception as e:
        print(f"Error getting Google Trends: {e}")
        return []

# Функция получения новостей с Google News
def get_google_news():
    try:
        url = "https://news.google.com/rss/search?q=cryptocurrency+OR+bitcoin+OR+memecoin&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        news_titles = [entry.title for entry in feed.entries[:5]]
        return news_titles
    except Exception as e:
        print(f"Error getting Google News: {e}")
        return ["No news available."]

# Функция генерации шутки на основе трендов и новостей
def generate_meme_text(trend, news):
    prompt = f"Создай смешной мем про криптовалюту, включая {trend} и новость: {news}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error generating meme text: {e}")
        return "Failed to generate meme text."

# Функция публикации мема в Twitter
def post_meme():
    trends = get_google_trends()
    news = get_google_news()

    if trends and news:
        meme_text = generate_meme_text(trends[0], news[0])
        try:
            api.update_status(status=f"{meme_text}\n\n#Crypto #Meme #Trends")
            print("Мем успешно опубликован!")
        except Exception as e:
            print(f"Error posting meme: {e}")
    else:
        print("Не удалось получить тренды или новости.")

if __name__ == "__main__":
    post_meme()
