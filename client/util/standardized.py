def str_standard(text:str):
    text = text.strip()
    while text.count('  ') or text.count('\t'):
        text = text.replace('\t', ' ')
        text = text.replace('  ', ' ')
    return text
