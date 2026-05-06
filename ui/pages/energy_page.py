import customtkinter as ctk

from ui.theme import BG, CARD, ACCENT, TEXT, MUTED, BORDER, ACCENT_DARK


def build_energy_page(app):
    page = ctk.CTkFrame(app.page_container, fg_color=BG)
    page.grid(row=0, column=0, sticky="nsew")

    page.grid_columnconfigure(0, weight=1)
    page.grid_rowconfigure(0, weight=0)  # title
    page.grid_rowconfigure(1, weight=0)  # subtitle
    page.grid_rowconfigure(2, weight=1)  # content expands

    ctk.CTkLabel(
        page,
        text="Energy Model Details",
        text_color=TEXT,
        font=ctk.CTkFont(size=42, weight="bold")
    ).grid(row=0, column=0, sticky="w")

    ctk.CTkLabel(
        page,
        text="Dataset features, ANN architecture, and training setup.",
        text_color=MUTED,
        font=ctk.CTkFont(size=18)
    ).grid(row=1, column=0, sticky="w", pady=(4, 14))

    content = ctk.CTkScrollableFrame(
        page,
        fg_color=BG,
        scrollbar_button_color=ACCENT,
        scrollbar_button_hover_color=ACCENT_DARK
    )
    content.grid(row=2, column=0, sticky="nsew")

    content.grid_columnconfigure(0, weight=1)
    content.grid_columnconfigure(1, weight=1)

    sections = [
        (
            "PVGIS Solar Output Model",
            (
                "Dataset: PVGIS-ERA5 Solar Data for Iloilo City\n\n"
                "Features:\n"
                "• H_sun — sun height / solar elevation angle in degrees\n"
                "• T2m — air temperature at 2 meters in °C\n"
                "• WS10m — wind speed at 10 meters in m/s\n"
                "• hour — hour of the day from 0 to 23\n"
                "• month — month number from 1 to 12\n"
                "• day_of_week — Monday = 0, Sunday = 6\n\n"
                "Target: Estimated solar energy output in kWh\n"
                "Split: 2022 for training/validation, 2023 for testing"
            )
        ),
        (
            "UCI Heating Load Model",
            (
                "Dataset: UCI Energy Efficiency Dataset\n\n"
                "Features:\n"
                "• relative_compactness — unitless building compactness ratio\n"
                "• surface_area — total external surface area in m²\n"
                "• wall_area — wall area in m²\n"
                "• roof_area — roof area in m²\n"
                "• overall_height — building height in meters\n"
                "• orientation — orientation category\n"
                "• glazing_area — window/glass area ratio\n"
                "• glazing_area_distribution — glazing placement category\n\n"
                "Target: Heating Load\n"
                "Split: 70% training, 15% validation, 15% testing"
            )
        ),
        (
            "ANN Architecture",
            (
                "Input Layer: depends on dataset feature count\n"
                "Hidden Layer 1: 10 neurons, ReLU activation\n"
                "Hidden Layer 2: 8 neurons, ReLU activation\n"
                "Output Layer: 1 neuron, linear activation\n\n"
                "Loss Function: Mean Squared Error\n"
                "Optimizer: Adam\n"
                "Batch Size: 32\n"
                "Early Stopping: patience of 10"
            )
        ),
        (
            "Backpropagation",
            (
                "The ANN learns by performing a forward pass to generate predictions, "
                "calculating the prediction error using MSE, and then applying "
                "backpropagation to update the weights. This process repeats over "
                "multiple epochs until the validation loss stops improving."
            )
        ),
    ]

    for index, (title, body) in enumerate(sections):
        row = index // 2
        col = index % 2

        card = ctk.CTkFrame(
            content,
            fg_color=CARD,
            corner_radius=24,
            border_color=BORDER,
            border_width=1
        )
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=title,
            text_color=TEXT,
            font=ctk.CTkFont(size=23, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(20, 8))

        ctk.CTkLabel(
            card,
            text=body,
            text_color=MUTED,
            font=ctk.CTkFont(size=14),
            wraplength=500,
            justify="left"
        ).grid(row=1, column=0, sticky="nw", padx=22, pady=(0, 20))

    content.grid_rowconfigure(0, weight=1)
    content.grid_rowconfigure(1, weight=1)