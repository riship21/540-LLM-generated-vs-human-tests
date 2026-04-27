import os
import subject

def test_validate_collection_path_trailing_slash_duplicates_component():
    base_path = os.path.join('/tmp', 'test_data', 'ansible_collections')
    collection_path_with_trailing_slash = base_path + os.path.sep
    expected_buggy_output = os.path.join(collection_path_with_trailing_slash, 'ansible_collections')
    result = subject.validate_collection_path(collection_path_with_trailing_slash)
    assert os.path.normpath(result) == os.path.normpath(expected_buggy_output)
