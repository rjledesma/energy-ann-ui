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
    page = ctk.CTkFrame(app.page_container, fg_color=BG)
    page.grid(row=0, column=0, sticky="nsew")

    page.grid_columnconfigure(0, weight=1)
    page.grid_rowconfigure(0, weight=0)
    page.grid_rowconfigure(1, weight=1)
    page.grid_rowconfigure(2, weight=0)

    build_hero(app, page)
    build_main_section(app, page)
    build_metrics_section(app, page)


def build_hero(app, parent):
    hero = ctk.CTkFrame(parent, fg_color=BG)
    hero.grid(row=0, column=0, sticky="ew", pady=(0, 10))

    hero.grid_columnconfigure(0, weight=1)
    hero.grid_columnconfigure(1, weight=1)

    left = ctk.CTkFrame(hero, fg_color=BG)
    left.grid(row=0, column=0, sticky="w")

    ctk.CTkLabel(
        left,
        text="Here’s Your",
        text_color=ACCENT,
        font=ctk.CTkFont(size=40, weight="bold")
    ).pack(anchor="w")

    ctk.CTkLabel(
        left,
        text="Current Energy Overview",
        text_color=TEXT,
        font=ctk.CTkFont(size=40, weight="bold")
    ).pack(anchor="w")

    ctk.CTkLabel(
        left,
        text="Professional ANN-based energy prediction dashboard.",
        text_color=MUTED,
        font=ctk.CTkFont(size=16)
    ).pack(anchor="w")

    right = ctk.CTkFrame(
        hero,
        fg_color=WHITE,
        corner_radius=22,
        border_color=BORDER,
        border_width=1
    )
    right.grid(row=0, column=1, sticky="e")

    ctk.CTkLabel(
        right,
        text="Live Prediction Summary",
        text_color=TEXT,
        font=ctk.CTkFont(size=22, weight="bold")
    ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 4))

    app.summary_status = ctk.CTkLabel(
        right,
        text="System Ready",
        text_color=ACCENT,
        font=ctk.CTkFont(size=15, weight="bold")
    )
    app.summary_status.grid(row=1, column=0, sticky="w", padx=20)

    app.summary_text = ctk.CTkLabel(
        right,
        text="Select a dataset mode and enter values to predict.",
        text_color=MUTED,
        font=ctk.CTkFont(size=13),
        justify="left",
        wraplength=330
    )
    app.summary_text.grid(row=2, column=0, sticky="w", padx=20, pady=(8, 16))


def build_main_section(app, parent):
    main = ctk.CTkFrame(parent, fg_color=BG)
    main.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

    main.grid_columnconfigure(0, weight=0)
    main.grid_columnconfigure(1, weight=1)
    main.grid_rowconfigure(0, weight=1)

    build_input_card(app, main)
    build_result_panel(app, main)


