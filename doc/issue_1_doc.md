# Issue #1 – Automatic Meta‑Tag Generation in Colab

**URL:** https://github.com/bonsai/fotei/issues/1

## Overview
The goal is to add automatic semantic tag generation for images and videos using the Gemini 1.5 Flash model in Google Colab. Tags will be stored in a JSON file (`semantic_tags_metadata.json`) and optionally embedded in EXIF metadata. This enables powerful search and organization of media assets.

## Implementation Phases

### Phase 1 – Gemini API Integration
- Install `google-generativeai` and set `GEMINI_API_KEY`.
- Implement `generate_semantic_tags(media_path)` in `src/semantic_tagging.py`.
- Add unit tests that mock the Gemini client.
- Store generated tags in `semantic_tags_metadata.json` on Drive.

### Phase 2 – Batch Processing & Colab Optimisation
- Use `src/batch_tagging.py` to walk the media tree, call the tag generator, and write a checkpoint (`.fotei_tag_checkpoint`).
- Add progress bars, error handling, and resumability.
- Optimize for Colab T4 GPU (memory monitoring, exponential back‑off).

### Phase 3 – Semantic Search & Pipeline Integration
- Create `src/search_tags.py` with `search_by_tags(tags, root_dir)`.
- Update `10_semantic_ai_processor.py` to filter media by tags before upload.
- Optional: write tags back into EXIF using `piexif`.

## Deliverables
- `src/semantic_tagging.py` – Gemini wrapper.
- `src/batch_tagging.py` – Batch driver with checkpointing.
- `src/search_tags.py` – Search utility (to be added).
- Updated documentation in `doc/README.md`.
- CI workflow (`.github/workflows/ci.yml`) covering linting, type‑checking, and tests.

## Current Status
- Phase 1 code is present and committed.
- Phase 2 driver is present; checkpoint logic needs testing.
- Issue tasks are listed in `dev/issue_1.md` as a broken‑task TODO list.

## Next Steps
1. Write unit tests for `generate_semantic_tags` (mock Gemini). 
2. Add checkpoint validation in `batch_tagging.py`.
3. Implement `search_tags.py` and integrate it.
4. Update the README with usage examples.
5. Verify CI passes for new tests.

---
*Generated from the GitHub issue discussion and the internal “Coding Plan”.*
