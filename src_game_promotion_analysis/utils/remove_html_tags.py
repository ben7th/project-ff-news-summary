from bs4 import BeautifulSoup
from bs4 import Comment

def has_text_content(html):
    """
    判断 HTML 中是否存在文字内容。

    :param html: HTML 字符串
    :type html: str
    :return: True，如果存在文字内容；False，如果不存在文字内容
    :rtype: bool
    """
    if not html:
        return False

    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return bool(text.strip())

def get_text_content(html):
    """
    获取 HTML 中文字内容。

    :param html: HTML 字符串
    :type html: str
    :return: 文字内容
    :rtype: str
    """
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    return text.strip()


def remove_html_script_tags(html_text):
    """
    去除 HTML 中的 script 标签
    """

    soup = BeautifulSoup(html_text, 'html.parser')

    # 移除指定标签
    for tag in ['script']:
        [s.extract() for s in soup(tag)]

    cleaned_html = str(soup)
    
    return cleaned_html


def remove_extra_blank_lines(text):
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.strip():  # 判断是否为空行
            cleaned_lines.append(line)
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text
        