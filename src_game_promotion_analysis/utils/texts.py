def fix_text(text):
    """修正 LLM 摘要文本"""
    lines = text.split('\n')
    processed_lines = []
    previous_line = ''

    for line in lines:
        _line = line.strip()
        
        # 移除 "```" 行
        if _line == '```':
            continue

        # 去掉 "<" 和 ">"，只保留中间内容
        if _line.startswith('<') and _line.endswith('>'):
            _line = _line[1:-1]

        # 只保留一个空行
        if _line == '' and previous_line == '':
            continue

        processed_lines.append(_line)
        previous_line = _line

    processed_text = '\n'.join(processed_lines)
    return processed_text