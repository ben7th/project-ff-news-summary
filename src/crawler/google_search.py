import json
import requests
from serpapi import GoogleSearch

def save_search_results_to_json(keyword, filename, api_key):
    # 使用 SerpApi 搜索前100个结果
    params = {
        "q": keyword,
        "num": 100,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # 从搜索结果中提取 URL 和内容
    data = []
    for result in results['organic_results']:
        url = result['link']
        try:
            content = requests.get(url).content.decode()
        except Exception as e:
            print(f"Error while fetching {url}: {str(e)}")
            content = ''

        data.append({
            'url': url,
            'content': content
        })

    # 保存到本地 JSON 文件
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)