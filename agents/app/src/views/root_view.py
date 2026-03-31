"""
views/root_view.py
──────────────────────────────────────────────────────────────────────
RootView is the top-level layout controller.

It owns the three-column layout:
    [ Sidebar ]  [ ChatView ]  [ InfoPanel ]

And handles two global events:
    • on_nav_change    — user clicks a sidebar nav item
    • on_theme_toggle  — user flips the dark/light switch

After either event, it calls mount() to rebuild and re-render the
full UI with the new state.

WHY FULL REBUILD INSTEAD OF PARTIAL UPDATE?
  A full rebuild is simpler to reason about for beginners and is fast
  enough for this app.  If you later add heavy animations or large
  data tables, you can optimise specific components to update
  themselves in place (like ChatView already does for new bubbles).
──────────────────────────────────────────────────────────────────────
"""

import flet as ft

from utils.state  import AppState
from utils.theme  import apply_page_theme, bg

from components.sidebar    import Sidebar
from components.info_panel import InfoPanel
from views.chat_view       import ChatView


class RootView:
    """
    Assembles the full app layout and handles global events.

    Parameters
    ----------
    page  : the Flet page
    state : shared AppState
    """

    def __init__(self, page: ft.Page, state: AppState):
        self.page  = page
        self.state = state

    # ── Public entry point — called from main.py ──────────────────
    def mount(self):
        """
        Clears the page and draws the full three-column layout.
        Called once on startup, and again after theme/nav changes.
        """
        page  = self.page
        state = self.state

        # ── Build the three columns ───────────────────────────────
        sidebar = Sidebar(
            is_dark=state.is_dark,
            selected_index=state.selected_nav,
            on_nav_change=self._on_nav_change,
            on_theme_toggle=self._on_theme_toggle,
        )

        # ChatView manages its own file picker overlay, so it needs
        # a reference to the page
        chat_view = ChatView(page=page, state=state)

        info_panel = InfoPanel(is_dark=state.is_dark)

        # ── Three-column root row ─────────────────────────────────
        root_row = ft.Row(
            controls=[sidebar, chat_view, info_panel],
            expand=True,
            spacing=0,
        )

        # ── Replace everything on the page ───────────────────────
        page.controls.clear()
        page.controls.append(
            ft.Container(
                content=root_row,
                expand=True,
                bgcolor=bg(state.is_dark),
            )
        )
        page.bgcolor = bg(state.is_dark)
        page.update()

    # ═══════════════════════════════════════════════════════════════
    #  GLOBAL EVENT HANDLERS
    # ═══════════════════════════════════════════════════════════════

    def _on_nav_change(self, index: int):
        """
        User clicked a sidebar nav item.
        Updates state, then re-mounts the layout so the active item
        highlight and the header breadcrumb both update.
        """
        self.state.selected_nav = index
        self.mount()

    def _on_theme_toggle(self, e):
        """
        User flipped the dark/light switch.
        Updates state + page theme, then re-mounts to repaint everything.
        """
        self.state.is_dark = e.control.value
        apply_page_theme(self.page, self.state.is_dark)
        self.mount()
