import customtkinter as ctk

from ui.theme import CARD, WHITE, ACCENT, TEXT, MUTED, BORDER


def add_input(parent, label_text, placeholder, row, description=None):
    row_frame = ctk.CTkFrame(parent, fg_color=CARD)
    row_frame.grid(row=row, column=0, sticky="ew", pady=7)

    row_frame.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        row_frame,
        text=label_text,
        text_color=TEXT,
        font=ctk.CTkFont(size=13, weight="bold"),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", pady=(0, 3))

    if description:
        ctk.CTkLabel(
            row_frame,
            text=description,
            text_color=MUTED,
            font=ctk.CTkFont(size=10),
            wraplength=420,
            justify="left",
            anchor="w"
        ).grid(row=1, column=0, sticky="ew", pady=(0, 5))

    entry = ctk.CTkEntry(
        row_frame,
        height=38,
        corner_radius=14,
        fg_color=WHITE,
        border_color=BORDER,
        text_color=TEXT,
        placeholder_text=placeholder
    )
    entry.grid(row=2, column=0, sticky="ew")

    parent.grid_columnconfigure(0, weight=1)

    return entry


def create_info_card(parent, title, value, subtitle):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=22,
        border_color=BORDER,
        border_width=1
    )

    card.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        card,
        text=title,
        text_color=TEXT,
        font=ctk.CTkFont(size=16, weight="bold"),
        anchor="w"
    ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 4))

    value_label = ctk.CTkLabel(
        card,
        text=value,
        text_color=ACCENT,
        font=ctk.CTkFont(size=24, weight="bold"),
        anchor="w"
    )
    value_label.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 2))

    subtitle_label = ctk.CTkLabel(
        card,
        text=subtitle,
        text_color=MUTED,
        font=ctk.CTkFont(size=11),
        wraplength=260,
        justify="left",
        anchor="w"
    )
    subtitle_label.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 14))

    card.value_label = value_label
    card.subtitle_label = subtitle_label

    return card