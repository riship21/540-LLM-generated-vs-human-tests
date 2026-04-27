def flip_join_inputs(self_is_mi, how):
    flip_order = False
    if self_is_mi:
        flip_order = True
        how = {"right": "left", "left": "right"}.get(how, how)
    return flip_order, how
