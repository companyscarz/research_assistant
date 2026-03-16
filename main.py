"""
AI Research Assistant — Flet Frontend (Flet 0.80+ compatible)
A modern multi-agent AI chat interface with simulated agent workflow.

To run:
    pip install flet
    python main.py

Future backend swap:
    Replace `simulate_api_request()` body with:
        import requests
        response = requests.post("http://localhost:5000/ask", json={"question": question})
        return response.json()
"""

import flet as ft
import time
import threading


# ─────────────────────────────────────────────
# DEMO API SIMULATION
# Replace this function body to connect to a real backend
# ─────────────────────────────────────────────

def simulate_api_request(question: str) -> dict:
    """
    Simulates a backend API call.
    Returns a dict with research, analysis, and final_answer keys.

    Future replacement:
        import requests
        response = requests.post("http://localhost:5000/ask", json={"question": question})
        return response.json()
    """
    q = question.lower()

    if any(w in q for w in ["renewable", "solar", "wind", "energy"]):
        return {
            "research": "Found 12 peer-reviewed sources on renewable energy. Key sources include IPCC reports, IEA data, and Nature Energy journals covering solar, wind, hydro, and geothermal technologies.",
            "analysis": "Cross-referencing sources reveals consistent findings: renewables now account for 30%+ of global electricity. Cost curves show exponential decreases — solar dropped 89% since 2010. Key challenge: grid intermittency and storage.",
            "final_answer": "Renewable energy refers to power derived from naturally replenishing sources such as sunlight, wind, rain, tides, and geothermal heat. Unlike fossil fuels, these resources are virtually inexhaustible on human timescales. Modern renewable technologies have seen dramatic cost reductions, making them the cheapest form of new electricity generation in most markets. The main engineering challenges involve grid stability, energy storage, and geographic distribution of resources.",
        }
    elif any(w in q for w in ["ai", "artificial intelligence", "machine learning", "neural"]):
        return {
            "research": "Surveyed 20+ sources including ArXiv preprints, Google DeepMind publications, and OpenAI technical reports. Identified key milestones: perceptrons (1958), backpropagation (1986), deep learning (2012), transformers (2017), LLMs (2020+).",
            "analysis": "The field has undergone three major paradigm shifts: symbolic AI → connectionism, shallow → deep networks, supervised → self-supervised learning. Current frontier models demonstrate emergent capabilities not present in smaller models.",
            "final_answer": "Artificial Intelligence is the simulation of human intelligence processes by machines. Modern AI is dominated by machine learning — systems that learn from data rather than following explicit rules. Deep learning, using multi-layered neural networks, has enabled breakthroughs in image recognition, natural language processing, and game-playing. Large Language Models represent the current frontier, capable of complex reasoning, code generation, and creative tasks.",
        }
    elif any(w in q for w in ["climate", "global warming", "carbon", "greenhouse"]):
        return {
            "research": "Compiled data from NASA GISS, NOAA, and IPCC AR6 report. Global average temperature has risen 1.1°C above pre-industrial levels. CO₂ concentration at 421 ppm — highest in 800,000 years.",
            "analysis": "Causal attribution studies show >97% scientific consensus that current warming is human-caused. Tipping points identified: Arctic sea ice loss, Amazon dieback, permafrost thaw create self-reinforcing feedback loops irreversible above 1.5–2°C.",
            "final_answer": "Climate change refers to long-term shifts in global temperatures and weather patterns. Since the Industrial Revolution, human activities — primarily burning fossil fuels — have been the main driver. The release of greenhouse gases traps solar heat in the atmosphere. Consequences include rising sea levels, more frequent extreme weather events, ecosystem disruption, and threats to food security. The Paris Agreement aims to limit warming to 1.5°C, requiring rapid decarbonization of the global economy by mid-century.",
        }
    else:
        return {
            "research": f"Searched academic databases, news archives, and expert sources for: '{question}'. Found relevant materials across multiple domains.",
            "analysis": f"Synthesizing gathered information on '{question}'. Identified key themes, conflicting perspectives, and areas of consensus among leading sources.",
            "final_answer": f"Based on comprehensive research into '{question}': This is a multifaceted topic with several important dimensions. The available evidence suggests a nuanced answer that depends on context, methodology, and the specific aspect being addressed. Further investigation with more specific parameters would yield more targeted insights.",
        }


# ─────────────────────────────────────────────
# MESSAGE BUILDER FUNCTIONS
# ─────────────────────────────────────────────

