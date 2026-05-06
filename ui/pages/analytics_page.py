import customtkinter as ctk

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

from src.interpretation import compare_models, generate_overall_interpretation
from ui.theme import BG, CARD, WHITE, ACCENT, TEXT, MUTED, BORDER


def build_analytics_page(app):
    page = ctk.CTkFrame(app.page_container, fg_color=BG)
    page.grid(row=0, column=0, sticky="nsew")
    page.grid_columnconfigure(0, weight=1)

    content = ctk.CTkFrame(page, fg_color=BG)
    content.grid(row=1, column=0, sticky="nsew")

    content.grid_columnconfigure(0, weight=1)
    content.grid_rowconfigure(0, weight=0)
    content.grid_rowconfigure(1, weight=0)
    content.grid_rowconfigure(2, weight=0)
    content.grid_rowconfigure(3, weight=1)

    ctk.CTkLabel(
        content,
        text="Analytics",
        text_color=TEXT,
        font=ctk.CTkFont(size=42, weight="bold")
    ).grid(row=0, column=0, sticky="w")

    ctk.CTkLabel(
        content,
        text="Model performance comparison across PVGIS and UCI datasets.",
        text_color=MUTED,
        font=ctk.CTkFont(size=18)
    ).grid(row=1, column=0, sticky="w", pady=(4, 18))

    table = ctk.CTkFrame(
        content,
        fg_color=WHITE,
        corner_radius=24,
        border_color=BORDER,
        border_width=1
    )
    table.grid(row=2, column=0, sticky="ew", pady=(0, 18))

    headers = ["Dataset", "Model", "RMSE", "MAE", "R²", "Unit"]
    rows = [
        [
            "PVGIS Solar",
            "ANN",
            f"{PVGIS_ANN_RMSE:.4f}",
            f"{PVGIS_ANN_MAE:.4f}",
            f"{PVGIS_ANN_R2:.4f}",
            "kWh"
        ],
        [
            "PVGIS Solar",
            "Linear Regression",
            f"{PVGIS_LR_RMSE:.4f}",
            f"{PVGIS_LR_MAE:.4f}",
            f"{PVGIS_LR_R2:.4f}",
            "kWh"
        ],
        [
            "UCI Energy",
            "ANN",
            f"{UCI_ANN_RMSE:.4f}",
            f"{UCI_ANN_MAE:.4f}",
            f"{UCI_ANN_R2:.4f}",
            "Heating Load"
        ],
        [
            "UCI Energy",
            "Linear Regression",
            f"{UCI_LR_RMSE:.4f}",
            f"{UCI_LR_MAE:.4f}",
            f"{UCI_LR_R2:.4f}",
            "Heating Load"
        ],
    ]

    for col, header in enumerate(headers):
        table.grid_columnconfigure(col, weight=1)

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

    explanation = ctk.CTkScrollableFrame(
        content,
        fg_color=CARD,
        corner_radius=24,
        border_color=BORDER,
        border_width=1
    )
    explanation.grid(row=3, column=0, sticky="nsew")

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

    ctk.CTkLabel(
        explanation,
        text="Results Interpretation",
        text_color=TEXT,
        font=ctk.CTkFont(size=28, weight="bold")
    ).pack(anchor="w", padx=24, pady=(24, 10))

    ctk.CTkLabel(
        explanation,
        text=(
            pvgis_interpretation["summary"] + "\n\n" +
            uci_interpretation["summary"] + "\n\n" +
            overall_interpretation
        ),
        text_color=MUTED,
        font=ctk.CTkFont(size=16),
        wraplength=1100,
        justify="left"
    ).pack(anchor="w", padx=24, pady=(0, 18))

    ctk.CTkLabel(
        explanation,
        text="Metric Units",
        text_color=TEXT,
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(anchor="w", padx=24, pady=(4, 8))

    ctk.CTkLabel(
        explanation,
        text=(
            "PVGIS Solar Output: RMSE and MAE are measured in kWh because the target is estimated solar energy output.\n\n"
            "UCI Heating Load: RMSE and MAE are measured in Heating Load units because the target is building heating load.\n\n"
            "R² is unitless for both datasets. Lower RMSE and MAE are better, while higher R² is better."
        ),
        text_color=MUTED,
        font=ctk.CTkFont(size=15),
        wraplength=1100,
        justify="left"
    ).pack(anchor="w", padx=24, pady=(0, 24))