def build_input_card(app, parent):
    app.input_card = ctk.CTkScrollableFrame(
        parent,
        fg_color=CARD,
        corner_radius=22,
        border_color=BORDER,
        border_width=1,
        width=500,
        scrollbar_button_color=ACCENT,
        scrollbar_button_hover_color=ACCENT_DARK
    )
    app.input_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    ctk.CTkLabel(
        app.input_card,
        text="Prediction Inputs",
        text_color=TEXT,
        font=ctk.CTkFont(size=25, weight="bold")
    ).pack(anchor="w", padx=22, pady=(18, 6))

    ctk.CTkLabel(
        app.input_card,
        text="Choose a model and enter the required feature values.",
        text_color=MUTED,
        font=ctk.CTkFont(size=13)
    ).pack(anchor="w", padx=22, pady=(0, 12))

    selector_frame = ctk.CTkFrame(app.input_card, fg_color=CARD)
    selector_frame.pack(fill="x", padx=18, pady=(0, 10))

    ctk.CTkLabel(
        selector_frame,
        text="Prediction Mode",
        text_color=TEXT,
        font=ctk.CTkFont(size=13, weight="bold")
    ).pack(anchor="w", pady=(0, 5))

    app.mode_selector = ctk.CTkOptionMenu(
        selector_frame,
        values=["PVGIS Solar Output", "UCI Heating Load"],
        command=app.on_mode_change,
        height=38,
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
    app.mode_selector.set("PVGIS Solar Output" if app.current_mode == "pvgis" else "UCI Heating Load")

    app.mode_description = ctk.CTkLabel(
        selector_frame,
        text=(
            "PVGIS mode predicts solar energy output in kWh from solar/weather inputs."
            if app.current_mode == "pvgis"
            else "UCI mode predicts building heating load from building design features."
        ),
        text_color=MUTED,
        font=ctk.CTkFont(size=10),
        wraplength=420,
        justify="left"
    )
    app.mode_description.pack(anchor="w", pady=(7, 0))

    app.form = ctk.CTkFrame(app.input_card, fg_color=CARD)
    app.form.pack(fill="x", padx=18, pady=(0, 8))

    app.build_dynamic_fields = lambda: build_dynamic_fields(app)
    app.update_metric_cards = lambda: update_metric_cards(app)

    build_dynamic_fields(app)

    button_frame = ctk.CTkFrame(app.input_card, fg_color=CARD)
    button_frame.pack(fill="x", padx=18, pady=(4, 18))

    buttons = [
        ("Predict Output", app.predict, ACCENT, "white"),
        ("Load Example", app.load_example, WHITE, TEXT),
        ("Clear", app.clear_inputs, WHITE, TEXT),
    ]

    for index, (text, command, color, text_color) in enumerate(buttons):
        ctk.CTkButton(
            button_frame,
            text=text,
            height=42,
            corner_radius=16,
            fg_color=color,
            hover_color=ACCENT_DARK if color == ACCENT else "#F1EEE8",
            text_color=text_color,
            border_width=0 if color == ACCENT else 1,
            border_color=BORDER,
            command=command
        ).grid(row=0, column=index, padx=4, sticky="ew")

    for col in range(3):
        button_frame.grid_columnconfigure(col, weight=1)


def build_dynamic_fields(app):
    for widget in app.form.winfo_children():
        widget.destroy()

    app.entries = {}

    if app.current_mode == "pvgis":
        fields = [
            ("h_sun", "Sun Height H_sun (degrees)", "0 - 90", "Solar elevation angle measured in degrees."),
            ("temperature", "Temperature T2m (°C)", "15 - 45", "Air temperature measured in degrees Celsius at 2 meters above ground."),
            ("wind_speed", "Wind Speed WS10m (m/s)", "0 - 20", "Wind speed measured in meters per second at 10 meters above ground."),
            ("hour", "Hour (0–23)", "0 - 23", "Hour of the day using 24-hour time."),
            ("month", "Month (1–12)", "1 - 12", "Month number of the year."),
            ("day_of_week", "Day of Week (0–6)", "0=Mon ... 6=Sun", "Numeric day of the week. 0 is Monday and 6 is Sunday."),
        ]
    else:
        fields = [
            ("relative_compactness", "Relative Compactness (unitless)", "0.5 - 1.0", "Unitless ratio describing how compact the building shape is."),
            ("surface_area", "Surface Area (m²)", "500 - 900", "Total external surface area measured in square meters."),
            ("wall_area", "Wall Area (m²)", "200 - 450", "Total wall area measured in square meters."),
            ("roof_area", "Roof Area (m²)", "100 - 250", "Roof surface area measured in square meters."),
            ("overall_height", "Overall Height (m)", "3.5 or 7.0", "Building height measured in meters."),
            ("orientation", "Orientation (category)", "2, 3, 4, or 5", "Categorical code for building orientation."),
            ("glazing_area", "Glazing Area (ratio)", "0 - 0.4", "Window/glass area ratio. Example: 0.25 means 25%."),
            ("glazing_area_distribution", "Glazing Area Distribution (category)", "0 - 5", "Categorical code for window placement distribution."),
        ]

    for row, (key, label, placeholder, description) in enumerate(fields):
        app.entries[key] = add_input(app.form, label, placeholder, row, description)


def build_result_panel(app, parent):
    right_panel = ctk.CTkFrame(parent, fg_color=BG)
    right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

    right_panel.grid_columnconfigure(0, weight=1)
    right_panel.grid_rowconfigure(0, weight=0)
    right_panel.grid_rowconfigure(1, weight=1)

    result_card = ctk.CTkFrame(
        right_panel,
        fg_color=WHITE,
        corner_radius=22,
        border_color=BORDER,
        border_width=1
    )
    result_card.grid(row=0, column=0, sticky="ew")

    app.result_title = ctk.CTkLabel(
        result_card,
        text="Solar Energy Output" if app.current_mode == "pvgis" else "Building Heating Load",
        text_color=TEXT,
        font=ctk.CTkFont(size=26, weight="bold")
    )
    app.result_title.grid(row=0, column=0, sticky="w", padx=22, pady=(20, 4))

    app.result_value = ctk.CTkLabel(
        result_card,
        text="0.0000 kWh" if app.current_mode == "pvgis" else "0.0000 HL",
        text_color=ACCENT,
        font=ctk.CTkFont(size=36, weight="bold")
    )
    app.result_value.grid(row=1, column=0, sticky="w", padx=22)

    app.result_desc = ctk.CTkLabel(
        result_card,
        text="Predict to see the estimated output.",
        text_color=MUTED,
        font=ctk.CTkFont(size=14),
        wraplength=650,
        justify="left"
    )
    app.result_desc.grid(row=2, column=0, sticky="w", padx=22, pady=(5, 10))

    app.energy_progress = ctk.CTkProgressBar(
        result_card,
        width=420,
        height=18,
        corner_radius=10,
        progress_color=ACCENT,
        fg_color="#E8E0D3"
    )
    app.energy_progress.grid(row=3, column=0, sticky="w", padx=22)
    app.energy_progress.set(0)

    app.percentage_label = ctk.CTkLabel(
        result_card,
        text="0%",
        text_color=TEXT,
        font=ctk.CTkFont(size=15, weight="bold")
    )
    app.percentage_label.grid(row=4, column=0, sticky="w", padx=22, pady=(3, 18))

    lower_cards = ctk.CTkFrame(right_panel, fg_color=BG)
    lower_cards.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

    lower_cards.grid_columnconfigure(0, weight=1)
    lower_cards.grid_columnconfigure(1, weight=1)
    lower_cards.grid_rowconfigure(0, weight=1)
    lower_cards.grid_rowconfigure(1, weight=1)

    app.card_current = create_info_card(lower_cards, "Current Prediction", "—", "Estimated output")
    app.card_current.grid(row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

    app.card_status = create_info_card(lower_cards, "Prediction Status", "Ready", "Model loaded successfully")
    app.card_status.grid(row=0, column=1, padx=(5, 0), pady=(0, 5), sticky="nsew")

    app.card_model = create_info_card(lower_cards, "Model Type", "ANN", "Multilayer perceptron")
    app.card_model.grid(row=1, column=0, padx=(0, 5), pady=(5, 0), sticky="nsew")

    dataset_name = "PVGIS-ERA5" if app.current_mode == "pvgis" else "UCI Energy"
    dataset_desc = "Solar output prediction" if app.current_mode == "pvgis" else "Heating load prediction"

    app.card_dataset = create_info_card(lower_cards, "Dataset", dataset_name, dataset_desc)
    app.card_dataset.grid(row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="nsew")


def build_metrics_section(app, parent):
    app.metrics = ctk.CTkFrame(parent, fg_color=BG)
    app.metrics.grid(row=2, column=0, sticky="ew")

    for col in range(4):
        app.metrics.grid_columnconfigure(col, weight=1)

    update_metric_cards(app)


def create_metric_card(parent, title, value, subtitle):
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=18,
        border_color=BORDER,
        border_width=1
    )

    card.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        card,
        text=title,
        text_color=TEXT,
        font=ctk.CTkFont(size=11, weight="bold")
    ).grid(row=0, column=0, sticky="w", padx=14, pady=(9, 0))

    ctk.CTkLabel(
        card,
        text=value,
        text_color=ACCENT,
        font=ctk.CTkFont(size=19, weight="bold")
    ).grid(row=1, column=0, sticky="w", padx=14, pady=(1, 0))

    ctk.CTkLabel(
        card,
        text=subtitle,
        text_color=MUTED,
        font=ctk.CTkFont(size=10)
    ).grid(row=2, column=0, sticky="w", padx=14, pady=(0, 9))

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

    for index, (title, value, subtitle) in enumerate(cards):
        card = create_metric_card(app.metrics, title, value, subtitle)
        card.grid(row=0, column=index, sticky="ew", padx=4)