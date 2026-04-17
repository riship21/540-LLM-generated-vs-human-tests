Project: pandas
Bug: pandas_2
Bug ID: 2

Changed source file(s):
- pandas/core/indexing.py

Changed test file(s):
- (none captured in patch)

Known failing test reference(s):
"pandas/tests/indexing/test_scalar.py"

Why selected:
- buggy and fixed checkouts are available
- patch metadata was extracted successfully
- bug is narrow enough for focused unit test generation
- source/test context is packaged for LLM prompting

Task for model:
Generate a regression-style unit test that fails on the buggy version.
Follow repository test style.
Do not change source code.
