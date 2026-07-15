"""A clickable card that highlights when selected, used for option pickers."""
from typing import Callable

import customtkinter as ctk

from .. import theme


class SelectableCard(ctk.CTkFrame):
    def __init__(
        self,
        master,
        title: str,
        subtitle: str = "",
        on_select: Callable[[], None] | None = None,
        **kwargs,
    ):
        super().__init__(
            master,
            fg_color=theme.BG_CARD,
            corner_radius=10,
            border_width=2,
            border_color=theme.BORDER,
            **kwargs,
        )
        self._on_select = on_select
        self._selected = False

        self.title_label = ctk.CTkLabel(
            self, text=title, font=theme.heading_font(14), text_color=theme.TEXT_PRIMARY
        )
        self.title_label.pack(padx=16, pady=(14, 2), anchor="w")

        if subtitle:
            self.subtitle_label = ctk.CTkLabel(
                self, text=subtitle, font=theme.body_font(12), text_color=theme.TEXT_MUTED
            )
            self.subtitle_label.pack(padx=16, pady=(0, 14), anchor="w")
        else:
            self.subtitle_label = None
            ctk.CTkFrame(self, fg_color="transparent", height=8).pack()

        for widget in (self, self.title_label, self.subtitle_label):
            if widget is not None:
                widget.bind("<Button-1>", self._handle_click)

    def _handle_click(self, _event=None) -> None:
        if self._on_select is not None:
            self._on_select()

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.configure(border_color=theme.ACCENT if selected else theme.BORDER)
        self.configure(fg_color=theme.ACCENT_SOFT if selected else theme.BG_CARD)
