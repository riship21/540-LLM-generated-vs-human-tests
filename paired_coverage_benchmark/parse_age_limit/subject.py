import re

US_RATINGS = {
    'TV-Y': 0,
    'TV-Y7': 7,
    'TV-G': 0,
    'TV-PG': 7,
    'TV-14': 14,
    'TV-MA': 18,
    'G': 0,
    'PG': 0,
    'PG-13': 13,
    'R': 16,
    'NC-17': 17,
}

def parse_age_limit(s):
    if s is None:
        return None
    m = re.match(r'^(?P<age>\d{1,2})\+?$', s)
    return int(m.group('age')) if m else US_RATINGS.get(s, None)
