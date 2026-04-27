class _AtIndexer:
    def _convert_key(self, key, is_setter: bool = False):
        if is_setter:
            return list(key)
        return key
