"""The Robot Vacuum's Best Excuse (make.fun).

The vacuum explains why the Cheerio under the couch is still there:
it found the crumb, named him Gerald, and now cleans around him out of
respect. One line, deadpan, in the vacuum's own voice.

The program writes the entry to /output/entry.txt after gate-checking it:
one line, 1 to 140 characters, valid UTF-8. Pure standard library,
deterministic, no network.
"""

import os
import sys

ENTRY = "I found a Cheerio under the couch, named him Gerald, and now I clean around him out of respect."


def validate_entry(text):
    """Check the entry against the kit gate. Returns an error string or None."""
    if not isinstance(text, str):
        return "entry is not text"
    if text != text.strip():
        return "entry has leading or trailing whitespace"
    if not text:
        return "entry is empty"
    if len(text) > 140:
        return "entry is %d characters, over the 140 limit" % len(text)
    if "\n" in text or "\r" in text:
        return "entry is not one line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8"
    return None


def main():
    error = validate_entry(ENTRY)
    if error is not None:
        print("gate failed: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    print("wrote %s (%d chars)" % (path, len(ENTRY)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
