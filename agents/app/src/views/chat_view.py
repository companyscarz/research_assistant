"""
views/chat_view.py
──────────────────────────────────────────────────────────────────────
The central chat workspace: header + scrollable message list + input.

This view owns:
  • HeaderBar    (top bar with breadcrumb)
  • ListView     (the scrollable chat history)
  • InputConsole (bottom text input + action buttons)

It also handles all chat-related events:
  • on_submit  — sends a message and gets an AI response
  • on_tts     — placeholder text-to-speech
  • on_dl_text — placeholder download text
  • on_dl_audio— placeholder download audio
  • on_record  — placeholder audio record
  • on_attach  — opens media file picker
  • on_upload  — opens document file picker

EVENT FLOW (simplified):
  user types → clicks Submit
    → ChatView.on_submit()
      → adds UserBubble to ListView
      → calls ai_service.get_response()
      → adds AgentBubble to ListView
──────────────────────────────────────────────────────────────────────
"""

import flet as ft

from utils.state  import AppState, ChatMessage
from utils.theme  import bg

from components.header_bar    import HeaderBar
from components.chat_bubbles  import UserBubble, AgentBubble
from components.input_console import InputConsole

from services import ai_service, file_service


class ChatView(ft.Column):
    """
    The main centre panel.

    Parameters
    ----------
    page  : the Flet page (needed to show snackbars + add file picker)
    state : shared AppState object
    """

    def __init__(self, page: ft.Page, state: AppState):
        self.page  = page
        self.state = state

        # Set up file picker and register it with the page overlay
        self.file_picker = file_service.create_file_picker(
            on_result=self._on_file_picked
        )
        page.overlay.append(self.file_picker)

        # Build the ListView first (we reference it in build())
        self.chat_list = self._build_chat_list()

        # Build the input console
        self.input_console = InputConsole(
            is_dark=state.is_dark,
            on_submit=self._on_submit,
            on_record=self._on_record,
            on_attach=self._on_attach,
            on_upload=self._on_upload,
        )

        super().__init__(
            controls=[
                HeaderBar(
                    is_dark=state.is_dark,
                    section_name=state.current_section,
                ),
                ft.Container(
                    content=self.chat_list,
                    expand=True,
                    bgcolor=bg(state.is_dark),
                ),
                self.input_console,
            ],
            expand=True,
            spacing=0,
        )

    # ── Build the scrollable chat list ────────────────────────────
    def _build_chat_list(self) -> ft.ListView:
        """
        Creates a ListView pre-populated with all messages in state.
        auto_scroll=True means it always jumps to the latest message.
        """
        controls = [ft.Container(height=8)]

        for msg in self.state.messages:
            controls.append(self._bubble_from_message(msg))

        controls.append(ft.Container(height=8))

        return ft.ListView(
            controls=controls,
            expand=True,
            padding=ft.padding.symmetric(horizontal=16, vertical=0),
            auto_scroll=True,
            spacing=2,
        )

    # ── Build the correct bubble type from a ChatMessage ─────────
    def _bubble_from_message(self, msg: ChatMessage) -> ft.Control:
        if msg.role == "user":
            return UserBubble(
                text=msg.text,
                timestamp=msg.timestamp,
                is_dark=self.state.is_dark,
            )
        else:
            return AgentBubble(
                text=msg.text,
                timestamp=msg.timestamp,
                is_dark=self.state.is_dark,
                on_tts=self._on_tts,
                on_dl_text=self._on_dl_text,
                on_dl_audio=self._on_dl_audio,
            )

    # ── Append a new bubble without rebuilding the whole list ─────
    def _append_bubble(self, msg: ChatMessage):
        """
        Inserts a new bubble before the trailing spacer at index -1.
        This is more efficient than rebuilding the entire ListView.
        """
        self.chat_list.controls.insert(-1, self._bubble_from_message(msg))
        self.chat_list.update()

    # ═══════════════════════════════════════════════════════════════
    #  EVENT HANDLERS
    # ═══════════════════════════════════════════════════════════════

    def _on_submit(self, e):
        """User clicked Submit — add message, get AI response."""
        text = self.input_console.text_field.value.strip()
        if not text:
            return

        # 1. Save to state and clear the input field
        user_msg = self.state.add_message("user", text)
        self.input_console.text_field.value = ""
        self.input_console.text_field.update()

        # 2. Show the user bubble immediately
        self._append_bubble(user_msg)

        # 3. Get an AI response (replace ai_service.get_response with
        #    your real API call — only this one line needs to change)
        ai_text = ai_service.get_response(text)
        ai_msg  = self.state.add_message("agent", ai_text)

        # 4. Show the agent bubble
        self._append_bubble(ai_msg)

    def _on_tts(self, e):
        """Play text-to-speech for the agent message."""
        file_service.play_tts(e.control.data)
        self._snack("🔊  Text-to-Speech playback starting…", "blue")

    def _on_dl_text(self, e):
        """Download the agent response as a .txt file."""
        file_service.download_as_text(e.control.data)
        self._snack("⬇  Downloading response as text file…", "blue")

    def _on_dl_audio(self, e):
        """Download the agent response as an audio file."""
        file_service.download_as_audio(e.control.data)
        self._snack("⬇  Generating and downloading audio file…", "blue")

    def _on_record(self, e):
        """Start audio recording (placeholder)."""
        self._snack("🎤  Recording started — speak your query…", "red")

    def _on_attach(self, e):
        """Open media file picker."""
        file_service.open_media_picker(self.file_picker)

    def _on_upload(self, e):
        """Open document file picker."""
        file_service.open_document_picker(self.file_picker)

    def _on_file_picked(self, e: ft.FilePickerResultEvent):
        """Handle result from the file picker dialog."""
        names = file_service.handle_upload_result(e)
        if names:
            self._snack(f"📎  Uploading: {names}", "green")
        else:
            self._snack("No file selected.", "grey")

    # ── Snackbar helper ───────────────────────────────────────────
    def _snack(self, message: str, color_key: str):
        """Show a short notification at the bottom of the screen."""
        color_map = {
            "blue":  "#00D4FF",
            "green": "#22C55E",
            "red":   "#EF4444",
            "grey":  "#6B7FA3",
        }
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=ft.colors.with_opacity(0.9, color_map.get(color_key, "#00D4FF")),
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()
