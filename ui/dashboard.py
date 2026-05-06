from tkinter import messagebox
import customtkinter as ctk

from src.config import (
    APP_TITLE,
    WINDOW_SIZE,
    MIN_WIDTH,
    MIN_HEIGHT,
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

from src.model_loader import load_all_models_and_artifacts
from src.predictor import (
    predict_from_model,
    get_solar_status,
    get_heating_status,
    get_energy_percentage,
)
from src.validation import validate_pvgis_inputs, validate_uci_inputs

from ui.theme import BG, CARD, WHITE, ACCENT, ACCENT_DARK, TEXT, MUTED, BORDER
from ui.components import add_input, create_info_card


class EnergyDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.models = load_all_models_and_artifacts()
        self.current_mode = "pvgis"
        self.entries = {}

        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.configure(fg_color=BG)
        self.minsize(MIN_WIDTH, MIN_HEIGHT)

        self.build_ui()

    def build_ui(self):
        self.wrapper = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.wrapper.pack(fill="both", expand=True, padx=24, pady=20)

        self.build_navbar()
        self.build_hero()
        self.build_main_section()
        self.build_metrics_section()

    # Navbar

    def build_navbar(self):
        nav = ctk.CTkFrame(self.wrapper, fg_color=BG)
        nav.pack(fill="x", pady=(0, 16))

        brand = ctk.CTkLabel(
            nav,
            text="☀ ENERGY AI",
            text_color=TEXT,
            font=ctk.CTkFont(size=22, weight="bold")
        )
        brand.pack(side="left", padx=(8, 0))

        center_frame = ctk.CTkFrame(nav, fg_color=BG)
        center_frame.pack(side="left", expand=True)

        nav_items = [
            ("Overview", False),
            ("Monitoring", True),
            ("Analytics", False),
            ("Energy", False),
        ]

        for text, active in nav_items:
            btn = ctk.CTkButton(
                center_frame,
                text=text,
                width=120,
                height=40,
                corner_radius=20,
                fg_color=ACCENT if active else WHITE,
                hover_color=ACCENT_DARK if active else "#F2F2F2",
                text_color="white" if active else "#555555",
                border_width=0
            )
            btn.pack(side="left", padx=8)

        right_frame = ctk.CTkFrame(nav, fg_color=BG)
        right_frame.pack(side="right")

        for icon in ["🔔", "👤"]:
            ctk.CTkButton(
                right_frame,
                text=icon,
                width=40,
                height=40,
                corner_radius=20,
                fg_color=WHITE,
                text_color=TEXT,
                hover_color="#F4F1EB"
            ).pack(side="left", padx=6)

    # Hero

    def build_hero(self):
        hero = ctk.CTkFrame(self.wrapper, fg_color=BG)
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

        self.summary_status = ctk.CTkLabel(
            right,
            text="System Ready",
            text_color=ACCENT,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.summary_status.pack(anchor="w", padx=20)

        self.summary_text = ctk.CTkLabel(
            right,
            text="Select a dataset mode and enter values to predict.",
            text_color=MUTED,
            font=ctk.CTkFont(size=14),
            justify="left",
            wraplength=330
        )
        self.summary_text.pack(anchor="w", padx=20, pady=(10, 8))

    # Main Section

    def build_main_section(self):
        main = ctk.CTkFrame(self.wrapper, fg_color=BG)
        main.pack(fill="both", expand=True)

        self.build_input_card(main)
        self.build_result_panel(main)

    def build_input_card(self, parent):
        self.input_card = ctk.CTkScrollableFrame(
            parent,
            fg_color=CARD,
            corner_radius=24,
            border_color=BORDER,
            border_width=1,
            width=500,
            scrollbar_button_color=ACCENT,
            scrollbar_button_hover_color=ACCENT_DARK
        )
        self.input_card.pack(side="left", fill="both", padx=(0, 12), expand=False)

        ctk.CTkLabel(
            self.input_card,
            text="Prediction Inputs",
            text_color=TEXT,
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            self.input_card,
            text="Choose a model and enter the required feature values.",
            text_color=MUTED,
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=24, pady=(0, 14))

        selector_frame = ctk.CTkFrame(self.input_card, fg_color=CARD)
        selector_frame.pack(fill="x", padx=20, pady=(0, 12))

        ctk.CTkLabel(
            selector_frame,
            text="Prediction Mode",
            text_color=TEXT,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(0, 6))

        self.mode_selector = ctk.CTkOptionMenu(
            selector_frame,
            values=[
                "PVGIS Solar Output",
                "UCI Heating Load"
            ],
            command=self.on_mode_change,
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
        self.mode_selector.pack(fill="x")
        self.mode_selector.set("PVGIS Solar Output")

        self.form = ctk.CTkScrollableFrame(
            self.input_card,
            fg_color=CARD,
            height=360,
            scrollbar_button_color=ACCENT,
            scrollbar_button_hover_color=ACCENT_DARK
        )
        self.form.pack(fill="x", padx=20, pady=(0, 10))

        self.build_dynamic_fields()

        button_frame = ctk.CTkFrame(self.input_card, fg_color=CARD)
        button_frame.pack(fill="x", padx=20, pady=(4, 16))

        buttons = [
            ("Predict Output", self.predict, ACCENT, "white"),
            ("Load Example", self.load_example, WHITE, TEXT),
            ("Clear", self.clear_inputs, WHITE, TEXT),
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

    def build_dynamic_fields(self):
        for widget in self.form.winfo_children():
            widget.destroy()

        self.entries = {}

        if self.current_mode == "pvgis":
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
            self.entries[key] = add_input(self.form, label, placeholder, row)

    # Result Panel

    def build_result_panel(self, parent):
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

        self.result_title = ctk.CTkLabel(
            result_card,
            text="Solar Energy Output",
            text_color=TEXT,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.result_title.pack(anchor="w", padx=24, pady=(24, 8))

        self.result_value = ctk.CTkLabel(
            result_card,
            text="0.0000 kWh",
            text_color=ACCENT,
            font=ctk.CTkFont(size=38, weight="bold")
        )
        self.result_value.pack(anchor="w", padx=24)

        self.result_desc = ctk.CTkLabel(
            result_card,
            text="Predict to see the estimated output.",
            text_color=MUTED,
            font=ctk.CTkFont(size=15),
            wraplength=650
        )
        self.result_desc.pack(anchor="w", padx=24, pady=(8, 16))

        self.energy_progress = ctk.CTkProgressBar(
            result_card,
            width=420,
            height=20,
            corner_radius=12,
            progress_color=ACCENT,
            fg_color="#E8E0D3"
        )
        self.energy_progress.pack(anchor="w", padx=24, pady=(0, 8))
        self.energy_progress.set(0)

        self.percentage_label = ctk.CTkLabel(
            result_card,
            text="0%",
            text_color=TEXT,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.percentage_label.pack(anchor="w", padx=24)

        lower_cards = ctk.CTkFrame(right_panel, fg_color=BG)
        lower_cards.pack(fill="both", expand=True)

        self.card_current = create_info_card(
            lower_cards,
            "Current Prediction",
            "—",
            "Estimated output"
        )
        self.card_current.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        self.card_status = create_info_card(
            lower_cards,
            "Prediction Status",
            "Ready",
            "Model loaded successfully"
        )
        self.card_status.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

        self.card_model = create_info_card(
            lower_cards,
            "Model Type",
            "ANN",
            "Multilayer perceptron"
        )
        self.card_model.grid(row=1, column=0, padx=6, pady=6, sticky="nsew")

        self.card_dataset = create_info_card(
            lower_cards,
            "Dataset",
            "PVGIS-ERA5",
            "Solar output prediction"
        )
        self.card_dataset.grid(row=1, column=1, padx=6, pady=6, sticky="nsew")

        lower_cards.grid_columnconfigure(0, weight=1)
        lower_cards.grid_columnconfigure(1, weight=1)
        lower_cards.grid_rowconfigure(0, weight=1)
        lower_cards.grid_rowconfigure(1, weight=1)

    # Metrics Section

    def build_metrics_section(self):
        self.metrics = ctk.CTkFrame(self.wrapper, fg_color=BG)
        self.metrics.pack(fill="x", pady=(16, 0))
        self.metric_cards = []
        self.update_metric_cards()

    def create_metric_card(self, parent, title, value, subtitle):
        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=22,
            border_color=BORDER,
            border_width=1,
            height=120
        )
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=title,
            text_color=TEXT,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=14, pady=(14, 4))

        ctk.CTkLabel(
            card,
            text=value,
            text_color=ACCENT,
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w"
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

    def update_metric_cards(self):
        for widget in self.metrics.winfo_children():
            widget.destroy()

        if self.current_mode == "pvgis":
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
            card = self.create_metric_card(self.metrics, title, value, subtitle)
            card.pack(side="left", fill="both", expand=True, padx=4)

    # Mode Switching

    def on_mode_change(self, selected):
        if selected == "PVGIS Solar Output":
            self.current_mode = "pvgis"
        else:
            self.current_mode = "uci"

        self.build_dynamic_fields()
        self.clear_inputs()
        self.update_mode_labels()
        self.update_metric_cards()

    def update_mode_labels(self):
        if self.current_mode == "pvgis":
            self.result_title.configure(text="Solar Energy Output")
            self.result_value.configure(text="0.0000 kWh")
            self.card_dataset.value_label.configure(text="PVGIS-ERA5")
            self.card_dataset.subtitle_label.configure(text="Solar output prediction")
            self.summary_text.configure(text="PVGIS mode predicts estimated solar energy output.")
        else:
            self.result_title.configure(text="Building Heating Load")
            self.result_value.configure(text="0.0000")
            self.card_dataset.value_label.configure(text="UCI Energy")
            self.card_dataset.subtitle_label.configure(text="Heating load prediction")
            self.summary_text.configure(text="UCI mode predicts building heating load.")

    # Actions

    def clear_inputs(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

        if self.current_mode == "pvgis":
            self.result_value.configure(text="0.0000 kWh")
        else:
            self.result_value.configure(text="0.0000")

        self.result_desc.configure(text="Predict to see the estimated output.")
        self.energy_progress.set(0)
        self.percentage_label.configure(text="0%")
        self.summary_status.configure(text="System Ready")
        self.card_current.value_label.configure(text="—")
        self.card_status.value_label.configure(text="Ready")
        self.card_status.subtitle_label.configure(text="Model loaded successfully")

    def load_example(self):
        self.clear_inputs()

        if self.current_mode == "pvgis":
            values = {
                "h_sun": "70",
                "temperature": "32",
                "wind_speed": "4",
                "hour": "12",
                "month": "5",
                "day_of_week": "2",
            }
        else:
            values = {
                "relative_compactness": "0.76",
                "surface_area": "661.5",
                "wall_area": "416.5",
                "roof_area": "122.5",
                "overall_height": "7.0",
                "orientation": "3",
                "glazing_area": "0.25",
                "glazing_area_distribution": "3",
            }

        for key, value in values.items():
            self.entries[key].insert(0, value)

    def predict(self):
        try:
            if self.current_mode == "pvgis":
                values = [
                    float(self.entries["h_sun"].get()),
                    float(self.entries["temperature"].get()),
                    float(self.entries["wind_speed"].get()),
                    float(self.entries["hour"].get()),
                    float(self.entries["month"].get()),
                    float(self.entries["day_of_week"].get()),
                ]

                error_message = validate_pvgis_inputs(values)
                if error_message:
                    messagebox.showerror("Input Error", error_message)
                    return

                model_bundle = self.models["pvgis"]
                prediction = predict_from_model(
                    model_bundle["model"],
                    model_bundle["scaler_X"],
                    model_bundle["scaler_y"],
                    values
                )

                status, desc = get_solar_status(prediction)
                progress, percentage = get_energy_percentage(prediction, max_expected=0.86)

                self.result_value.configure(text=f"{prediction:.4f} kWh")
                self.card_current.value_label.configure(text=f"{prediction:.4f} kWh")

            else:
                values = [
                    float(self.entries["relative_compactness"].get()),
                    float(self.entries["surface_area"].get()),
                    float(self.entries["wall_area"].get()),
                    float(self.entries["roof_area"].get()),
                    float(self.entries["overall_height"].get()),
                    float(self.entries["orientation"].get()),
                    float(self.entries["glazing_area"].get()),
                    float(self.entries["glazing_area_distribution"].get()),
                ]

                error_message = validate_uci_inputs(values)
                if error_message:
                    messagebox.showerror("Input Error", error_message)
                    return

                model_bundle = self.models["uci"]
                prediction = predict_from_model(
                    model_bundle["model"],
                    model_bundle["scaler_X"],
                    model_bundle["scaler_y"],
                    values
                )

                status, desc = get_heating_status(prediction)
                progress, percentage = get_energy_percentage(prediction, max_expected=45)

                self.result_value.configure(text=f"{prediction:.4f}")
                self.card_current.value_label.configure(text=f"{prediction:.4f}")

            self.result_desc.configure(text=desc)
            self.energy_progress.set(progress)
            self.percentage_label.configure(text=f"{percentage}%")

            self.summary_status.configure(text=status)
            self.summary_text.configure(text=f"Predicted value: {prediction:.4f}")

            self.card_status.value_label.configure(text=status)
            self.card_status.subtitle_label.configure(text=desc)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Error", str(e))