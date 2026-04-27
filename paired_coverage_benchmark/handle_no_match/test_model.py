from unittest.mock import Mock
import subject

def test_function_returns_correct_list_based_on_flags():
    mock_mask = Mock()
    mock_mask.any.return_value = False

    original_self_obj = Mock()
    mock_copied_obj = Mock()
    original_self_obj.copy.return_value = mock_copied_obj

    result_when_inplace = subject.handle_no_match(mock_mask, original_self_obj, True)
    assert result_when_inplace == [original_self_obj]
    original_self_obj.copy.assert_not_called()

    original_self_obj.copy.reset_mock()

    result_when_not_inplace = subject.handle_no_match(mock_mask, original_self_obj, False)
    assert result_when_not_inplace == [mock_copied_obj]
    original_self_obj.copy.assert_called_once()
    assert original_self_obj.copy.return_value is mock_copied_obj
