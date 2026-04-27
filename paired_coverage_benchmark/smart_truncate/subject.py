def smart_truncate(
    string: str,
    max_length: int = 0,
    word_boundary: bool = False,
    separator: str = " ",
    save_order: bool = False,
) -> str:
    string = string.strip(separator)
    if not max_length:
        return string
    if len(string) < max_length:
        return string
    if not word_boundary:
        return string[:max_length].strip(separator)
    if separator not in string:
        return string[:max_length]

    truncated = ''
    for word in string.split(separator):
        if word:
            next_len = len(truncated) + len(word)
            if next_len < max_length:
                truncated += '{}{}'.format(word, separator)
            elif next_len == max_length:
                truncated += '{}'.format(word)
                break
            else:
                if save_order:
                    break
    if not truncated:
        truncated = string[:max_length]
    return truncated.strip(separator)
