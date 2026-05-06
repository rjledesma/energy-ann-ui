import customtkinter as ctk
from src.interpretation import compare_models, generate_overall_interpretation

from src.config import (
    PVGIS_ANN_RMSE,
    PVGIS_ANN_MAE,
    PVGIS_ANN_R2,
    PVGIS_LR_RMSE,
    PVGIS_LR_MAE,
    PVGIS_LR_R2,
    UCI_ANN_RMSE,
    UCI_ANN_MAE,
    UCI_ANN_R2,
    UCI_LR_RMSE,
    UCI_LR_MAE,
    UCI_LR_R2,
)

from ui.theme import BG, CARD, WHITE, ACCENT, TEXT, MUTED, BORDER


def build_analytics_page(app):
    page = ctk.CTkFrame(app.page_container, fg_color=BG)
    page.pack(fill="both", expand=True)

    ctk.CTkLabel(
        page,
        text="Analytics",
        text_color=TEXT,
        font=ctk.CTkFont(size=42, weight="bold")
    ).pack(anchor="w", pady=(10, 8))

    ctk.CTkLabel(
        page,
        text="Model performance comparison across PVGIS and UCI datasets.",
        text_color=MUTED,
        font=ctk.CTkFont(size=18)
    ).pack(anchor="w", pady=(0, 18))

    table = ctk.CTkFrame(
        page,
        fg_color=WHITE,
        corner_radius=24,
        border_color=BORDER,
        border_width=1
    )
    table.pack(fill="x", pady=(0, 18))

    headers = ["Dataset", "Model", "RMSE", "MAE", "R²"]
    rows = [
        ["PVGIS Solar", "ANN", f"{PVGIS_ANN_RMSE:.4f}", f"{PVGIS_ANN_MAE:.4f}", f"{PVGIS_ANN_R2:.4f}"],
        ["PVGIS Solar", "Linear Regression", f"{PVGIS_LR_RMSE:.4f}", f"{PVGIS_LR_MAE:.4f}", f"{PVGIS_LR_R2:.4f}"],
        ["UCI Energy", "ANN", f"{UCI_ANN_RMSE:.4f}", f"{UCI_ANN_MAE:.4f}", f"{UCI_ANN_R2:.4f}"],
        ["UCI Energy", "Linear Regression", f"{UCI_LR_RMSE:.4f}", f"{UCI_LR_MAE:.4f}", f"{UCI_LR_R2:.4f}"],
    ]

    for col, header in enumerate(headers):
        ctk.CTkLabel(
            table,
            text=header,
            text_color=TEXT,
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=col, padx=16, pady=14, sticky="w")

    for row_index, row_data in enumerate(rows, start=1):
        for col_index, value in enumerate(row_data):
            ctk.CTkLabel(
                table,
                text=value,
                text_color=ACCENT if row_data[1] == "ANN" and col_index == 1 else TEXT,
                font=ctk.CTkFont(size=14)
            ).grid(row=row_index, column=col_index, padx=16, pady=12, sticky="w")

    for col in range(len(headers)):
        table.grid_columnconfigure(col, weight=1)

        pvgis_interpretation = compare_models(
        "PVGIS-ERA5 Solar",
        PVGIS_ANN_RMSE,
        PVGIS_ANN_MAE,
        PVGIS_ANN_R2,
        PVGIS_LR_RMSE,
        PVGIS_LR_MAE,
        PVGIS_LR_R2,
    )

    uci_interpretation = compare_models(
        "UCI Energy Efficiency",
        UCI_ANN_RMSE,
        UCI_ANN_MAE,
        UCI_ANN_R2,
        UCI_LR_RMSE,
        UCI_LR_MAE,
        UCI_LR_R2,
    )

    overall_interpretation = generate_overall_interpretation(
        pvgis_interpretation,
        uci_interpretation
    )

    explanation = ctk.CTkFrame(
        page,
        fg_color=CARD,
        corner_radius=24,
        border_color=BORDER,
        border_width=1
    )
    explanation.pack(fill="both", expand=True)

    ctk.CTkLabel(
        explanation,
        text=(
            pvgis_interpretation["summary"] + "\n\n" +
            uci_interpretation["summary"] + "\n\n" +
            overall_interpretation
        ),
        text_color=MUTED,
        font=ctk.CTkFont(size=16),
        wraplength=1000,
        justify="left"
    ).pack(anchor="w", padx=24, pady=(0, 24))

    ctk.CTkLabel(
        explanation,
        text=(
            "Lower RMSE and MAE values indicate smaller prediction errors, while a higher R² score "
            "means the model explains more variation in the target variable. In both datasets, the ANN "
            "achieved lower error values and higher R² scores compared with Linear Regression, showing "
            "that the neural network performed better overall."
        ),
        text_color=MUTED,
        font=ctk.CTkFont(size=16),
        wraplength=1000,
        justify="left"
    ).pack(anchor="w", padx=24, pady=(0, 24))