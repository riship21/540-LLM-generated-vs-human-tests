import subject

def test_check_required_arguments_missing_param():
    argument_spec = {"name": {"required": True}, "age": {"required": False}}
    module_parameters = {"age": 25}
    try:
        subject.check_required_arguments(argument_spec, module_parameters)
        assert False
    except TypeError:
        assert True
