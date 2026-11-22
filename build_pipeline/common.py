"""
Shared helpers for the LittleSprout build pipeline. Used by both
extract_spec.py and render.py so the two stay in lockstep.
"""


def amp(text: str) -> str:
    """Escape '&' for use inside HTML (the <title>, og tags and alt text).

    Book titles are stored as plain text in the specs ("Maya & Marcus ...").
    The published pages write them as "Maya &amp; Marcus ..." in HTML and
    as plain text inside the JavaScript constants.
    """
    return text.replace("&", "&amp;")
