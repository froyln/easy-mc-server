"""Landing page: dependency status, quick actions and recent projects."""
import os
import platform
import subprocess
import threading
from pathlib import Path
from typing import Callable

import customtkinter as ctk

from core import recent_projects, system_check

from .. import theme


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, on_new_server: Callable[[], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_new_server = on_new_server

        self.grid_columnconfigure(0, weight=1)

        subheader = ctk.CTkLabel(
            self,
            text="Easy Minecraft Server",
            font=theme.title_font(20),
            text_color=theme.TEXT_PRIMARY,
        )
        subheader.grid(row=1, column=0, sticky="w", padx=32, pady=(28, 20))

        self._build_java_card()
        self._build_new_server_button()
        self._build_recent_projects()

    def _build_java_card(self) -> None:
        card = ctk.CTkFrame(self, fg_color=theme.BG_CARD, corner_radius=12)
        card.grid(row=2, column=0, sticky="ew", padx=32, pady=8)
        card.grid_columnconfigure(1, weight=1)

        self._java_dot = ctk.CTkLabel(
            card, text="●", font=theme.heading_font(18), text_color=theme.TEXT_MUTED, width=20
        )
        self._java_dot.grid(row=0, column=0, padx=(18, 4), pady=16)

        self._java_label = ctk.CTkLabel(
            card, text="Checking Java installation...", font=theme.body_font(13),
            text_color=theme.TEXT_SECONDARY, anchor="w",
        )
        self._java_label.grid(row=0, column=1, sticky="w", pady=16)

        os_label = ctk.CTkLabel(
            card, text=f"OS: {platform.system()}", font=theme.body_font(12),
            text_color=theme.TEXT_MUTED,
        )
        os_label.grid(row=0, column=2, padx=18, pady=16)

        threading.Thread(target=self._check_java, daemon=True).start()

    def _check_java(self) -> None:
        status = system_check.check_java(min_version=21)
        self.after(0, lambda: self._update_java_card(status))

    def _update_java_card(self, status: system_check.JavaStatus) -> None:
        if not status.installed:
            self._java_dot.configure(text_color=theme.ERROR)
            self._java_label.configure(text="Java was not found. Install Java 21+ to run any server.")
        elif status.version is not None and status.version < 21:
            self._java_dot.configure(text_color=theme.WARNING)
            self._java_label.configure(
                text=f"Java {status.version} detected. Java 21+ is recommended for modern servers."
            )
        else:
            self._java_dot.configure(text_color=theme.SUCCESS)
            version_text = status.version if status.version is not None else "unknown"
            self._java_label.configure(text=f"Java {version_text} detected and ready.")

    def _build_new_server_button(self) -> None:
        button = ctk.CTkButton(
            self,
            text="+  Create New Server",
            font=theme.heading_font(15),
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            height=48,
            corner_radius=10,
            command=self._on_new_server,
        )
        button.grid(row=3, column=0, sticky="w", padx=32, pady=(20, 24))

    def _build_recent_projects(self) -> None:
        label = ctk.CTkLabel(
            self, text="Recent servers", font=theme.heading_font(15), text_color=theme.TEXT_PRIMARY
        )
        label.grid(row=4, column=0, sticky="w", padx=32, pady=(4, 8))

        self._recent_container = ctk.CTkFrame(self, fg_color="transparent")
        self._recent_container.grid(row=5, column=0, sticky="ew", padx=32, pady=(0, 24))
        self._recent_container.grid_columnconfigure(0, weight=1)

        self.refresh_recent_projects()

    def refresh_recent_projects(self) -> None:
        for widget in self._recent_container.winfo_children():
            widget.destroy()

        projects = recent_projects.load_recent()
        if not projects:
            empty_label = ctk.CTkLabel(
                self._recent_container,
                text="No servers created yet. Click \"Create New Server\" to get started.",
                font=theme.body_font(12),
                text_color=theme.TEXT_MUTED,
            )
            empty_label.grid(row=0, column=0, sticky="w", pady=8)
            return

        for index, project in enumerate(projects):
            self._build_project_row(index, project)

    def _build_project_row(self, index: int, project: recent_projects.RecentProject) -> None:
        row = ctk.CTkFrame(self._recent_container, fg_color=theme.BG_CARD, corner_radius=10)
        row.grid(row=index, column=0, sticky="ew", pady=4)
        row.grid_columnconfigure(1, weight=1)

        badge_text = project.server_type.capitalize()
        if project.used_mcdreforged:
            badge_text += " + MCDR"
        badge = ctk.CTkLabel(
            row, text=badge_text, font=theme.body_font(11), text_color=theme.TEXT_PRIMARY,
            fg_color=theme.ACCENT_SOFT, corner_radius=6, width=110,
        )
        badge.grid(row=0, column=0, padx=(14, 12), pady=12)

        info = ctk.CTkLabel(
            row,
            text=f"{project.name}  ·  Minecraft {project.mc_version}  ·  {project.path}",
            font=theme.body_font(12),
            text_color=theme.TEXT_SECONDARY,
            anchor="w",
        )
        info.grid(row=0, column=1, sticky="w", pady=12)

        open_button = ctk.CTkButton(
            row, text="Open folder", width=100, height=28, font=theme.body_font(11),
            fg_color=theme.BG_INPUT, hover_color=theme.BORDER,
            command=lambda p=project.path: self._open_folder(p),
        )
        open_button.grid(row=0, column=2, padx=14, pady=12)

    @staticmethod
    def _open_folder(path: str) -> None:
        if not Path(path).exists():
            return
        if system_check.is_windows():
            os.startfile(path)  # noqa: S606
        elif system_check.is_macos():
            subprocess.run(["open", path], check=False)
        else:
            subprocess.run(["xdg-open", path], check=False)
