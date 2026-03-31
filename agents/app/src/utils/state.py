"""
utils/state.py
──────────────────────────────────────────────────────────────────────
AppState is the single source of truth for the whole application.

Think of it as a small "database in memory":
  • Every component reads data FROM here.
  • Every event handler writes changes TO here.
  • After a change, call page.update() (or a targeted control.update())
    to refresh the UI.

WHY THIS PATTERN?
  Instead of passing ten arguments into every component, we pass one
  `state` object.  When you need a new piece of shared data (e.g. the
  active case ID), just add it here — nothing else needs to change.
──────────────────────────────────────────────────────────────────────
"""

from dataclasses import dataclass, field
from datetime import datetime


# ── A single chat message ─────────────────────────────────────────
@dataclass
class ChatMessage:
    role:      str   # "user" or "agent"
    text:      str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M"))


# ── The whole app state ───────────────────────────────────────────
class AppState:
    """
    Holds every piece of shared state.

    USAGE in a component:
        class MyComponent(ft.Container):
            def __init__(self, state: AppState, ...):
                self.state = state
                # read:  self.state.is_dark
                # write: self.state.is_dark = True
    """

    def __init__(self):
        # Theme flag — True = dark mode (default)
        self.is_dark: bool = True

        # Which sidebar item is selected (0 = Dashboard)
        self.selected_nav: int = 0

        # Full chat history — list of ChatMessage objects
        self.messages: list[ChatMessage] = []

        # Navigation labels (index matches selected_nav)
        self.nav_labels: list[str] = [
            "Dashboard", "Cases", "Research", "Clients", "Settings"
        ]

        # Load a sample conversation so the app isn't empty on first run
        self._load_sample_messages()

    # ── Pre-load sample chat ──────────────────────────────────────
    def _load_sample_messages(self):
        samples = [
            ("user",
             "What are the key elements required to prove breach of "
             "fiduciary duty in a corporate context?"),
            ("agent",
             "To establish breach of fiduciary duty you must show four things:\n\n"
             "1. A fiduciary relationship existed (e.g. director → shareholder).\n"
             "2. The fiduciary breached that duty — acting in self-interest or "
             "failing the duty of loyalty / care (Business Judgment Rule applies).\n"
             "3. The breach caused the harm (causation).\n"
             "4. Quantifiable damages resulted.\n\n"
             "Key precedent: Smith v. Van Gorkom (Del. 1985) — directors held "
             "liable for gross negligence. Also review the Caremark standard for "
             "oversight failures."),
            ("user",
             "Can you draft an outline for a motion to compel discovery?"),
            ("agent",
             "Standard outline for a Motion to Compel Discovery:\n\n"
             "I.   INTRODUCTION — Relief sought + requests at issue.\n"
             "II.  FACTUAL BACKGROUND — Timeline of requests and non-responses.\n"
             "III. LEGAL STANDARD — Fed. R. Civ. P. 37(a); Rule 26(b)(1).\n"
             "IV.  ARGUMENT\n"
             "     A. Defendant failed to respond timely.\n"
             "     B. Objections are without merit.\n"
             "     C. Information is relevant and proportional.\n"
             "V.   CONCLUSION — Order to compel + sanctions under Rule 37(a)(5).\n\n"
             "Shall I draft the full motion for case CV-2025-04821?"),
        ]
        for role, text in samples:
            self.messages.append(ChatMessage(role=role, text=text))

    # ── Convenience helpers ───────────────────────────────────────
    def add_message(self, role: str, text: str) -> ChatMessage:
        """Append a new message and return it (so the UI can use it)."""
        msg = ChatMessage(role=role, text=text)
        self.messages.append(msg)
        return msg

    @property
    def current_section(self) -> str:
        """Return the label of the active navigation item."""
        return self.nav_labels[self.selected_nav]
