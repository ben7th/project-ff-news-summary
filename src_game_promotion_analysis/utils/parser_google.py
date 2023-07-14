import os
import sys
SRC_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_PATH)

from bs4 import BeautifulSoup
import json

from logger.setup_logger import get_loguru_logger

logger = get_loguru_logger('parser_google', log_file_path='../logs/parser_google.log')

def parse_google_search_result_html(html_text) -> list[dict]:
    """解析谷歌搜索结果网页数据 #main 部分，2023 年 7 月 14 日"""

    soup = BeautifulSoup(html_text, 'html.parser')
    elements = soup.select('#search h3')

    results = []

    for index, _h3_dom in enumerate(elements, start=1):
        try:
            data = {}

            # 序号
            data['index'] = index
            
            # 标题
            title = _h3_dom.text
            data['title'] = title
            
            # 链接地址
            url = _h3_dom.parent.get('href')
            data['url'] = url

            if not url:
                continue # 没有链接地址，则不放入解析结果

            # 来源链接地址和来源标识
            _cite_dom = _h3_dom.next_sibling.select_one('cite')
            source_url = _cite_dom.contents[0]
            data['source_url'] = source_url

            source = None
            _source_dom = _cite_dom.parent.previous_sibling
            if _source_dom:
                source = _source_dom.contents[0].text
            data['source'] = source
            
            # 语言标识
            _g_dom = _h3_dom.parent.parent.parent.parent.parent
            language = _g_dom.get('lang')
            data['language'] = language
            

            # 时间与网页描述
            time = None
            description = None
            _desc_dom = _g_dom.select_one('[data-sncf="1"]')
            if _desc_dom:
                _span_doms = _desc_dom.contents[0].contents
                if len(_span_doms) == 2:
                    time = _span_doms[0].select_one('span').text
                    description = _span_doms[1].text
                else:
                    description = _span_doms[0].text
            
            data['time'] = time
            data['description'] = description
                
            
            # 媒体描述
            media_desc = None
            _jsshadow_dom = _g_dom.select_one('[jsshadow]')
            if _jsshadow_dom:
                media_desc = _jsshadow_dom.contents[1].contents[0].text
        
            data['media_desc'] = media_desc

            results.append(data)
                
        except Exception as e:
            logger.error(f'html 解析错误 {e}')
            logger.error(f'{_h3_dom}')

    return results