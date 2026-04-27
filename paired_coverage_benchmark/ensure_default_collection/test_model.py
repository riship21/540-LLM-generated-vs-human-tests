from unittest.mock import MagicMock, patch
import subject

def test_ensure_default_collection_none_input_adds_default_and_legacy():
    with patch('subject.AnsibleCollectionLoader') as MockLoader:
        mock_loader_instance = MagicMock()
        mock_loader_instance.default_collection = "my.test_default_collection"
        MockLoader.return_value = mock_loader_instance
        actual_list = subject._ensure_default_collection(None)
        expected_list = ["my.test_default_collection", "ansible.legacy"]
        assert actual_list == expected_list
