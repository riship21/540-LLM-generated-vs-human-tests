import re

compat_str = str
_htmlentity_transform_map = {
    'amp;': '&',
    'lt;': '<',
    'gt;': '>',
    'quot;': '"',
    '#39;': "'",
    '#x22;': '"',
    'nbsp;': '\u00A0',
}

def _htmlentity_transform(entity_name):
    return _htmlentity_transform_map.get(entity_name, '&' + entity_name)

def unescapeHTML(s):
    if s is None:
        return None
    assert type(s) == compat_str
    return re.sub(r'&([^;]+;)', lambda m: _htmlentity_transform(m.group(1)), s)
