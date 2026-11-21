"""Where better-oss finds its code and your files.

Three places, and the scripts never guess outside them:

  PLUGIN_ROOT  the plugin's own folder (code, skills, shipped defaults).
               It is replaced on every plugin update, so nothing of yours
               lives here.
  DATA_DIR     your personal folder: your voice guide, search strategy,
               playbook, ship manifest template, and the tools' logs.
               ~/.claude/better-oss, or $BETTER_OSS_HOME if set.
  DEFAULTS_DIR the prefilled examples shipped with the plugin. A file
               missing from DATA_DIR falls back to the shipped example.
"""

import os
import re
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = PLUGIN_ROOT / "skills"
DEFAULTS_DIR = PLUGIN_ROOT / "defaults"
DATA_DIR = Path(os.environ.get("BETTER_OSS_HOME")
                or Path.home() / ".claude" / "better-oss").expanduser()

# Every prefilled example opens with an HTML comment that starts "EXAMPLE:".
# While that comment is still there, the file is the shipped example, not
# yours yet.
_EXAMPLE_BANNER = re.compile(r"<!--\s*EXAMPLE:")


def user_file(name: str) -> Path:
    """Your copy of a file if you have one, else the shipped example."""
    mine = DATA_DIR / name
    return mine if mine.exists() else DEFAULTS_DIR / name


def is_example(text: str) -> bool:
    """True while a file still carries the shipped EXAMPLE banner."""
    return bool(_EXAMPLE_BANNER.search(text))
