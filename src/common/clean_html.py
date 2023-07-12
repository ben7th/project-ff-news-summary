from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import BeautifulSoup, NavigableString, Tag
from mongoengine.errors import NotUniqueError

from common.setup_logger import get_logger
logger = get_logger('clean', '../logs/clean-html-errors.log')


def simplify_tags(soup):
    """
    如果一个标签的父标签和该标签一样，那么去掉该标签，但保留其内容

    :param soup: BeautifulSoup 对象
    :return: 简化后的 BeautifulSoup 对象
    """
    if isinstance(soup, NavigableString):
        return
    elif isinstance(soup, Tag):
        for child in soup.contents:
            simplify_tags(child)
            if child.parent.name == child.name:
                child.unwrap()
    return soup


def remove_tags_and_save_to_db(search_result):
    """
    去除 HTML 中的特定标签并保存到数据库

    :param search_result: SearchResult 对象
    """
    content = search_result.content
    if content is None:
        logger.error(f'No content found for {search_result.url}')
        return

    soup = BeautifulSoup(content, 'html.parser')

    try:
        # 移除指定标签
        for tag in ['script', 'noscript', 'meta', 'link', 'style', 'iframe', 'a']:
            [s.extract() for s in soup(tag)]

        # 去掉注释内容
        for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
            comment.extract()

        # 去掉所有标签的属性
        for tag in soup():
            tag.attrs = {}

        # 移除没有文本内容的标签
        for tag in reversed(soup()):
            if not tag.get_text(strip=True):
                tag.extract()

        # 简化嵌套
        soup = simplify_tags(soup)

        # 使用 prettify() 方法格式化 HTML
        # cleaned_html = soup.prettify()

        cleaned_html = "".join(str(soup).split())
        
        # 更新 SearchResult 对象并保存到数据库
        search_result.update(set__cleaned_html=cleaned_html, upsert=True)

    except NotUniqueError as e:
        # 如果出现重复的 URL，记录错误日志
        logger.error(f"Duplicate URL {search_result.url}: {str(e)}")
    except Exception as e:
        # 记录其他错误日志
        logger.error(f"Error while processing HTML: {str(e)}")


def remove_tags_and_save_text_to_db(search_result):
    """
    去除 HTML 中的特定标签并保存到数据库

    :param search_result: SearchResult 对象
    """
    content = search_result.content
    if content is None:
        logger.error(f'No content found for {search_result.url}')
        return

    soup = BeautifulSoup(content, 'html.parser')

    try:
        # 移除指定标签
        for tag in ['script', 'noscript', 'meta', 'link', 'style', 'iframe', 'a']:
            [s.extract() for s in soup(tag)]

        # 去掉注释内容
        for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
            comment.extract()

        # 去掉所有标签的属性
        for tag in soup():
            tag.attrs = {}

        # 移除没有文本内容的标签
        for tag in reversed(soup()):
            if not tag.get_text(strip=True):
                tag.extract()

        # 简化嵌套
        soup = simplify_tags(soup)

        # 使用 prettify() 方法格式化 HTML
        # cleaned_html = soup.prettify()

        cleaned_html = "".join(str(soup).split())
        cleaned_text = soup.get_text(separator='', strip=True)
        
        # 更新 SearchResult 对象并保存到数据库
        search_result.update(set__cleaned_text=cleaned_text, upsert=True)

    except NotUniqueError as e:
        # 如果出现重复的 URL，记录错误日志
        logger.error(f"Duplicate URL {search_result.url}: {str(e)}")
    except Exception as e:
        # 记录其他错误日志
        logger.error(f"Error while processing HTML: {str(e)}")