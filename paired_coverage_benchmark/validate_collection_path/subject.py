import os

def validate_collection_path(collection_path):
    if os.path.split(collection_path)[1] != 'ansible_collections':
        return os.path.join(collection_path, 'ansible_collections')
    return collection_path
