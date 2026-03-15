import os
import sys


def resource_path(relative_path):
    """Return the correct path whether running from source or PyInstaller bundle."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__ + "/..")))
    return os.path.join(base, relative_path)


class Version:
    version = "v1.0.0"

class Constant:
    DEFAULT_RESOLUTION = "1200x1600"
    FONT_COLOR         = "#A0AFFA"
    HEADER_BACKGROUND  = "#e2202a"
    BG                 = "#fafafa"
    CARD_BG            = "#f2f2f2"
    CARD_HOVER         = "#e8e8e8"
    TEXT_PRIMARY       = "#1a1a1a"
    TEXT_MUTED         = "#888888"
    ICON_PATH          = resource_path("assets/icon.png")


class FileTypes:
    """Immutable file type constants used as filters in file dialogs."""
    PDF  = (("PDF files",  "*.pdf"),)
    WORD = (("Word files", "*.docx"),)
    ZIP  = (("ZIP archive", "*.zip"),)
    TGZ  = (("TGZ archive", "*.tar.gz"),)
