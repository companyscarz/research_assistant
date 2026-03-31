# LEXIS AI — Lawyer Assistant
### Built with the [Flet](https://flet.dev) framework · Python 3.11+

---

## Quick Start

```bash
# 1. Install Flet
pip install flet

# 2. Run as a desktop app
python main.py

# 3. Or run in your browser
flet run --web main.py
```

---

## Project Structure

```
lexis_ai/
│
├── main.py                   ← START HERE — run this file
│
├── utils/
│   ├── theme.py              ← ALL colours & theme helpers (edit this to rebrand)
│   └── state.py              ← Shared app data (is_dark, chat messages, nav index)
│
├── components/               ← Individual UI building blocks
│   ├── sidebar.py            ← Left nav with logo + nav items + theme toggle
│   ├── header_bar.py         ← Top breadcrumb bar
│   ├── chat_bubbles.py       ← UserBubble and AgentBubble
│   ├── input_console.py      ← Multiline text field + action buttons
│   └── info_panel.py         ← Right panel: case details, next steps, metrics
│
├── views/
│   ├── root_view.py          ← Assembles the three-column layout, handles global events
│   └── chat_view.py          ← Chat list + input logic + file picker events
│
└── services/
    ├── ai_service.py         ← AI/LLM logic (replace get_response() with real API)
    └── file_service.py       ← File upload, TTS, download placeholders
```

---

## How Data Flows

```
User action
    │
    ▼
views/chat_view.py  (event handlers: _on_submit, _on_tts, ...)
    │
    ├──▶ services/ai_service.py      (get AI response)
    ├──▶ services/file_service.py    (file pick / TTS / download)
    └──▶ utils/state.py              (save new ChatMessage)
              │
              ▼
         component.update()   (update only what changed)
```

---

## Common Customisations

### Change brand colours
Edit `utils/theme.py` → `Palette` class.
Every component automatically inherits the new values.

### Connect a real AI (e.g. OpenAI)
Open `services/ai_service.py` and replace the body of `get_response()`:

```python
import openai
client = openai.OpenAI(api_key="sk-...")

def get_response(query: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": query}]
    )
    return resp.choices[0].message.content
```

### Add a new nav section
1. Append `("Label", ft.icons.ICON_NAME)` to `NAV_ITEMS` in `components/sidebar.py`.
2. Add the matching label string to `nav_labels` in `utils/state.py`.
3. Optionally create a new view file in `views/` and render it in `views/root_view.py`
   based on `state.selected_nav`.

### Add a new right-panel card
Open `components/info_panel.py`, create a new `_my_card()` method using
the existing `_card()` helper, then add it to `_build()`.

### Add a new input action button
Open `components/input_console.py`, add an `icon_btn(...)` call to the
`action_bar` Row, and wire it to a new `on_*` parameter in `__init__`.

---

## Requirements

```
flet>=0.21.0
```
