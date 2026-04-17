Project: ansible
Bug: ansible_2
Bug ID: 2

Changed source file(s):
- lib/ansible/utils/version.py

Changed test file(s):
- (none captured in patch)

Known failing test reference(s):
"test/units/utils/test_version.py"

Why selected:
- buggy and fixed checkouts are available
- patch metadata was extracted successfully
- bug is narrow enough for focused unit test generation
- source/test context is packaged for LLM prompting

Task for model:
Generate a regression-style unit test that fails on the buggy version.
Follow repository test style.
Do not change source code.
