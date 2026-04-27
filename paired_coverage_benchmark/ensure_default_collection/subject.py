string_types = str

class AnsibleCollectionLoader:
    def __init__(self):
        self.default_collection = None

def _ensure_default_collection(collection_list=None):
    default_collection = AnsibleCollectionLoader().default_collection
    if collection_list is None:
        collection_list = []
    if default_collection:
        if isinstance(collection_list, string_types):
            collection_list = [collection_list]
        if default_collection not in collection_list:
            collection_list.insert(0, default_collection)
    if collection_list and 'ansible.builtin' not in collection_list and 'ansible.legacy' not in collection_list:
        collection_list.append('ansible.legacy')
    return collection_list
