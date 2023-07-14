import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from models.google_search_result import GoogleSearchResult
from models.web_page_item import WebPageItem

def create_items_from_result_data(result_data_item):
    print(result_data_item)
    title = result_data_item.get('title')
    url = result_data_item.get('url')
    source = result_data_item.get('source')
    language = result_data_item.get('language')

    # 使用 upsert() 方法创建或更新 WebPageItem
    WebPageItem.objects(url=url).update_one(
        set__title=title,
        set__source=source,
        set__language=language,
        upsert=True
    )

    print(f'create_items_from_result_data: {title}, {url}')

def main():
    connect_to_db()

    for record in GoogleSearchResult.objects:
        result_data = record.result_data
        for item in result_data:
            create_items_from_result_data(item)

if __name__ == '__main__':
    main()