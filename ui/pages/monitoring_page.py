import customtkinter as ctk

from src.config import (
    PVGIS_ANN_RMSE,
    PVGIS_ANN_MAE,
    PVGIS_ANN_R2,
    PVGIS_LR_R2,
    UCI_ANN_RMSE,
    UCI_ANN_MAE,
    UCI_ANN_R2,
    UCI_LR_R2,
)

from ui.theme import BG, CARD, WHITE, ACCENT, ACCENT_DARK, TEXT, MUTED, BORDER
from ui.components import add_input, create_info_card


def build_monitoring_page(app):
    build_hero(app)
    build_main_section(app)
    build_metrics_section(app)


def build_hero(app):
    hero = ctk.CTkFrame(app.page_container, fg_color=BG)
    hero.pack(fill="x", pady=(0, 18))

    left = ctk.CTkFrame(hero, fg_color=BG)
    left.pack(side="left", fill="both", expand=True)

    ctk.CTkLabel(
        left,
        text="Here’s Your",
        text_color=ACCENT,
        font=ctk.CTkFont(size=44, weight="bold")
    ).pack(anchor="w")

    ctk.CTkLabel(
        left,
        text="Current Energy Overview",
        text_color=TEXT,
        font=ctk.CTkFont(size=44, weight="bold")
    ).pack(anchor="w", pady=(0, 10))

    ctk.CTkLabel(
        left,
        text="Professional ANN-based energy prediction dashboard.",
        text_color=MUTED,
        font=ctk.CTkFont(size=18)
    ).pack(anchor="w")

    right = ctk.CTkFrame(
        hero,
        fg_color=WHITE,
        corner_radius=24,
        border_color=BORDER,
        border_width=1,
        width=380,
        height=180
    )
    right.pack(side="right", padx=(20, 0))
    right.pack_propagate(False)

    ctk.CTkLabel(
        right,
        text="Live Prediction Summary",
        text_color=TEXT,
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(anchor="w", padx=20, pady=(20, 8))

    app.summary_status = ctk.CTkLabel(
        right,
        text="System Ready",
        text_color=ACCENT,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    app.summary_status.pack(anchor="w", padx=20)

    app.summary_text = ctk.CTkLabel(
        right,
        text="Select a dataset mode and enter values to predict.",
        text_color=MUTED,
        font=ctk.CTkFont(size=14),
        justify="left",
        wraplength=330
    )
    app.summary_text.pack(anchor="w", padx=20, pady=(10, 8))


def build_main_section(app):
    main = ctk.CTkFrame(app.page_container, fg_color=BG)
    main.pack(fill="both", expand=True, pady=(0, 8))

    build_input_card(app, main)
    build_result_panel(app, main)


def build_input_card(app, parent):
    app.input_card = ctk.CTkScrollableFrame(
        parent,
        fg_color=CARD,
        corner_radius=24,
        border_color=BORDER,
        border_width=1,
        width=500,
        scrollbar_button_color=ACCENT,
        scrollbar_button_hover_color=ACCENT_DARK
    )
    app.input_card.pack(side="left", fill="both", padx=(0, 12), expand=False)

    ctk.CTkLabel(
        app.input_card,
        text="Prediction Inputs",
        text_color=TEXT,
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(anchor="w", padx=24, pady=(24, 8))

    ctk.CTkLabel(
        app.input_card,
        text="Choose a model and enter the required feature values.",
        text_color=MUTED,
        font=ctk.CTkFont(size=14)
    ).pack(anchor="w", padx=24, pady=(0, 14))

    selector_frame = ctk.CTkFrame(app.input_card, fg_color=CARD)
    selector_frame.pack(fill="x", padx=20, pady=(0, 12))

    ctk.CTkLabel(
        selector_frame,
        text="Prediction Mode",
        text_color=TEXT,
        font=ctk.CTkFont(size=14, weight="bold")
    ).pack(anchor="w", pady=(0, 6))

    app.mode_selector = ctk.CTkOptionMenu(
        selector_frame,
        values=[
            "PVGIS Solar Output",
            "UCI Heating Load"
        ],
        command=app.on_mode_change,
        height=42,
        corner_radius=14,
        fg_color=WHITE,
        button_color=ACCENT,
        button_hover_color=ACCENT_DARK,
        text_color=TEXT,
        dropdown_fg_color=WHITE,
        dropdown_text_color=TEXT,
        dropdown_hover_color="#F1EEE8"
    )
    app.mode_selector.pack(fill="x")

    if app.current_mode == "pvgis":
        app.mode_selector.set("PVGIS Solar Output")
    else:
        app.mode_selector.set("UCI Heating Load")

    app.form = ctk.CTkFrame(app.input_card, fg_color=CARD)
    app.form.pack(fill="x", padx=20, pady=(0, 10))

    app.build_dynamic_fields = lambda: build_dynamic_fields(app)
    app.update_metric_cards = lambda: update_metric_cards(app)

    build_dynamic_fields(app)

    button_frame = ctk.CTkFrame(app.input_card, fg_color=CARD)
    button_frame.pack(fill="x", padx=20, pady=(4, 20))

    buttons = [
        ("Predict Output", app.predict, ACCENT, "white"),
        ("Load Example", app.load_example, WHITE, TEXT),
        ("Clear", app.clear_inputs, WHITE, TEXT),
    ]

    for index, (text, command, color, text_color) in enumerate(buttons):
        ctk.CTkButton(
            button_frame,
            text=text,
            height=46,
            corner_radius=18,
            fg_color=color,
            hover_color=ACCENT_DARK if color == ACCENT else "#F1EEE8",
            text_color=text_color,
            border_width=0 if color == ACCENT else 1,
            border_color=BORDER,
            command=command
        ).grid(row=0, column=index, padx=5, pady=6, sticky="ew")

    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)


def build_dynamic_fields(app):
    for widget in app.form.winfo_children():
        widget.destroy()

    app.entries = {}

    if app.current_mode == "pvgis":
        fields = [
            ("h_sun", "Sun Height H_sun", "0 - 90"),
            ("temperature", "Temperature T2m (°C)", "15 - 45"),
            ("wind_speed", "Wind Speed WS10m (m/s)", "0 - 20"),
            ("hour", "Hour", "0 - 23"),
            ("month", "Month", "1 - 12"),
            ("day_of_week", "Day of Week", "0=Mon ... 6=Sun"),
        ]
    else:
        fields = [
            ("relative_compactness", "Relative Compactness", "0.5 - 1.0"),
            ("surface_area", "Surface Area", "500 - 900"),
            ("wall_area", "Wall Area", "200 - 450"),
            ("roof_area", "Roof Area", "100 - 250"),
            ("overall_height", "Overall Height", "3.5 or 7.0"),
            ("orientation", "Orientation", "2, 3, 4, or 5"),
            ("glazing_area", "Glazing Area", "0 - 0.4"),
            ("glazing_area_distribution", "Glazing Area Distribution", "0 - 5"),
        ]

    for row, (key, label, placeholder) in enumerate(fields):
        app.entries[key] = add_input(app.form, label, placeholder, row)


def build_result_panel(app, parent):
    right_panel = ctk.CTkFrame(parent, fg_color=BG)
    right_panel.pack(side="left", fill="both", expand=True, padx=(12, 0))

    result_card = ctk.CTkFrame(
        right_panel,
        fg_color=WHITE,
        corner_radius=24,
        border_color=BORDER,
        border_width=1,
        height=250
    )
    result_card.pack(fill="x", pady=(0, 12))
    result_card.pack_propagate(False)

    app.result_title = ctk.CTkLabel(
        result_card,
        text="Solar Energy Output" if app.current_mode == "pvgis" else "Building Heating Load",
        text_color=TEXT,
        font=ctk.CTkFont(size=28, weight="bold")
    )
    app.result_title.pack(anchor="w", padx=24, pady=(24, 8))

    app.result_value = ctk.CTkLabel(
        result_card,
        text="0.0000 kWh" if app.current_mode == "pvgis" else "0.0000 HL",
        text_color=ACCENT,
        font=ctk.CTkFont(size=38, weight="bold")
    )
    app.result_value.pack(anchor="w", padx=24)

    app.result_desc = ctk.CTkLabel(
        result_card,
        text="Predict to see the estimated output.",
        text_color=MUTED,
        font=ctk.CTkFont(size=15),
        wraplength=650
    )
    app.result_desc.pack(anchor="w", padx=24, pady=(8, 16))

    app.energy_progress = ctk.CTkProgressBar(
        result_card,
        width=420,
        height=20,
        corner_radius=12,
        progress_color=ACCENT,
        fg_color="#E8E0D3"
    )
    app.energy_progress.pack(anchor="w", padx=24, pady=(0, 8))
    app.energy_progress.set(0)

    app.percentage_label = ctk.CTkLabel(
        result_card,
        text="0%",
        text_color=TEXT,
        font=ctk.CTkFont(size=16, weight="bold")
    )
    app.percentage_label.pack(anchor="w", padx=24)

    lower_cards = ctk.CTkFrame(right_panel, fg_color=BG)
    lower_cards.pack(fill="both", expand=True)

    app.card_current = create_info_card(
        lower_cards,
        "Current Prediction",
        "—",
        "Estimated output"
    )
    app.card_current.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

    app.card_status = create_info_card(
        lower_cards,
        "Prediction Status",
        "Ready",
        "Model loaded successfully"
    )
    app.card_status.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

    app.card_model = create_info_card(
        lower_cards,
        "Model Type",
        "ANN",
        "Multilayer perceptron"
    )
    app.card_model.grid(row=1, column=0, padx=6, pady=6, sticky="nsew")

    dataset_name = "PVGIS-ERA5" if app.current_mode == "pvgis" else "UCI Energy"
    dataset_desc = "Solar output prediction" if app.current_mode == "pvgis" else "Heating load prediction"

    app.card_dataset = create_info_card(
        lower_cards,
        "Dataset",
        dataset_name,
        dataset_desc
    )
    app.card_dataset.grid(row=1, column=1, padx=6, pady=6, sticky="nsew")

    lower_cards.grid_columnconfigure(0, weight=1)
    lower_cards.grid_columnconfigure(1, weight=1)
    lower_cards.grid_rowconfigure(0, weight=1)
    lower_cards.grid_rowconfigure(1, weight=1)

def create_metric_card(parent, title, value, subtitle):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=20,
        border_color=BORDER,
        border_width=1,
        height=95
    )
    card.pack_propagate(False)

    ctk.CTkLabel(
        card,
        text=title,
        text_color=TEXT,
        font=ctk.CTkFont(size=12, weight="bold"),
        anchor="w"
    ).pack(anchor="w", padx=14, pady=(12, 2))

    ctk.CTkLabel(
        card,
        text=value,
        text_color=ACCENT,
        font=ctk.CTkFont(size=20, weight="bold"),
        anchor="w"
    ).pack(anchor="w", padx=14, pady=(0, 2))

    ctk.CTkLabel(
        card,
        text=subtitle,
        text_color=MUTED,
        font=ctk.CTkFont(size=10),
        anchor="w",
        wraplength=180,
        justify="left"
    ).pack(anchor="w", padx=14, pady=(0, 8))

    return card


def update_metric_cards(app):
    for widget in app.metrics.winfo_children():
        widget.destroy()

    if app.current_mode == "pvgis":
        cards = [
            ("ANN RMSE", f"{PVGIS_ANN_RMSE:.4f}", "Solar model"),
            ("ANN MAE", f"{PVGIS_ANN_MAE:.4f}", "Average error"),
            ("ANN R²", f"{PVGIS_ANN_R2:.4f}", "ANN accuracy"),
            ("Baseline R²", f"{PVGIS_LR_R2:.4f}", "Linear Regression"),
        ]
    else:
        cards = [
            ("ANN RMSE", f"{UCI_ANN_RMSE:.4f}", "Heating load model"),
            ("ANN MAE", f"{UCI_ANN_MAE:.4f}", "Average error"),
            ("ANN R²", f"{UCI_ANN_R2:.4f}", "ANN accuracy"),
            ("Baseline R²", f"{UCI_LR_R2:.4f}", "Linear Regression"),
        ]

    for title, value, subtitle in cards:
        card = create_metric_card(app.metrics, title, value, subtitle)
        card.pack(side="left", fill="both", expand=True, padx=4)

def build_metrics_section(app):
    app.metrics = ctk.CTkFrame(app.page_container, fg_color=BG, height=105)
    app.metrics.pack(fill="x", pady=(16, 0))
    app.metrics.pack_propagate(False)

    update_metric_cards(app)