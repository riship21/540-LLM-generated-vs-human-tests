Execution notes for team members
================================

Project: youtube-dl
Bug ID: 2
Slug: youtube-dl_2

Buggy checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\youtube-dl_2\buggy

Fixed checkout path:
C:\COSC540\github_mining_starter\workspace\checkouts\youtube-dl_2\fixed

Known failing test reference(s):
"test/test_InfoExtractor.py"

Changed source file(s):
- youtube_dl/extractor/common.py

Changed test file(s):
- (none)

Commits:
- Buggy commit: "84f085d4bdb66ee025fb337bcd571eab7469da97"
- Fixed commit: "9d6ac71c27b1dfb662c795ef598dbfd0286682da"

Recommended usage:
1. Use llm_prompt_minimal.txt for a fairer baseline.
2. Use llm_prompt_enhanced.txt for richer context / RAG-style prompting.
3. Run generated tests against the buggy checkout first.
4. Check whether the same test passes or is no longer failing on the fixed checkout.
