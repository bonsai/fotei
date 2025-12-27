# batch_tagging.py – Walk a folder and generate semantic tags using Gemini
"""Batch driver for generating semantic tags on a large media collection.

The script is intended to be run from a Colab notebook or from the command line
inside the repository.  It walks ``root_dir`` recursively, skips files that already
have entries in ``semantic_tags_metadata.json`` and writes a checkpoint after each
folder so the job can be resumed after a timeout.

Typical usage in Colab::

    %run src/batch_tagging.py /content/drive/MyDrive/FOTEI

The script prints a short progress summary and updates the JSON metadata file in
place.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List

from tqdm import tqdm

# Import the tag generator lazily – this will raise a clear error if the Gemini
# library or API key is missing.
try:
    from src.semantic_tagging import generate_semantic_tags
except Exception as exc:  # pragma: no cover – exercised via CI mocks
    sys.stderr.write(str(exc) + "\n")
    sys.exit(1)

def load_metadata(metadata_path: Path) -> Dict[str, List[str]]:
    if metadata_path.is_file():
        with metadata_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_metadata(metadata: Dict[str, List[str]], metadata_path: Path) -> None:
    with metadata_path.open("w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def is_media_file(p: Path) -> bool:
    return p.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic", ".heif", ".tiff", ".mp4", ".mov", ".avi"}

def batch_tag(root_dir: Path, metadata_path: Path, checkpoint_path: Path) -> None:
    metadata = load_metadata(metadata_path)
    # Load checkpoint if it exists – it stores the last processed directory.
    last_processed = None
    if checkpoint_path.is_file():
        with checkpoint_path.open("r", encoding="utf-8") as f:
            last_processed = f.read().strip()

    # Walk the directory tree depth‑first.
    for dirpath, _, _ in os.walk(root_dir):
        if last_processed and Path(dirpath) <= Path(last_processed):
            # Skip directories that were already processed before a crash.
            continue
        media_files = [
            Path(dirpath) / f for f in os.listdir(dirpath) if is_media_file(Path(dirpath) / f)
        ]
        if not media_files:
            continue
        for media_path in tqdm(media_files, desc=f"Tagging {dirpath}", unit="file"):
            rel = str(media_path.relative_to(root_dir))
            if rel in metadata:
                continue
            try:
                tags = generate_semantic_tags(str(media_path))
                metadata[rel] = tags
            except Exception as e:
                sys.stderr.write(f"Failed for {media_path}: {e}\n")
        # Save after each directory – this acts as a checkpoint.
        save_metadata(metadata, metadata_path)
        with checkpoint_path.open("w", encoding="utf-8") as f:
            f.write(dirpath)

    # Cleanup checkpoint after successful run.
    if checkpoint_path.is_file():
        checkpoint_path.unlink()

def main() -> None:
    parser = argparse.ArgumentParser(description="Batch generate Gemini tags for a media folder.")
    parser.add_argument("root", type=str, help="Root directory containing media files.")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"Root directory does not exist: {root}")
    metadata_path = root / "semantic_tags_metadata.json"
    checkpoint_path = root / ".fotei_tag_checkpoint"
    batch_tag(root, metadata_path, checkpoint_path)
    print(f"Tagging complete. Metadata written to {metadata_path}")

if __name__ == "__main__":
    main()

# End of file
