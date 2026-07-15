"""Horizontal step indicator showing wizard progress."""
import customtkinter as ctk

from .. import theme


class StepIndicator(ctk.CTkFrame):
    def __init__(self, master, steps: list[str], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._steps = steps
        self._labels: list[ctk.CTkLabel] = []
        self._dots: list[ctk.CTkLabel] = []

        for index, step in enumerate(steps):
            dot = ctk.CTkLabel(
                self,
                text=str(index + 1),
                width=26,
                height=26,
                corner_radius=13,
                fg_color=theme.BG_INPUT,
                text_color=theme.TEXT_MUTED,
                font=theme.body_font(12),
            )
            dot.grid(row=0, column=index * 2, padx=(0, 8))
            self._dots.append(dot)

            label = ctk.CTkLabel(
                self, text=step, font=theme.body_font(12), text_color=theme.TEXT_MUTED
            )
            label.grid(row=0, column=index * 2 + 1, padx=(0, 20), sticky="w")
            self._labels.append(label)

    def set_active(self, active_index: int) -> None:
        for index, (dot, label) in enumerate(zip(self._dots, self._labels)):
            if index < active_index:
                dot.configure(fg_color=theme.SUCCESS, text_color=theme.TEXT_PRIMARY)
                label.configure(text_color=theme.TEXT_SECONDARY)
            elif index == active_index:
                dot.configure(fg_color=theme.ACCENT, text_color=theme.TEXT_PRIMARY)
                label.configure(text_color=theme.TEXT_PRIMARY)
            else:
                dot.configure(fg_color=theme.BG_INPUT, text_color=theme.TEXT_MUTED)
                label.configure(text_color=theme.TEXT_MUTED)
