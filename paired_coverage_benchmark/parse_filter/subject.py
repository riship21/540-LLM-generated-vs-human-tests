import tokenize

def parse_filter(tokens):
    filter_parts = []
    for type, string, start, _, _ in tokens:
        if type == tokenize.OP and string == ']':
            return ''.join(filter_parts)
        else:
            filter_parts.append(string)