def build_user_message(text: str) -> ft.Container:
    """Right-aligned blue user chat bubble."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("You", size=11, color="#94a3b8",
                        weight=ft.FontWeight.W_500),
                ft.Text(text, color="white", size=14, selectable=True),
            ],
            spacing=4,
            tight=True,
        ),
        bgcolor="#1d4ed8",
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        border_radius=ft.BorderRadius.only(
            top_left=16, top_right=4, bottom_left=16, bottom_right=16
        ),
        margin=ft.Margin.only(left=80, bottom=8),
    )


def build_agent_message(agent_name: str, text: str) -> ft.Container:
    """Left-aligned agent chat bubble with per-agent accent color."""
    agent_colors = {
        "Research Agent": "#0ea5e9",
        "Analyst Agent":  "#a855f7",
        "Writer Agent":   "#f59e0b",
    }
    name_color = agent_colors.get(agent_name, "#94a3b8")

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(agent_name, size=11, color=name_color,
                        weight=ft.FontWeight.W_600),
                ft.Text(text, color="#cbd5e1", size=14, selectable=True),
            ],
            spacing=4,
            tight=True,
        ),
        bgcolor="#1e293b",
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        border_radius=ft.BorderRadius.only(
            top_left=4, top_right=16, bottom_left=16, bottom_right=16
        ),
        margin=ft.Margin.only(right=80, bottom=8),
        border=ft.Border.all(1, "#334155"),
    )


def build_final_answer_message(text: str) -> ft.Container:
    """Left-aligned green final answer bubble."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.AUTO_AWESOME,
                                color="#4ade80", size=14),
                        ft.Text(
                            "Final Answer",
                            size=11,
                            color="#4ade80",
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=4,
                    tight=True,
                ),
                ft.Text(text, color="#ecfdf5", size=15, selectable=True),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor="#052e16",
        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        border_radius=ft.BorderRadius.only(
            top_left=4, top_right=16, bottom_left=16, bottom_right=16
        ),
        margin=ft.Margin.only(right=40, bottom=8),
        border=ft.Border.all(1, "#166534"),
    )


def build_loading_indicator(agent_name: str) -> ft.Container:
    """Typing / loading indicator shown while an agent processes."""
    agent_colors = {
        "Research Agent": "#0ea5e9",
        "Analyst Agent":  "#a855f7",
        "Writer Agent":   "#f59e0b",
    }
    name_color = agent_colors.get(agent_name, "#94a3b8")

    return ft.Container(
        content=ft.Column(
            [
                ft.Text(agent_name, size=11, color=name_color,
                        weight=ft.FontWeight.W_600),
                ft.Row(
                    [
                        ft.ProgressRing(width=14, height=14,
                                        stroke_width=2, color=name_color),
                        ft.Text("Processing...", color="#64748b",
                                size=13, italic=True),
                    ],
                    spacing=8,
                    tight=True,
                ),
            ],
            spacing=4,
            tight=True,
        ),
        bgcolor="#1e293b",
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        border_radius=ft.BorderRadius.only(
            top_left=4, top_right=16, bottom_left=16, bottom_right=16
        ),
        margin=ft.Margin.only(right=80, bottom=8),
        border=ft.Border.all(1, "#334155"),
    )


def build_chip(label: str) -> ft.Container:
    """Small suggestion chip for the welcome screen."""
    return ft.Container(
        content=ft.Text(label, color="#64748b", size=12),
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        bgcolor="#1e293b",
        border_radius=20,
        border=ft.Border.all(1, "#334155"),
    )


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────

