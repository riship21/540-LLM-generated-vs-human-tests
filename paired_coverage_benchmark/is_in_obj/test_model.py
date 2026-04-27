import subject

class MockGPR:
    def __init__(self, name_attr=None):
        if name_attr is not None:
            self.name = name_attr

def test_is_in_obj_identity_and_edge_cases():
    gpr_target = MockGPR("item_name")
    container = {"item_name": gpr_target, "other_item": MockGPR("other_name")}
    assert subject.is_in_obj(gpr_target, container) is True

    gpr_different_instance = MockGPR("item_name")
    assert subject.is_in_obj(gpr_different_instance, container) is False

    gpr_no_name = MockGPR()
    assert subject.is_in_obj(gpr_no_name, container) is False

    gpr_missing_key = MockGPR("non_existent_key")
    assert subject.is_in_obj(gpr_missing_key, container) is False

    gpr_list_item = MockGPR(0)
    list_container = [gpr_list_item, MockGPR(1)]
    assert subject.is_in_obj(gpr_list_item, list_container) is True

    gpr_invalid_index = MockGPR(999)
    assert subject.is_in_obj(gpr_invalid_index, list_container) is False

    assert subject.is_in_obj(gpr_target, None) is False
    assert subject.is_in_obj(gpr_target, 123) is False
