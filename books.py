from googleapiclient.discovery import build

db = []

async def search_books(query, api_key: str =  "AIzaSyBisHmOLjCEjd8vXVjmKdQ0zlolNa6rMtE"):
    service = build('books', 'v1', developerKey=api_key)

    request = service.volumes().list(q=query, maxResults=5)
    response = request.execute()

    result_matrix = []

    if 'items' in response:
        for item in response['items']:
            title = item['volumeInfo'].get('title', 'Без названия')
            authors = item['volumeInfo'].get('authors', ['Автор неизвестен'])
            published_date = item['volumeInfo'].get('publishedDate', 'Дата выхода неизвестна')
            publisher = item['volumeInfo'].get('publisher', 'Неизвестно')
            image_links = item['volumeInfo'].get('imageLinks', {})
            thumbnail = image_links.get('thumbnail', 'https://via.placeholder.com/100')

            data = {"title": title,
                    "authors": authors,
                    "publishedDate": published_date,
                    "publisher": publisher,
                    "thumbnail": thumbnail}
            # Добавляем строку с данными о книге в матрицу
            result_matrix.append(data)

            db.append(data)
    else:
        return None

    return result_matrix

api_key = "AIzaSyBisHmOLjCEjd8vXVjmKdQ0zlolNa6rMtE"
