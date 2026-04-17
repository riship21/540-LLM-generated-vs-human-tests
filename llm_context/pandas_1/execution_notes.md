Execution notes for team members
================================

Project: pandas
Bug ID: 1
Slug: pandas_1

Buggy checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\pandas_1\buggy

Fixed checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\pandas_1\fixed

Known failing test reference(s):
"pandas/tests/dtypes/test_dtypes.py"

Changed source file(s):
- pandas/core/dtypes/common.py

Changed test file(s):
- (none)

Commits:
- Buggy commit: "3fd150c"
- Fixed commit: "e41ee47a90bb1d8a1fa28fcefcd45ed8ef5cb946"

Recommended usage:
1. Use llm_prompt_minimal.txt for a fairer baseline.
2. Use llm_prompt_enhanced.txt for richer context / RAG-style prompting.
3. Run generated tests against the buggy checkout first.
4. Check whether the same test passes or is no longer failing on the fixed checkout.
