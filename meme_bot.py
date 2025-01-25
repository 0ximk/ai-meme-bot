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
def log_environment_vars():
    print(f"API_KEY: {API_KEY}")
    print(f"API_SECRET: {API_SECRET}")
    print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
    print(f"ACCESS_SECRET: {ACCESS_SECRET}")
    print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")

log_environment_vars()

# Проверка наличия всех секретов
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, OPENAI_API_KEY]):
    raise ValueError("Не все секреты установлены. Проверьте переменные окружения.")

# Настройка API-ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Авторизация в Twitter API
try:
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    api.verify_credentials()
    print("Успешная авторизация в Twitter API")
except Exception as e:
    print(f"Ошибка авторизации в Twitter API: {e}")
    raise

# Функция получения трендов из Google Trends
def get_google_trends():
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(["cryptocurrency", "bitcoin", "memecoin"], cat=0, timeframe='now 1-d', geo='US')
        trends = pytrends.related_queries()
        trending_topics = []

        for keyword in ["cryptocurrency", "bitcoin", "memecoin"]:
            if keyword in trends and trends[keyword]["top"] is not None:
                trending_topics.extend(trends[keyword]["top"]["query"].tolist())

        print(f"Полученные тренды: {trending_topics[:5]}")
        return trending_topics[:5]
    except Exception as e:
        print(f"Ошибка получения трендов Google Trends: {e}")
        return []

# Функция получения новостей из CoinGecko
def get_crypto_news():
    try:
        url = "https://api.coingecko.com/api/v3/news"
        response = requests.get(url)
        if response.status_code == 200:
            news = response.json()["data"]
            news_titles = [article["title"] for article in news[:5]]
            print(f"Полученные новости: {news_titles}")
            return news_titles
        else:
            print("Не удалось получить новости с CoinGecko")
            return ["No news available."]
    except Exception as e:
        print(f"Ошибка получения новостей CoinGecko: {e}")
        return ["No news available."]

# Функция генерации мема на основе трендов и новостей
def generate_meme_text(trend, news):
    prompt = f"Создай смешной мем про криптовалюту, тренд {trend}, и новость: {news}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        meme_text = response['choices'][0]['message']['content']
        print(f"Сгенерированный текст мема: {meme_text}")
        return meme_text
    except Exception as e:
        print(f"Ошибка генерации текста мема: {e}")
        return "Не удалось сгенерировать текст мема."

# Функция публикации мема в Twitter
def post_meme():
    print("Начало работы функции post_meme()")
    trends = get_google_trends()
    news = get_crypto_news()

    if trends and news:
        meme_text = generate_meme_text(trends[0], news[0])
        try:
            api.update_status(status=f"{meme_text}\n\n#Crypto #Meme #Trends")
            print("Мем успешно опубликован!")
        except Exception as e:
            print(f"Ошибка публикации мема: {e}")
    else:
        print("Не удалось получить тренды или новости.")

if __name__ == "__main__":
    print("Запуск скрипта meme_bot.py")
    post_meme()
    print("Завершение работы скрипта meme_bot.py")
