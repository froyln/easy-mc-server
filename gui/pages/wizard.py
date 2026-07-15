"""Step-by-step wizard to configure and create a new Minecraft server."""
import threading
from dataclasses import dataclass, field
from pathlib import Path
from tkinter import filedialog
from typing import Callable

import customtkinter as ctk

from core.downloader import DownloadError
from core.process_runner import ProcessError
from core.project_manager import ServerRequest, create_server
from core.recent_projects import RecentProject, add_recent
from core.server_types import SERVER_TYPES, get_installer

from .. import theme
from ..widgets.console import LogConsole
from ..widgets.selectable_card import SelectableCard
from ..widgets.step_indicator import StepIndicator

STEP_TITLES = ["Basics", "Server type", "Version", "Resources", "Create"]

SERVER_TYPE_SUBTITLES = {
    "vanilla": "Official Mojang server, no mods or plugins.",
    "fabric": "Lightweight modding platform.",
    "forge": "The classic modding platform.",
    "paper": "High-performance server with plugin support.",
}


@dataclass
class WizardState:
    project_name: str = "my-server"
    destination: Path = field(default_factory=Path.cwd)
    use_mcdreforged: bool = False
    server_type_id: str = "vanilla"
    mc_version: str = ""
    loader_version: str = ""
    installer_version: str = ""
    min_ram_mb: str = "1024"
    max_ram_mb: str = "2048"


