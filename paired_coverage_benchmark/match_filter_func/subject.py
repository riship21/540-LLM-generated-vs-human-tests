def match_str(filter_str, info_dict):
    raise NotImplementedError("patch this in tests")

def match_filter_func(filter_str):
    def _match_func(info_dict):
        if match_str(filter_str, info_dict):
            return None
        else:
            video_title = info_dict.get('title', info_dict.get('id', 'video'))
            return '%s does not pass filter %s, skipping ..' % (video_title, filter_str)
    return _match_func