def main(page: ft.Page):
    # ── Page config ─────────────────────────
    page.title = "AI Research Assistant"
    page.bgcolor = "#0f172a"
    page.padding = 0
    page.window.icon = "assets/icon.png"  # Custom icon from assets/

    # ── Mutable state ────────────────────────
    is_processing = False

    # ── Header ──────────────────────────────
    header = ft.Container(
        content=ft.Row(
            [
                ft.Text("🤖", size=24),
                ft.Column(
                    [
                        ft.Text(
                            "AI Research Assistant",
                            color="white",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Multi-Agent AI Research System",
                            color="#475569",
                            size=12,
                        ),
                    ],
                    spacing=2,
                    tight=True,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(width=8, height=8,
                                         bgcolor="#4ade80", border_radius=4),
                            ft.Text("3 agents online",
                                    color="#4ade80", size=11),
                        ],
                        spacing=6,
                        tight=True,
                    ),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    bgcolor="#052e16",
                    border_radius=20,
                    border=ft.Border.all(1, "#166534"),
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=16),
        bgcolor="#0f172a",
        border=ft.Border.only(bottom=ft.BorderSide(1, "#1e293b")),
    )

    # ── Chat column ──────────────────────────
    chat_column = ft.Column(
        [],
        spacing=4,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        auto_scroll=True,
    )

    chat_area = ft.Container(
        content=chat_column,
        expand=True,
        padding=ft.Padding.symmetric(horizontal=24, vertical=16),
    )

    # ── Welcome placeholder ──────────────────
    welcome = ft.Container(
        content=ft.Column(
            [
                ft.Text("👋  Welcome", color="#94a3b8",
                        size=14, weight=ft.FontWeight.W_500),
                ft.Text(
                    "Ask any research question and watch three specialized AI agents\n"
                    "collaborate to deliver a comprehensive answer.",
                    color="#475569",
                    size=13,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Row(
                    [
                        build_chip("🌱  Renewable Energy"),
                        build_chip("🤖  Artificial Intelligence"),
                        build_chip("🌍  Climate Change"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                    spacing=8,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding.symmetric(horizontal=32, vertical=32),
        margin=ft.Margin.only(top=40, bottom=20),
        alignment=ft.Alignment.CENTER,
    )
    chat_column.controls.append(welcome)

    # ── Input field ──────────────────────────
    question_field = ft.TextField(
        hint_text="Ask a research question...",
        hint_style=ft.TextStyle(color="#334155"),
        text_style=ft.TextStyle(color="white", size=14),
        bgcolor="#1e293b",
        border_color="#334155",
        focused_border_color="#3b82f6",
        border_radius=12,
        expand=True,
        cursor_color="white",
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        shift_enter=False,
    )

    # ft.Button replaces deprecated ft.ElevatedButton in Flet 0.80+
    send_button = ft.Button(
        "Ask",
        style=ft.ButtonStyle(
            bgcolor={"": "#2563eb"},
            color={"": "white"},
            shape={"": ft.RoundedRectangleBorder(radius=10)},
            padding={"": ft.Padding.symmetric(horizontal=20, vertical=14)},
        ),
    )

    input_area = ft.Container(
        content=ft.Row(
            [question_field, send_button],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=24, vertical=16),
        bgcolor="#0f172a",
        border=ft.Border.only(top=ft.BorderSide(1, "#1e293b")),
    )

    # ── Helpers ──────────────────────────────

    def add_message(widget):
        """Append widget to chat and refresh UI."""
        chat_column.controls.append(widget)
        page.update()

    def remove_widget(widget):
        """Remove a widget from chat (e.g. loading spinner)."""
        if widget in chat_column.controls:
            chat_column.controls.remove(widget)

    # ── Agent workflow (background thread) ───

    def handle_submit(question: str):
        nonlocal is_processing
        if is_processing or not question.strip():
            return

        is_processing = True
        send_button.disabled = True
        question_field.value = ""
        page.update()

        # Remove welcome screen on first question
        if welcome in chat_column.controls:
            chat_column.controls.remove(welcome)

        # Step 1 — User message appears immediately
        add_message(build_user_message(question))

        # Call simulated (or real) API
        api_data = simulate_api_request(question)

        # Step 2 — Research Agent
        loader1 = build_loading_indicator("Research Agent")
        add_message(loader1)
        time.sleep(1.2)
        remove_widget(loader1)
        add_message(build_agent_message(
            "Research Agent", api_data["research"]))

        # Step 3 — Analyst Agent
        loader2 = build_loading_indicator("Analyst Agent")
        add_message(loader2)
        time.sleep(1.4)
        remove_widget(loader2)
        add_message(build_agent_message("Analyst Agent", api_data["analysis"]))

        # Step 4 — Writer Agent
        loader3 = build_loading_indicator("Writer Agent")
        add_message(loader3)
        time.sleep(1.0)
        remove_widget(loader3)
        add_message(build_agent_message("Writer Agent",
                    "Composing final answer from research synthesis..."))

        # Step 5 — Final Answer
        time.sleep(0.8)
        add_message(build_final_answer_message(api_data["final_answer"]))

        is_processing = False
        send_button.disabled = False
        page.update()

    # ── Event wiring ─────────────────────────

    def on_send_click(e):
        question = question_field.value.strip()
        if question:
            threading.Thread(target=handle_submit, args=(
                question,), daemon=True).start()

    send_button.on_click = on_send_click
    question_field.on_submit = on_send_click  # Enter key sends

    # ── Build page ───────────────────────────
    page.add(
        ft.Column(
            [header, chat_area, input_area],
            expand=True,
            spacing=0,
        )
    )


# ─────────────────────────────────────────────
# ENTRY POINT — Flet 0.80+ style
# ─────────────────────────────────────────────

ft.run(main, assets_dir="assets/", view=ft.WEB_BROWSER, port=8080)
