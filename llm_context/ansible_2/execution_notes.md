Execution notes for team members
================================

Project: ansible
Bug ID: 2
Slug: ansible_2

Buggy checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\ansible_2\buggy

Fixed checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\ansible_2\fixed

Known failing test reference(s):
"test/units/utils/test_version.py"

Changed source file(s):
- lib/ansible/utils/version.py

Changed test file(s):
- (none)

Commits:
- Buggy commit: "de59b17c7f69d5cfb72479b71776cc8b97e29a6b"
- Fixed commit: "5b9418c06ca6d51507468124250bb58046886be6"

Recommended usage:
1. Use llm_prompt_minimal.txt for a fairer baseline.
2. Use llm_prompt_enhanced.txt for richer context / RAG-style prompting.
3. Run generated tests against the buggy checkout first.
4. Check whether the same test passes or is no longer failing on the fixed checkout.
