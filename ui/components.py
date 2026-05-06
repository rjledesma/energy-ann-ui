import customtkinter as ctk

from ui.theme import CARD, WHITE, ACCENT, TEXT, MUTED, BORDER


def create_metric_card(parent, title, value, subtitle):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=22,
        border_color=BORDER,
        border_width=1,
        height=140
    )
    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text=title,
        text_color=TEXT,
        font=ctk.CTkFont(size=13, weight="bold")
    ).pack(anchor="w", padx=14, pady=(14, 4))

    ctk.CTkLabel(
        card,
        text=value,
        text_color=ACCENT,
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(anchor="w", padx=14, pady=(0, 2))

    ctk.CTkLabel(
        card,
        text=subtitle,
        text_color=MUTED,
        font=ctk.CTkFont(size=11),
        anchor="w",
        wraplength=180,
        justify="left"
    ).pack(anchor="w", padx=14, pady=(0, 10))

    return card


def create_info_card(parent, title, value, subtitle):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=24,
        border_color=BORDER,
        border_width=1,
        height=160
    )
    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text=title,
        text_color=TEXT,
        font=ctk.CTkFont(size=18, weight="bold")
    ).pack(anchor="w", padx=18, pady=(18, 8))

    value_label = ctk.CTkLabel(
        card,
        text=value,
        text_color=ACCENT,
        font=ctk.CTkFont(size=26, weight="bold")
    )
    value_label.pack(anchor="w", padx=18)

    subtitle_label = ctk.CTkLabel(
        card,
        text=subtitle,
        text_color=MUTED,
        font=ctk.CTkFont(size=12)
    )
    subtitle_label.pack(anchor="w", padx=18, pady=(4, 12))

    card.value_label = value_label
    card.subtitle_label = subtitle_label

    return card


def add_input(parent, label_text, placeholder, row):
    row_frame = ctk.CTkFrame(parent, fg_color=CARD)
    row_frame.grid(row=row, column=0, sticky="ew", pady=8)

    label = ctk.CTkLabel(
        row_frame,
        text=label_text,
        text_color=TEXT,
        font=ctk.CTkFont(size=14, weight="bold")
    )
    label.pack(anchor="w", pady=(0, 6))

    entry = ctk.CTkEntry(
        row_frame,
        height=42,
        corner_radius=14,
        fg_color=WHITE,
        border_color=BORDER,
        text_color=TEXT,
        placeholder_text=placeholder
    )
    entry.pack(fill="x")

    parent.grid_columnconfigure(0, weight=1)

    return entry