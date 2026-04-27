import subject

class Dummy:
    def __init__(self, name):
        self.name = name

def test_is_in_obj_basic_and_missing_cases():
    obj = {"a": None}
    gpr = Dummy("a")
    obj["a"] = gpr
    assert subject.is_in_obj(gpr, obj) is True
    assert subject.is_in_obj(123, obj) is False
    gpr2 = Dummy("b")
    assert subject.is_in_obj(gpr2, obj) is False
