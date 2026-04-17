Execution notes for team members
================================

Project: youtube-dl
Bug ID: 1
Slug: youtube-dl_1

Buggy checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\youtube-dl_1\buggy

Fixed checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\youtube-dl_1\fixed

Known failing test reference(s):
"test/test_utils.py"

Changed source file(s):
- youtube_dl/utils.py

Changed test file(s):
- (none)

Commits:
- Buggy commit: "99036a1298089068dcf80c0985bfcc3f8c24f281"
- Fixed commit: "1cc47c667419e0eadc0a6989256ab7b276852adf"

Recommended usage:
1. Use llm_prompt_minimal.txt for a fairer baseline.
2. Use llm_prompt_enhanced.txt for richer context / RAG-style prompting.
3. Run generated tests against the buggy checkout first.
4. Check whether the same test passes or is no longer failing on the fixed checkout.
