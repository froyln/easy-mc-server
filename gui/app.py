"""Main application window: a single view, the create-server flow lives inline."""
import customtkinter as ctk

from . import theme
from .pages.dashboard import DashboardPage
from .pages.wizard import WizardPage

WINDOW_TITLE = "Easy MC Server"
WINDOW_SIZE = "980x640"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        theme.apply_appearance()

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(860, 560)
        self.configure(fg_color=theme.BG_PRIMARY)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_content()
        self.show_home()

    def _build_content(self) -> None:
        self.content_container = ctk.CTkFrame(self, fg_color=theme.BG_PRIMARY, corner_radius=0)
        self.content_container.grid(row=0, column=0, sticky="nsew")
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)

        self.home_page = DashboardPage(self.content_container, on_new_server=self.show_wizard)
        self.wizard_page = WizardPage(self.content_container, on_finish=self.show_home)

        for page in (self.home_page, self.wizard_page):
            page.grid(row=0, column=0, sticky="nsew")

    def show_home(self) -> None:
        self.home_page.refresh_recent_projects()
        self.home_page.tkraise()

    def show_wizard(self) -> None:
        self.wizard_page.reset()
        self.wizard_page.tkraise()
