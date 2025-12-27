# Issue #1 – Automatic Meta‑Tag Generation in Colab

**URL:** https://github.com/bonsai/fotei/issues/1

## 📖 Overview
The issue proposes adding **automatic semantic tag generation** for images and videos in the FOTEI pipeline, using Google Colab and a large‑language‑model API (Gemini 1.5 Flash).  Tags will be stored as JSON (and optionally embedded in EXIF) and later used for search and organization.

## 🎯 Goal
Create a robust, batch‑capable tagging system that runs on Colab, integrates with the existing pipeline, and provides a searchable tag database.

## 🗂️ Proposed Implementation Plan (as captured from the issue)

### Phase 1 – Gemini API Integration & Core Service
1. **Gemini API client** – install `google‑generativeai`, read `GEMINI_API_KEY` from the environment.
2. **`generate_semantic_tags` function** – send an image/video (or thumbnail) to Gemini, receive a comma‑separated list of Japanese tags, and return a cleaned `List[str]`.
3. **JSON storage** – write tags to `semantic_tags_metadata.json` alongside the media on Google Drive.

### Phase 2 – Batch Processing & Colab Optimisation
1. **Batch driver** (`batch_tagging.py`) – walk a root folder, call the Phase‑1 function, skip already‑tagged files, and write a checkpoint after each directory.
2. **Resumability** – checkpoint file (`.fotei_tag_checkpoint`) allows the job to continue after a timeout.
3. **T4 optimisation** – monitor GPU memory, use exponential back‑off, and keep the job within Colab limits.

### Phase 3 – Semantic Search & Pipeline Integration
1. **Search utility** – `search_by_tags(tags, root_dir)` loads the JSON metadata and returns matching file paths.
2. **Integration** – modify existing scripts (e.g., `10_semantic_ai_processor.py`) to filter media by tags before uploading or archiving.
3. **Optional EXIF embedding** – write tags back into image metadata for offline use.

## 📦 Deliverables
| Phase | Artifact |
|------|----------|
| 1 | `src/semantic_tagging.py` – Gemini wrapper.
| 2 | `src/batch_tagging.py` – batch driver, checkpointing.
| 3 | `src/search_tags.py` (to be added) + updated pipeline scripts.
| Documentation | Updated `doc/README.md` with usage examples and CI instructions.

## 🛠️ Current Repository State
- The project has been reorganised into `src/`, `doc/`, and `dev/`.
- The Gemini‑based tagging module (`semantic_tagging.py`) and batch driver (`batch_tagging.py`) have been added and committed on the `feature/colab-integration` branch.
- CI workflow (`.github/workflows/ci.yml`) is in place to lint, type‑check, and test the code.

## ✅ Next Steps for You
1. **Add unit tests** for `generate_semantic_tags` (mock the Gemini client) and for the batch driver.
2. **Create `src/search_tags.py`** implementing the search utility.
3. **Update documentation** (`doc/README.md`) with quick‑start instructions for Colab users.
4. **Push any further changes**; CI will automatically validate them.

---
*Generated from the GitHub issue discussion and the “Coding Plan” comment.*
## 🗂️ Broken Task TODO List (Step‑by‑Step)
- [ ] **Phase 1 – Gemini API Integration**
  - [ ] Install `google-generativeai` and set `GEMINI_API_KEY` in Colab.
  - [ ] Verify `generate_semantic_tags` implementation (already added).
  - [ ] Write unit test mocking Gemini client.
  - [ ] Add JSON storage logic and ensure file is written to Drive.
- [ ] **Phase 2 – Batch Processing**
  - [ ] Review `batch_tagging.py` for checkpoint handling.
  - [ ] Add progress bar and error handling for failed files.
  - [ ] Test resumability by interrupting the Colab run.
- [ ] **Phase 3 – Semantic Search**
  - [ ] Create `src/search_tags.py` with `search_by_tags` function.
  - [ ] Integrate search into `10_semantic_ai_processor.py`.
  - [ ] Add optional EXIF tag embedding.
- [ ] **Documentation & CI**
  - [ ] Update `doc/README.md` with usage examples.
  - [ ] Ensure CI runs tests for new modules.
  - [ ] Add a badge for CI status in the main README.
- [ ] **Final Review**
  - [ ] Verify all scripts run end‑to‑end in a Colab notebook.
  - [ ] Open a PR and request CodeRabbit review.
