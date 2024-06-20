import requests
from bs4 import BeautifulSoup

def parse_movies(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Поднимает исключение для статусов ошибок
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.find_all('div', class_='movie-title')  # Пример класса, который может быть использован
        return [movie.text.strip() for movie in movies]
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе к {url}: {e}")
        return []

def get_movies_from_genre(genre_url):
    try:
        response = requests.get(genre_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        movies = soup.find_all('div', class_='movie-title', limit=2)  # Пример класса, который может быть использован
        return [movie.text.strip() for movie in movies]
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе к {genre_url}: {e}")
        return []

def get_genre_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        genres = {'Боевики': None, 'Ужасы': None, 'Военные': None}
        genre_movies = {}
        for genre_name in genres.keys():
            genre_link = soup.find('a', text=genre_name)
            if genre_link:
                genres[genre_name] = genre_link.get('href')
                genre_movies[genre_name] = get_movies_from_genre(genres[genre_name])
        return genre_movies
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе к {url}: {e}")
        return {}

# URL веб-сайта, который вы хотите проанализировать
movies_url = 'https://premier.one/collections/top-250-filmov-na-premier'

# Заголовок программы
print("Программа для парсинга списка топ-250 фильмов и жанров с сайта Premier")

# Получение и вывод фильмов по жанрам
genre_movies = get_genre_links(movies_url)
if genre_movies:
    print("\nФильмы по жанрам:")
    for genre, movies in genre_movies.items():
        print(f"{genre}:")
        for movie in movies:
            print(movie)
else:
    print("Не удалось извлечь фильмы по жанрам.")
