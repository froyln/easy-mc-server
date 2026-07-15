"""Dark theme palette and typography shared across the whole GUI."""
import customtkinter as ctk

BG_PRIMARY = "#181414"
BG_SECONDARY = "#1f1919"
BG_CARD = "#241d1d"
BG_INPUT = "#2b2222"

ACCENT = "#ff5f6d"
ACCENT_HOVER = "#e6485a"
ACCENT_SOFT = "#402226"

SUCCESS = "#4caf6e"
WARNING = "#ffa447"
ERROR = "#ff5252"

TEXT_PRIMARY = "#f7f0ef"
TEXT_SECONDARY = "#c9b8b6"
TEXT_MUTED = "#8a7573"

BORDER = "#3a2e2d"

FONT_FAMILY = "Segoe UI"
FONT_MONO = "Consolas"


def apply_appearance() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")


def title_font(size: int = 22) -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight="bold")


def heading_font(size: int = 16) -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_FAMILY, size=size, weight="bold")


def body_font(size: int = 13) -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_FAMILY, size=size)


def mono_font(size: int = 12) -> ctk.CTkFont:
    return ctk.CTkFont(family=FONT_MONO, size=size)
