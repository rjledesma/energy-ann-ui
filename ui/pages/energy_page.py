import customtkinter as ctk

from ui.theme import BG, CARD, ACCENT, TEXT, MUTED, BORDER, ACCENT_DARK


def build_energy_page(app):
    page = ctk.CTkFrame(app.page_container, fg_color=BG)
    page.pack(fill="both", expand=True)

    ctk.CTkLabel(
        page,
        text="Energy Model Details",
        text_color=TEXT,
        font=ctk.CTkFont(size=42, weight="bold")
    ).pack(anchor="w", pady=(10, 8))

    ctk.CTkLabel(
        page,
        text="Dataset features, ANN architecture, and training setup.",
        text_color=MUTED,
        font=ctk.CTkFont(size=18)
    ).pack(anchor="w", pady=(0, 18))

    content = ctk.CTkScrollableFrame(
        page,
        fg_color=BG,
        scrollbar_button_color=ACCENT,
        scrollbar_button_hover_color=ACCENT_DARK
    )
    content.pack(fill="both", expand=True)

    sections = [
        (
            "PVGIS Solar Output Model",
            (
                "Dataset: PVGIS-ERA5 Solar Data for Iloilo City\n"
                "Features: H_sun, T2m, WS10m, hour, month, day_of_week\n"
                "Target: Estimated solar energy output in kWh\n"
                "Split: 2022 for training/validation, 2023 for testing"
            )
        ),
        (
            "UCI Heating Load Model",
            (
                "Dataset: UCI Energy Efficiency Dataset\n"
                "Features: relative compactness, surface area, wall area, roof area, overall height, "
                "orientation, glazing area, glazing area distribution\n"
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
                "Output Layer: 1 neuron, linear activation\n"
                "Loss Function: Mean Squared Error\n"
                "Optimizer: Adam\n"
                "Batch Size: 32\n"
                "Early Stopping: patience of 10"
            )
        ),
        (
            "Backpropagation",
            (
                "The ANN learns by performing a forward pass to generate predictions, calculating error "
                "using MSE, and then applying backpropagation to update the weights. This process repeats "
                "over multiple epochs until validation loss stops improving."
            )
        ),
    ]

    for title, body in sections:
        card = ctk.CTkFrame(
            content,
            fg_color=CARD,
            corner_radius=24,
            border_color=BORDER,
            border_width=1
        )
        card.pack(fill="x", padx=4, pady=10)

        ctk.CTkLabel(
            card,
            text=title,
            text_color=TEXT,
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w", padx=24, pady=(22, 8))

        ctk.CTkLabel(
            card,
            text=body,
            text_color=MUTED,
            font=ctk.CTkFont(size=15),
            wraplength=1000,
            justify="left"
        ).pack(anchor="w", padx=24, pady=(0, 22))