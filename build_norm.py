import re, unicodedata
def norm(s):
    s = re.sub(r'([\u3400-\u9fff\uf900-\ufaff])', r' \1 ', s)
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace('־', ' ')
    return re.sub(r'\s+', ' ', re.sub(r"[^\w\s']", ' ', s.lower())).strip()
