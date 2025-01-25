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

# Логирование значений переменных окружения для отладки
print(f"API_KEY: {API_KEY}")
print(f"API_SECRET: {API_SECRET}")
print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
print(f"ACCESS_SECRET: {ACCESS_SECRET}")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

# Проверка наличия всех секретов
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, OPENAI_API_KEY]):
    print("Не все секреты установлены. Проверьте переменныеThe failing job appears to be due to a potential issue with API окружения.")
    raise authentication or posting to Twitter. Here are steps ValueError("Не все секреты установлены. to diagnose and fix the issue:

1. **Add Authentication Check**: Ensure Twitter authentication is successful before attempting to post.

2. **Add Detailed Logging**: Enhance the logging to capture more details Проверьте переменные окружения.")

# Настройка API-ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Авторизация в Twitter API
try:
    auth = twe during execution.

### Updated `meme_bot.py` with Enhanced Logging and Authentication Check

```epy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api =python
import tweepy
import openai
import requests
from pytrends.request import TrendReq
import os

# Получ tweepy.API(auth, wait_on_rate_limit=True)
    print("Успешная авторизация в Twitter API")
except Exceptionаем API-ключи из переменных окружения
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS as e:
    print(f"Ошибка авторизации в Twitter API: {e}")
    raise

# Функция получения трендов из Google Trends
def get_google_trends():
    try:
_SECRET = os.getenv('ACCESS_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Логирование значений переменных окружения для отладки
print(f"API_KEY:        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(["cryptocurrency", "bitcoin", "memecoin"], cat=0, timeframe='now 1-d', geo='US')
        trends = pytrends.related_queries()
        trending_topics = {API_KEY}")
print(f"API_SECRET: {API_SECRET}")
print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
print(f"ACCESS_SECRET: {ACCESS_SECRET}")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY []

        for keyword in ["cryptocurrency", "bitcoin", "memecoin"]:
            if}")

# Проверка наличия всех секретов
if not all([API_KEY, API_SECRET, ACCESS keyword in trends and trends[keyword]["top"] is not None:
                trending_topics.extend(trends[keyword]["top"]["query"].tolist())

        print(f"_TOKEN, ACCESS_SECRET, OPENAI_API_KEY]):
    raise ValueError("Не все секреты установлены. Проверьте переменные окружения.")

# Настройка API-ключа OpenAI
openai.api_key = OPENAI_API_KEYПолученные тренды: {trending_topics[:5]}")
        return trending_topics[:5]
    except Exception as e:
        print(f"Ошибка получения трендов Google Trends: {e}")
        return []

# Функция получения новостей

# Авторизация в Twitter API
try:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token из CoinGecko
def get_crypto_news():
    try:
       (ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    api.verify_credentials url = "https://api.coingecko.com/api/v3/news"
        response = requests.get(url)
        if response.status_code == 200:
            news = response.json()["data()
    print("Успешная авторизация в Twitter API")
except Exception as e:
    print(f"Ошибка авторизации в Twitter API: {e}")
    raise

# Функция получения трендов из Google Trends
def get_google_trends():
    try:
        pytrends = TrendReq("]
            news_titles = [article["title"] for article in news[:5]]
            print(f"Полученные новости: {news_titles}")
            return news_titles
       hl='en-US', tz=360)
        pytrends.build_payload(["cryptocurrency", "bitcoin", "memecoin"], cat=0, timeframe=' else:
            print("Не удалось получить новости с CoinGecko")
            return ["No news available."]
    except Exception as e:
        print(f"Ошибка получения новостей CoinGecko:now 1-d', geo='US')
        trends = pytrends.related_queries()
        trending_topics = []

        {e}")
        return ["No news available."]

# Функция генерации мема на основе трендов и новостей
def generate_meme_text(trend, news):
    prompt = f for keyword in ["cryptocurrency", "bitcoin", "memecoin"]:
            if keyword in trends and trends[keyword"Создай смешной мем про криптов]["top"] is not None:
                trending_topics.extend(trends[keyword]["top"]["query"].tolist())

        print(f"Полученные тренды: {trendingалюту, тренд {trend}, и новость: {news}"
    try:
_topics[:5]}")
        return trending_topics[:5]
    except Exception as e:
        print(f"Ошибка получения трен        response = openai.ChatCompletion.create(
            model="gpt-4",
           дов Google Trends: {e}")
        return []

# messages=[{"role": "user", "content": prompt}]
        )
        meme_text = response['choices'][0]['message']['content']
        print(f Функция получения новостей из CoinGecko
def get_crypto_news():
    try:
"Сгенерированный текст мема: {meme_text}")
        return meme_text
    except Exception as e:
        print(f        url = "https://api.coingecko.com/api/v3/news"
        response = requests.get(url)
"Ошибка генерации текста мема: {e}")
        return "        if response.status_code == 200:
            news = response.jsonНе удалось сгенерировать текст мема."

# Проверка аутентификации в()["data"]
            news_titles = Twitter
try:
    api.verify_credentials()
    print("Authentication successful!")
except tweepy.TweepError as e:
    print(f"Authentication failed: [article["title"] for article in news[:5]]
            print(f"Полученные новости: {news_titles}")
            return news_titles
        else:
            {e}")

# Функция публикации мема в Twitter
def post_meme():
    trends = get_google_trends()
    news = get_crypto_news()

    if trends and news:
        meme_text print("Не удалось получить новости с CoinGecko")
            return ["No news available."]
    except Exception as e:
        print(f"Ошибка получения новостей CoinGecko: {e}")
        return ["No news available."]

# Функция генерации мема на основе трендов и новостей
def generate_meme_text(trend, news):
    prompt = f"Создай смешной мем про криптовалют = generate_meme_text(trends[0], news[0])
        try:
            api.update_status(status=f"{meme_text}\n\n#Crypto #Meme #Trends")
            print("Мем успешно опубликован!")
        except Exception as eу, тренд {trend}, и новость: {news}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role:
            print(f"Ошибка публикации мема: {e}")
    else:
        print("Не удалось получить тренды или новости.")

if __name__ == "__main__":
    post_meme()
