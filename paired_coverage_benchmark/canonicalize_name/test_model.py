import subject

def test_canonicalize_name_with_mixed_delimiters_and_case():
    input_name = "MY_Name.With..Multiple__DELIMITERS---Test-CASE"
    expected_output = "my-name-with-multiple-delimiters-test-case"
    assert subject.canonicalize_name(input_name) == expected_output
