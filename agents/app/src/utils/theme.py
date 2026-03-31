"""
utils/theme.py
──────────────────────────────────────────────────────────────────────
All colour constants live here in one place.

HOW TO CUSTOMISE:
  • Change any hex value in Palette and every component that imports
    it will automatically pick up the new colour — no hunting needed.
  • To add a brand-new theme variant, just add another set of
    constants and update apply_page_theme() at the bottom.
──────────────────────────────────────────────────────────────────────
"""

import flet as ft


# ══════════════════════════════════════════════════════════════════════
#  PALETTE  — every colour the app uses
# ══════════════════════════════════════════════════════════════════════
class Palette:
    # ── Dark theme backgrounds ──────────────────────────────────
    DARK_BG      = "#0A0C14"   # page background
    DARK_SURFACE = "#111827"   # sidebar / header / panels
    DARK_CARD    = "#161D2F"   # elevated cards
    DARK_BORDER  = "#1E2D4A"   # dividers / outlines

    # ── Light theme backgrounds ─────────────────────────────────
    LIGHT_BG      = "#F0F4FF"
    LIGHT_SURFACE = "#FFFFFF"
    LIGHT_CARD    = "#EAF0FB"
    LIGHT_BORDER  = "#C5D3EE"

    # ── Accent colours ──────────────────────────────────────────
    NEON_BLUE     = "#00D4FF"   # primary brand accent
    NEON_BLUE_DIM = "#0A8FAD"   # muted version (hover states)
    GOLD          = "#C9A84C"   # avatar / secondary highlight

    # ── Text ────────────────────────────────────────────────────
    TEXT_PRIMARY_DARK   = "#E8EEFF"
    TEXT_SECONDARY_DARK = "#6B7FA3"
    TEXT_PRIMARY_LIGHT  = "#0D1B3E"
    TEXT_SECONDARY_LIGHT = "#5A6E99"

    # ── Status indicators ────────────────────────────────────────
    SUCCESS = "#22C55E"
    WARNING = "#F59E0B"
    DANGER  = "#EF4444"


# ══════════════════════════════════════════════════════════════════════
#  HELPER — pick the right colour based on is_dark flag
# ══════════════════════════════════════════════════════════════════════
def bg(is_dark: bool)         -> str: return Palette.DARK_BG      if is_dark else Palette.LIGHT_BG
def surface(is_dark: bool)    -> str: return Palette.DARK_SURFACE  if is_dark else Palette.LIGHT_SURFACE
def card(is_dark: bool)       -> str: return Palette.DARK_CARD     if is_dark else Palette.LIGHT_CARD
def border(is_dark: bool)     -> str: return Palette.DARK_BORDER   if is_dark else Palette.LIGHT_BORDER
def text_primary(is_dark: bool)   -> str: return Palette.TEXT_PRIMARY_DARK   if is_dark else Palette.TEXT_PRIMARY_LIGHT
def text_secondary(is_dark: bool) -> str: return Palette.TEXT_SECONDARY_DARK if is_dark else Palette.TEXT_SECONDARY_LIGHT


# ══════════════════════════════════════════════════════════════════════
#  apply_page_theme — called once on startup and again on toggle
# ══════════════════════════════════════════════════════════════════════
def apply_page_theme(page: ft.Page, is_dark: bool):
    """
    Sets the Flet page's theme_mode + color_scheme so built-in
    Flet widgets (TextField focus ring, Switch, etc.) also follow
    our brand colours.
    """
    page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
    page.bgcolor    = bg(is_dark)

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=Palette.NEON_BLUE,
            on_primary=Palette.DARK_BG,
            surface=surface(is_dark),
        )
    )
