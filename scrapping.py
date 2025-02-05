import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'

response = requests.get(URL)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

articles = soup.find_all('article')

for article in articles:
    title_link = article.find('h2').find('a')
    title = title_link.text.strip()
    relative_link = title_link.get('href')
    full_link = f'https://habr.com{relative_link}' if relative_link else ''

    time_tag = article.find('time')
    pub_date = time_tag.get('datetime')[:10] if time_tag else ''

    preview = article.find(class_='tm-article-body tm-article-snippet__lead')
    preview_text = preview.text.strip() if preview else ''

    hubs = article.find_all(class_='tm-article-snippet__hubs-item')
    hubs_text = ' '.join([hub.text.strip() for hub in hubs])

    text_to_check = f'{title} {preview_text} {hubs_text}'.lower()

    if any(keyword in text_to_check for keyword in KEYWORDS):
        print(f'{pub_date} – {title} – {full_link}')