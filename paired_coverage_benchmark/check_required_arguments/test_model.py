import pytest
import subject

def test_check_required_arguments_raises_type_error_for_multiple_missing():
    argument_spec = {
        'required_param_a': {'required': True, 'type': 'str'},
        'optional_param_b': {'required': False, 'type': 'int', 'default': 10},
        'required_param_c': {'required': True, 'type': 'bool'},
        'required_param_d': {'required': True},
    }
    module_parameters = {
        'required_param_a': 'value_for_a',
        'optional_param_b': 20,
    }
    with pytest.raises(TypeError) as excinfo:
        subject.check_required_arguments(argument_spec, module_parameters)
    error_message = str(excinfo.value)
    assert "missing required arguments" in error_message
    assert "required_param_c" in error_message
    assert "required_param_d" in error_message
    assert "required_param_a" not in error_message
    assert "optional_param_b" not in error_message
