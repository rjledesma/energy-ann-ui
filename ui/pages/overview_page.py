import customtkinter as ctk

from ui.theme import BG, CARD, ACCENT, TEXT, MUTED, BORDER


def build_overview_page(app):
    page = ctk.CTkFrame(app.page_container, fg_color=BG)
    page.pack(fill="both", expand=True)

    ctk.CTkLabel(
        page,
        text="Project Overview",
        text_color=TEXT,
        font=ctk.CTkFont(size=42, weight="bold")
    ).pack(anchor="w", pady=(10, 8))

    ctk.CTkLabel(
        page,
        text="Renewable Energy Output Prediction Using Artificial Neural Networks",
        text_color=ACCENT,
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(anchor="w", pady=(0, 20))

    cards_frame = ctk.CTkFrame(page, fg_color=BG)
    cards_frame.pack(fill="both", expand=True)

    overview_items = [
        (
            "Main Goal",
            "Predict renewable and energy-related output using Artificial Neural Networks.",
            "The system predicts solar energy output from PVGIS data and building heating load from the UCI Energy Efficiency dataset."
        ),
        (
            "Datasets Used",
            "Two real datasets were used.",
            "Dataset 1: PVGIS-ERA5 Solar Data for Iloilo City. Dataset 2: UCI Energy Efficiency dataset for building heating load prediction."
        ),
        (
            "AI Technique",
            "Multilayer Artificial Neural Network.",
            "The ANN uses hidden layers with ReLU activation and a linear output layer for regression prediction."
        ),
        (
            "Evaluation",
            "Models were evaluated using RMSE, MAE, and R².",
            "The ANN was compared against Linear Regression as the baseline model."
        ),
    ]

    for index, (title, subtitle, body) in enumerate(overview_items):
        row = index // 2
        col = index % 2

        card = ctk.CTkFrame(
            cards_frame,
            fg_color=CARD,
            corner_radius=24,
            border_color=BORDER,
            border_width=1
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            card,
            text=title,
            text_color=TEXT,
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w", padx=22, pady=(22, 8))

        ctk.CTkLabel(
            card,
            text=subtitle,
            text_color=ACCENT,
            font=ctk.CTkFont(size=16, weight="bold"),
            wraplength=480,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 8))

        ctk.CTkLabel(
            card,
            text=body,
            text_color=MUTED,
            font=ctk.CTkFont(size=14),
            wraplength=520,
            justify="left"
        ).pack(anchor="w", padx=22, pady=(0, 22))

    cards_frame.grid_columnconfigure(0, weight=1)
    cards_frame.grid_columnconfigure(1, weight=1)
    cards_frame.grid_rowconfigure(0, weight=1)
    cards_frame.grid_rowconfigure(1, weight=1)