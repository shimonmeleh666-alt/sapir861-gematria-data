import re, unicodedata
def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace('־', ' ')
    return re.sub(r'\s+', ' ', re.sub(r"[^\w\s']", ' ', s.lower())).strip()
