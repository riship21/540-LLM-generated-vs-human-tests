import re

def parse_dfxp_time_expr(time_expr):
    if not time_expr:
        return
    mobj = re.match(r'^(?P<time_offset>\d+(?:\.\d+)?)s?$', time_expr)
    if mobj:
        return float(mobj.group('time_offset'))