class WizardPage(ctk.CTkFrame):
    def __init__(self, master, on_finish: Callable[[], None], **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self._on_finish = on_finish
        self.state = WizardState()
        self._current_step = 0
        self._version_cache: dict[str, list[str]] = {}
        self._creation_running = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_footer_placeholder()

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=2, column=0, sticky="nsew", padx=32, pady=(4, 4))
        self.content_frame.grid_columnconfigure(0, weight=1)

        self._render_step()

    def reset(self) -> None:
        self.state = WizardState()
        self._current_step = 0
        self._creation_running = False
        self._render_step()

    def _build_header(self) -> None:
        title = ctk.CTkLabel(
            self, text="Create New Server", font=theme.title_font(24), text_color=theme.TEXT_PRIMARY
        )
        title.grid(row=0, column=0, sticky="w", padx=32, pady=(28, 12))

        self.step_indicator = StepIndicator(self, STEP_TITLES)
        self.step_indicator.grid(row=1, column=0, sticky="w", padx=32, pady=(0, 12))

    def _build_footer_placeholder(self) -> None:
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=3, column=0, sticky="ew", padx=32, pady=(4, 24))
        footer.grid_columnconfigure(0, weight=1)

        self.back_button = ctk.CTkButton(
            footer, text="Back", width=110, height=38, fg_color=theme.BG_INPUT,
            hover_color=theme.BORDER, command=self._go_back,
        )
        self.back_button.grid(row=0, column=1, padx=(0, 10))

        self.next_button = ctk.CTkButton(
            footer, text="Next", width=110, height=38, fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER, command=self._go_next,
        )
        self.next_button.grid(row=0, column=2)

    def _clear_content(self) -> None:
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _render_step(self) -> None:
        self.step_indicator.set_active(self._current_step)
        self._clear_content()

        renderers = [
            self._render_basics_step,
            self._render_server_type_step,
            self._render_version_step,
            self._render_resources_step,
            self._render_create_step,
        ]
        renderers[self._current_step]()

        self.back_button.configure(state="disabled" if self._current_step == 0 else "normal")
        is_last_step = self._current_step == len(STEP_TITLES) - 1
        self.next_button.configure(text="Create Server" if is_last_step else "Next")
        if is_last_step:
            self.next_button.configure(command=self._start_creation)
        else:
            self.next_button.configure(command=self._go_next)

    def _go_back(self) -> None:
        if self._current_step > 0:
            self._current_step -= 1
            self._render_step()

    def _go_next(self) -> None:
        if not self._validate_current_step():
            return
        if self._current_step < len(STEP_TITLES) - 1:
            self._current_step += 1
            self._render_step()

    def _validate_current_step(self) -> bool:
        if self._current_step == 0:
            if not self.state.project_name.strip():
                self._show_error("Please enter a project name.")
                return False
        if self._current_step == 2:
            if not self.state.mc_version:
                self._show_error("Please select a Minecraft version.")
                return False
        return True

    def _show_error(self, message: str) -> None:
        error_label = ctk.CTkLabel(
            self.content_frame, text=message, font=theme.body_font(12), text_color=theme.ERROR
        )
        error_label.grid(row=99, column=0, sticky="w", pady=(12, 0))

    # --- Step 0: basics -------------------------------------------------

    def _render_basics_step(self) -> None:
        card = ctk.CTkFrame(self.content_frame, fg_color=theme.BG_CARD, corner_radius=12)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text="Project name", font=theme.heading_font(13), text_color=theme.TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 4))

        name_entry = ctk.CTkEntry(
            card, fg_color=theme.BG_INPUT, border_width=0, height=38, font=theme.body_font(13)
        )
        name_entry.insert(0, self.state.project_name)
        name_entry.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 16))
        name_entry.bind("<KeyRelease>", lambda e: setattr(self.state, "project_name", name_entry.get()))

        ctk.CTkLabel(
            card, text="Destination folder", font=theme.heading_font(13), text_color=theme.TEXT_PRIMARY
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 4))

        path_row = ctk.CTkFrame(card, fg_color="transparent")
        path_row.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        path_row.grid_columnconfigure(0, weight=1)

        self._path_entry = ctk.CTkEntry(
            path_row, fg_color=theme.BG_INPUT, border_width=0, height=38, font=theme.body_font(13)
        )
        self._path_entry.insert(0, str(self.state.destination))
        self._path_entry.grid(row=0, column=0, sticky="ew")
        self._path_entry.bind(
            "<KeyRelease>", lambda e: setattr(self.state, "destination", Path(self._path_entry.get()))
        )

        browse_button = ctk.CTkButton(
            path_row, text="Browse...", width=100, height=38, fg_color=theme.BG_INPUT,
            hover_color=theme.BORDER, command=self._browse_destination,
        )
        browse_button.grid(row=0, column=1, padx=(10, 0))

        mcdr_card = ctk.CTkFrame(self.content_frame, fg_color=theme.BG_CARD, corner_radius=12)
        mcdr_card.grid(row=1, column=0, sticky="ew", pady=(16, 0))
        mcdr_card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            mcdr_card, text="Use MCDReforged", font=theme.heading_font(13), text_color=theme.TEXT_PRIMARY
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 2))
        ctk.CTkLabel(
            mcdr_card,
            text="Wraps the server with MCDReforged for plugins, console tools and management.",
            font=theme.body_font(12), text_color=theme.TEXT_MUTED,
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 16))

        mcdr_switch = ctk.CTkSwitch(
            mcdr_card, text="", progress_color=theme.ACCENT, command=lambda: self._toggle_mcdr(mcdr_switch)
        )
        if self.state.use_mcdreforged:
            mcdr_switch.select()
        mcdr_switch.grid(row=0, column=1, rowspan=2, padx=20)

    def _toggle_mcdr(self, switch: ctk.CTkSwitch) -> None:
        self.state.use_mcdreforged = bool(switch.get())

    def _browse_destination(self) -> None:
        selected = filedialog.askdirectory(initialdir=str(self.state.destination))
        if selected:
            self.state.destination = Path(selected)
            self._path_entry.delete(0, "end")
            self._path_entry.insert(0, selected)

    # --- Step 1: server type ---------------------------------------------

    def _render_server_type_step(self) -> None:
        grid = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        grid.grid(row=0, column=0, sticky="ew")
        grid.grid_columnconfigure((0, 1), weight=1)

        self._type_cards: dict[str, SelectableCard] = {}
        for index, type_id in enumerate(SERVER_TYPES):
            installer_cls = SERVER_TYPES[type_id]
            card = SelectableCard(
                grid,
                title=installer_cls.display_name,
                subtitle=SERVER_TYPE_SUBTITLES.get(type_id, ""),
                on_select=lambda t=type_id: self._select_server_type(t),
                height=90,
            )
            card.grid(row=index // 2, column=index % 2, sticky="ew", padx=8, pady=8)
            card.set_selected(type_id == self.state.server_type_id)
            self._type_cards[type_id] = card

    def _select_server_type(self, type_id: str) -> None:
        self.state.server_type_id = type_id
        self.state.mc_version = ""
        for tid, card in self._type_cards.items():
            card.set_selected(tid == type_id)

    # --- Step 2: version ---------------------------------------------------

    def _render_version_step(self) -> None:
        card = ctk.CTkFrame(self.content_frame, fg_color=theme.BG_CARD, corner_radius=12)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        installer_cls = SERVER_TYPES[self.state.server_type_id]

        ctk.CTkLabel(
            card, text=f"Minecraft version ({installer_cls.display_name})",
            font=theme.heading_font(13), text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 4))

        self._mc_version_combo = ctk.CTkComboBox(
            card, values=["Loading..."], fg_color=theme.BG_INPUT, border_width=0,
            button_color=theme.ACCENT, button_hover_color=theme.ACCENT_HOVER,
            height=38, font=theme.body_font(13), command=self._on_mc_version_selected,
        )
        self._mc_version_combo.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        self._mc_version_combo.set("Loading...")

        self._extra_row_index = 2
        self._loader_combo = None
        self._installer_combo = None
        if installer_cls().requires_loader_selection:
            self._add_loader_selectors(card)

        self._load_versions_async()

    def _add_loader_selectors(self, card: ctk.CTkFrame) -> None:
        ctk.CTkLabel(
            card, text="Fabric loader version", font=theme.heading_font(13), text_color=theme.TEXT_PRIMARY
        ).grid(row=self._extra_row_index, column=0, sticky="w", padx=20, pady=(0, 4))
        self._loader_combo = ctk.CTkComboBox(
            card, values=["Loading..."], fg_color=theme.BG_INPUT, border_width=0,
            button_color=theme.ACCENT, button_hover_color=theme.ACCENT_HOVER,
            height=38, font=theme.body_font(13),
            command=lambda v: setattr(self.state, "loader_version", v),
        )
        self._loader_combo.grid(row=self._extra_row_index + 1, column=0, sticky="ew", padx=20, pady=(0, 20))
        self._extra_row_index += 2

        ctk.CTkLabel(
            card, text="Fabric installer version", font=theme.heading_font(13), text_color=theme.TEXT_PRIMARY
        ).grid(row=self._extra_row_index, column=0, sticky="w", padx=20, pady=(0, 4))
        self._installer_combo = ctk.CTkComboBox(
            card, values=["Loading..."], fg_color=theme.BG_INPUT, border_width=0,
            button_color=theme.ACCENT, button_hover_color=theme.ACCENT_HOVER,
            height=38, font=theme.body_font(13),
            command=lambda v: setattr(self.state, "installer_version", v),
        )
        self._installer_combo.grid(row=self._extra_row_index + 1, column=0, sticky="ew", padx=20, pady=(0, 20))
        self._extra_row_index += 2

    def _on_mc_version_selected(self, value: str) -> None:
        self.state.mc_version = value

    def _load_versions_async(self) -> None:
        installer = get_installer(self.state.server_type_id)
        threading.Thread(target=self._load_versions_worker, args=(installer,), daemon=True).start()

    def _load_versions_worker(self, installer) -> None:
        try:
            versions = installer.list_versions(lambda msg: None)
        except DownloadError:
            versions = []
        loader_versions: list[str] = []
        installer_versions: list[str] = []
        if installer.requires_loader_selection:
            try:
                loader_versions = installer.list_loader_versions(lambda msg: None)
                installer_versions = installer.list_installer_versions(lambda msg: None)
            except DownloadError:
                pass

        self.after(0, lambda: self._apply_loaded_versions(versions, loader_versions, installer_versions))

    def _apply_loaded_versions(
        self, versions: list[str], loader_versions: list[str], installer_versions: list[str]
    ) -> None:
        if self._current_step != 2:
            return

        if versions:
            self._mc_version_combo.configure(values=versions)
            self._mc_version_combo.set(versions[0])
            self.state.mc_version = versions[0]
        else:
            self._mc_version_combo.configure(values=["No versions found"])
            self._mc_version_combo.set("No versions found")

        if self._loader_combo is not None and loader_versions:
            self._loader_combo.configure(values=loader_versions)
            self._loader_combo.set(loader_versions[0])
            self.state.loader_version = loader_versions[0]

        if self._installer_combo is not None and installer_versions:
            self._installer_combo.configure(values=installer_versions)
            self._installer_combo.set(installer_versions[0])
            self.state.installer_version = installer_versions[0]

    # --- Step 3: resources ---------------------------------------------------

    def _render_resources_step(self) -> None:
        card = ctk.CTkFrame(self.content_frame, fg_color=theme.BG_CARD, corner_radius=12)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            card, text="Memory allocation", font=theme.heading_font(13), text_color=theme.TEXT_PRIMARY
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 4))
        ctk.CTkLabel(
            card, text="Values are in megabytes. 1024 MB = 1 GB.",
            font=theme.body_font(12), text_color=theme.TEXT_MUTED,
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 14))

        ctk.CTkLabel(
            card, text="Minimum RAM (MB)", font=theme.body_font(12), text_color=theme.TEXT_SECONDARY
        ).grid(row=2, column=0, sticky="w", padx=20)
        min_entry = ctk.CTkEntry(card, fg_color=theme.BG_INPUT, border_width=0, height=38)
        min_entry.insert(0, self.state.min_ram_mb)
        min_entry.grid(row=3, column=0, sticky="ew", padx=(20, 10), pady=(4, 20))
        min_entry.bind("<KeyRelease>", lambda e: setattr(self.state, "min_ram_mb", min_entry.get()))

        ctk.CTkLabel(
            card, text="Maximum RAM (MB)", font=theme.body_font(12), text_color=theme.TEXT_SECONDARY
        ).grid(row=2, column=1, sticky="w", padx=(10, 20))
        max_entry = ctk.CTkEntry(card, fg_color=theme.BG_INPUT, border_width=0, height=38)
        max_entry.insert(0, self.state.max_ram_mb)
        max_entry.grid(row=3, column=1, sticky="ew", padx=(10, 20), pady=(4, 20))
        max_entry.bind("<KeyRelease>", lambda e: setattr(self.state, "max_ram_mb", max_entry.get()))

        self._render_summary_card()

    def _render_summary_card(self) -> None:
        summary = ctk.CTkFrame(self.content_frame, fg_color=theme.BG_CARD, corner_radius=12)
        summary.grid(row=1, column=0, sticky="ew", pady=(16, 0))
        summary.grid_columnconfigure(1, weight=1)

        installer_cls = SERVER_TYPES[self.state.server_type_id]
        rows = [
            ("Project", self.state.project_name),
            ("Destination", str(self.state.destination)),
            ("Server type", installer_cls.display_name),
            ("Minecraft version", self.state.mc_version or "-"),
            ("MCDReforged", "Yes" if self.state.use_mcdreforged else "No"),
        ]
        for index, (label, value) in enumerate(rows):
            ctk.CTkLabel(
                summary, text=label, font=theme.body_font(12), text_color=theme.TEXT_MUTED, anchor="w"
            ).grid(row=index, column=0, sticky="w", padx=(20, 12), pady=(14 if index == 0 else 4))
            ctk.CTkLabel(
                summary, text=value, font=theme.body_font(12), text_color=theme.TEXT_PRIMARY, anchor="w"
            ).grid(row=index, column=1, sticky="w", pady=(14 if index == 0 else 4))
        ctk.CTkFrame(summary, fg_color="transparent", height=10).grid(row=len(rows), column=0)

    # --- Step 4: create ---------------------------------------------------

    def _render_create_step(self) -> None:
        self.content_frame.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(self.content_frame, fg_color=theme.BG_CARD, corner_radius=12)
        card.grid(row=0, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            card, text="Ready to create your server", font=theme.heading_font(14),
            text_color=theme.TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 8))

        self._progress_bar = ctk.CTkProgressBar(card, progress_color=theme.ACCENT, fg_color=theme.BG_INPUT)
        self._progress_bar.set(0)
        self._progress_bar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        self._log_console = LogConsole(card, height=220)
        self._log_console.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def _start_creation(self) -> None:
        if self._creation_running:
            return
        self._creation_running = True
        self.next_button.configure(state="disabled", text="Creating...")
        self.back_button.configure(state="disabled")
        self._log_console.clear()
        self._progress_bar.set(0)

        request = ServerRequest(
            destination=self.state.destination,
            server_type_id=self.state.server_type_id,
            mc_version=self.state.mc_version,
            use_mcdreforged=self.state.use_mcdreforged,
            min_ram_mb=self.state.min_ram_mb or "1024",
            max_ram_mb=self.state.max_ram_mb or "2048",
            loader_version=self.state.loader_version or None,
            installer_version=self.state.installer_version or None,
        )
        threading.Thread(target=self._run_creation, args=(request,), daemon=True).start()

    def _run_creation(self, request: ServerRequest) -> None:
        def log(message: str) -> None:
            self.after(0, lambda: self._log_console.write(message))

        def progress(done: int, total: int) -> None:
            fraction = (done / total) if total else 0
            self.after(0, lambda: self._progress_bar.set(min(fraction, 1.0)))

        try:
            create_server(request, log, progress)
            add_recent(
                RecentProject(
                    name=self.state.project_name,
                    path=str(self.state.destination),
                    server_type=self.state.server_type_id,
                    mc_version=self.state.mc_version,
                    used_mcdreforged=self.state.use_mcdreforged,
                )
            )
            self.after(0, self._on_creation_success)
        except (DownloadError, ProcessError, ValueError, OSError) as exc:
            self.after(0, lambda: self._on_creation_failure(str(exc)))

    def _on_creation_success(self) -> None:
        self._log_console.write("Server created successfully.", level="success")
        self._progress_bar.set(1.0)
        self.next_button.configure(state="normal", text="Finish", command=self._finish)
        self.back_button.configure(state="normal")

    def _on_creation_failure(self, message: str) -> None:
        self._log_console.write(f"Error: {message}", level="error")
        self.next_button.configure(state="normal", text="Retry", command=self._start_creation)
        self.back_button.configure(state="normal")
        self._creation_running = False

    def _finish(self) -> None:
        self._on_finish()
