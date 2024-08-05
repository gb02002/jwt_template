import asyncio
from bs4 import BeautifulSoup
from fastapi import APIRouter
import httpx

PARSING_LINK = 'https://www.farpost.ru/vladivostok/dir?_suggest=hidden&query=s+asdd'
PARSING_LINK = 'https://www.farpost.ru/vladivostok/service/construction/guard/+/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B+%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BD%D0%B0%D0%B1%D0%BB%D1%8E%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F/#center=43.197730597756475%2C131.8686402922909&zoom=11.251855439712799'
# PARSING_LINK = 'https://www.farpost.ru/vladivostok/service/construction/guard/+/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B+%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE%D0%BD%D0%B0%D0%B1%D0%BB%D1%8E%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F/'
# PARSING_LINK = 'https://www.farpost.ru/vladivostok/service/construction/guard/+/Системы+видеонаблюдения/'
PARSING_BASE = 'https://www.farpost.ru'

router = APIRouter(
    prefix='/parsing'
)


@router.get('')
async def start_parsing():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",  # Do Not Track Request Header
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(PARSING_LINK, headers=headers, follow_redirects=True)
        response.raise_for_status()  # Поднимает исключение для неудачного запроса (4xx или 5xx)

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        items = []

        rows = soup.find_all('tr', class_='bull-list-item-js')[:10]
        for row in rows:
            # Извлечение ID
            item_id = row.get('data-doc-id')

            # Извлечение заголовка
            title_tag = row.find('a', class_='bulletinLink')
            title = title_tag.get_text(strip=True) if title_tag else None

            # Извлечение просмотров
            views_tag = row.find('span', class_='views')
            views = views_tag.get_text(strip=True) if views_tag else None

            # Извлечение ссылки для дополнительного запроса
            detail_link = PARSING_BASE + title_tag['href'] if title_tag else None

            if detail_link:
                # Отправить дополнительный запрос для получения информации о пользователе
                detail_response = await client.get(detail_link, headers=headers, follow_redirects=True)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

                user_tag = detail_soup.find('span', class_='userNick auto-shy')
                user_name = user_tag.find('a').get_text(strip=True) if user_tag else None
            else:
                user_name = None

            items.append({
                'id': item_id,
                'title': title,
                'views': views,
                'user_name': user_name
            })

        return items


# async def main():
#     items = await start_parsing()
#     for idx, item in enumerate(items, start=1):
#         print(f"Item {idx}: ID = {item['id']}, Title = {item['title']}, Views = {item['views']}")

# asyncio.run(main())
