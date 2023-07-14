import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(SRC_PATH)

from setup.setup import connect_to_db
from models.google_search_result import GoogleSearchResult
from utils.parser_google import parse_google_search_result_html


def main():
    connect_to_db()
    for record in GoogleSearchResult.objects:
        if record.result_data:
            continue
        
        data = parse_google_search_result_html(record.search_result_html)
        record.result_data = data
        record.save()

if __name__ == '__main__':
    main()