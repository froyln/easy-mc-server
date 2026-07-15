"""Read-only, auto-scrolling console for streaming install logs."""
import customtkinter as ctk

from .. import theme

LEVEL_COLORS = {
    "info": theme.TEXT_SECONDARY,
    "success": theme.SUCCESS,
    "warning": theme.WARNING,
    "error": theme.ERROR,
}


class LogConsole(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("fg_color", theme.BG_INPUT)
        kwargs.setdefault("text_color", theme.TEXT_SECONDARY)
        kwargs.setdefault("font", theme.mono_font(12))
        kwargs.setdefault("corner_radius", 8)
        kwargs.setdefault("wrap", "word")
        super().__init__(master, **kwargs)

        for level, color in LEVEL_COLORS.items():
            self.tag_config(level, foreground=color)

        self.configure(state="disabled")

    def write(self, message: str, level: str = "info") -> None:
        self.configure(state="normal")
        self.insert("end", message.rstrip() + "\n", level)
        self.configure(state="disabled")
        self.see("end")

    def clear(self) -> None:
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.configure(state="disabled")
