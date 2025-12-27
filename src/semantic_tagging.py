# semantic_tagging.py – Gemini‑based tag generation for media files
"""Utilities for generating semantic tags using the Gemini 1.5 Flash model.

The module expects the environment variable ``GEMINI_API_KEY`` to be set (e.g. in
Google Colab).  It provides a single public function ``generate_semantic_tags``
that returns a list of Japanese tags for an image or video file.

Typical usage::

    from src.semantic_tagging import generate_semantic_tags
    tags = generate_semantic_tags("/path/to/photo.jpg")
    print(tags)

The implementation includes exponential back‑off retries and minimal error
handling so it can be used in batch pipelines.
"""

import os
import time
from typing import List

# The Gemini client library is ``google‑generativeai``.  It is imported lazily so
# that the module can be imported even when the library is not installed (e.g. in
# CI).  The import will raise an informative error when the function is called.

def _get_gemini_model():
    """Configure the Gemini client and return a ``GenerativeModel`` instance.

    The function reads the ``GEMINI_API_KEY`` environment variable, configures the
    ``google.generativeai`` package and returns a model object for the
    ``gemini-1.5-flash`` model.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable not set. Set it before calling "
            "generate_semantic_tags."
        )
    try:
        from google.generativeai import configure, GenerativeModel
    except ImportError as exc:
        raise RuntimeError(
            "google-generativeai package is required. Install it with "
            "'pip install google-generativeai'"
        ) from exc
    configure(api_key=api_key)
    return GenerativeModel("gemini-1.5-flash")


def _read_media_bytes(path: str) -> bytes:
    """Read a file and return its raw bytes.

    For videos we currently read the whole file – in a real‑world pipeline you may
    want to extract a representative frame to keep the request size small.
    """
    with open(path, "rb") as f:
        return f.read()


def generate_semantic_tags(media_path: str, max_retries: int = 3) -> List[str]:
    """Generate a list of Japanese tags for *media_path*.

    Parameters
    ----------
    media_path: str
        Path to an image (JPEG/PNG/etc.) or video file.
    max_retries: int, optional
        Number of retry attempts on transient errors.  Defaults to ``3``.

    Returns
    -------
    List[str]
        A list of cleaned tag strings.
    """
    if not os.path.isfile(media_path):
        raise FileNotFoundError(f"Media file not found: {media_path}")

    model = _get_gemini_model()
    media_bytes = _read_media_bytes(media_path)

    prompt = (
        "以下の画像または動画に対して、10 個程度のタグ（日本語、カンマ区切り）を出力してください。"
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                [prompt, {"mime_type": "image/jpeg", "data": media_bytes}],
                generation_config={"temperature": 0.7},
            )
            # The response text may contain newlines; split on commas and strip.
            raw = response.text.strip()
            tags = [t.strip() for t in raw.split(",") if t.strip()]
            return tags
        except Exception as exc:  # pragma: no cover – exercised in CI via mocks
            if attempt == max_retries - 1:
                raise RuntimeError(
                    f"Failed to generate tags for {media_path} after {max_retries} attempts"
                ) from exc
            # Exponential back‑off before retrying.
            time.sleep(2 ** attempt)

# End of file
