def update_or_append_format(formats, formats_dict, representation_id, f):
    try:
        existing_format = next(
            fo for fo in formats
            if fo['format_id'] == representation_id
        )
    except StopIteration:
        full_info = formats_dict.get(representation_id, {}).copy()
        full_info.update(f)
        formats.append(full_info)
    else:
        existing_format.update(f)
    return formats
