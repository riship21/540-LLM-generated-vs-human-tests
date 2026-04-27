def is_in_obj(gpr, obj):
    if not hasattr(gpr, "name"):
        return False
    try:
        return gpr is obj[gpr.name]
    except (KeyError, IndexError, TypeError):
        return False
