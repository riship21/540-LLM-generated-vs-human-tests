def handle_no_match(mask, self_obj, inplace=False):
    if not mask.any():
        if inplace:
            return [self_obj]
        return [self_obj.copy()]
    return []
