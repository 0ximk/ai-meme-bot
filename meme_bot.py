import requests
import openai
import tweepy
import os

# Получаем API-ключи из переменных окружения
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Настройка API-ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Авторизация в Twitter API (для публикации)
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Функция получения новостей о криптовалютах с CoinGecko API
def get_crypto_news():
    url = "https://api.coingecko.com/api/v3/news"
    response = requests.get(url)
    
    if response.status_code == 200:
        news_data = response.json()
        top_news = [article["title"] for article in news_data["data"][:5]]
        return top_news
    else:
        print("Error fetching news from CoinGecko")
        return ["No news available"]

# Функция генерации текста мема на основе крипто-новостей
def generate_meme_text(news):
    prompt = f"Создай смешной твит на основе новости: '{news}' в одном предложении"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Функция публикации текстового мема в Twitter
def post_meme():
    news_list = get_crypto_news()
    if news_list:
        meme_text = generate_meme_text(news_list[0])
        api.update_status(status=f"{meme_text}\n\n#Crypto #Meme #CoinGecko")
        print("Text meme successfully posted!")
    else:
        print("No crypto news found.")

if __name__ == "__main__":
    post_meme()
