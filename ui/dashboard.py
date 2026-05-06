from tkinter import messagebox
import customtkinter as ctk

from src.config import (
    APP_TITLE,
    WINDOW_SIZE,
    MIN_WIDTH,
    MIN_HEIGHT,
    ANN_RMSE,
    ANN_MAE,
    ANN_R2,
    LR_R2,
)

from src.model_loader import load_model_and_artifacts
from src.predictor import (
    predict_energy_output,
    get_energy_status,
    get_energy_percentage,
)
from src.validation import validate_inputs

from ui.theme import BG, CARD, WHITE, ACCENT, ACCENT_DARK, TEXT, MUTED, BORDER
from ui.components import add_input, create_metric_card, create_info_card


class EnergyDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.model, self.scaler_X, self.scaler_y, self.features = load_model_and_artifacts()

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
            text="Professional solar output monitoring and ANN-based prediction dashboard.",
            text_color=MUTED,
            font=ctk.CTkFont(size=18)
        ).pack(anchor="w")

        right = ctk.CTkFrame(
            hero,
            fg_color=WHITE,
            corner_radius=24,
            border_color=BORDER,
            border_width=1,
            width=360,
            height=180
        )
        right.pack(side="right", padx=(20, 0))
        right.pack_propagate(False)

        ctk.CTkLabel(
            right,
            text="Live Monitoring Summary",
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
            text="Use the panel below to estimate solar energy output.",
            text_color=MUTED,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        self.summary_text.pack(anchor="w", padx=20, pady=(10, 8))

    def build_main_section(self):
        main = ctk.CTkFrame(self.wrapper, fg_color=BG)
        main.pack(fill="both", expand=True)

        self.build_input_card(main)
        self.build_result_panel(main)

    def build_input_card(self, parent):
        input_card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=24,
            border_color=BORDER,
            border_width=1,
            width=500
        )
        input_card.pack(side="left", fill="y", padx=(0, 12))
        input_card.pack_propagate(False)

        ctk.CTkLabel(
            input_card,
            text="Prediction Inputs",
            text_color=TEXT,
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 8))

        ctk.CTkLabel(
            input_card,
            text="Enter current solar and weather conditions.",
            text_color=MUTED,
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=24, pady=(0, 16))

        form = ctk.CTkFrame(input_card, fg_color=CARD)
        form.pack(fill="x", padx=20, pady=(0, 10))

        self.entry_h_sun = add_input(form, "Sun Height H_sun", "0 - 90", 0)
        self.entry_temp = add_input(form, "Temperature T2m (°C)", "15 - 45", 1)
        self.entry_wind = add_input(form, "Wind Speed WS10m (m/s)", "0 - 20", 2)
        self.entry_hour = add_input(form, "Hour", "0 - 23", 3)
        self.entry_month = add_input(form, "Month", "1 - 12", 4)
        self.entry_day = add_input(form, "Day of Week", "0=Mon ... 6=Sun", 5)

        button_frame = ctk.CTkFrame(input_card, fg_color=CARD)
        button_frame.pack(fill="x", padx=20, pady=16)

        buttons = [
            ("Predict Output", self.predict_energy, ACCENT, "white"),
            ("Load Noon Example", self.load_noon_example, WHITE, TEXT),
            ("Load Night Example", self.load_night_example, WHITE, TEXT),
            ("Clear", self.clear_inputs, WHITE, TEXT),
        ]

        for index, (text, command, color, text_color) in enumerate(buttons):
            row = index // 2
            col = index % 2

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
            ).grid(row=row, column=col, padx=6, pady=6, sticky="ew")

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

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

        ctk.CTkLabel(
            result_card,
            text="Total Energy",
            text_color=TEXT,
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 8))

        self.result_value = ctk.CTkLabel(
            result_card,
            text="0.0000 kWh",
            text_color=ACCENT,
            font=ctk.CTkFont(size=38, weight="bold")
        )
        self.result_value.pack(anchor="w", padx=24)

        self.result_desc = ctk.CTkLabel(
            result_card,
            text="Predict to see the estimated solar energy output.",
            text_color=MUTED,
            font=ctk.CTkFont(size=15)
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
            "Current Power",
            "—",
            "Estimated output right now"
        )
        self.card_current.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        self.card_status = create_info_card(
            lower_cards,
            "System Status",
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
            "Iloilo 2022–2023"
        )
        self.card_dataset.grid(row=1, column=1, padx=6, pady=6, sticky="nsew")

        lower_cards.grid_columnconfigure(0, weight=1)
        lower_cards.grid_columnconfigure(1, weight=1)
        lower_cards.grid_rowconfigure(0, weight=1)
        lower_cards.grid_rowconfigure(1, weight=1)

    def build_metrics_section(self):
        metrics = ctk.CTkFrame(self.wrapper, fg_color=BG)
        metrics.pack(fill="x", pady=(16, 0))

        cards = [
            ("ANN RMSE", f"{ANN_RMSE:.6f}", "Lower is better"),
            ("ANN MAE", f"{ANN_MAE:.6f}", "Average absolute error"),
            ("ANN R²", f"{ANN_R2:.6f}", "Explains 91.3% variance"),
            ("Linear Regression R²", f"{LR_R2:.6f}", "Baseline comparison"),
        ]

        for title, value, subtitle in cards:
            card = create_metric_card(metrics, title, value, subtitle)
            card.pack(side="left", fill="both", expand=True, padx=6)

    def clear_inputs(self):
        for entry in [
            self.entry_h_sun,
            self.entry_temp,
            self.entry_wind,
            self.entry_hour,
            self.entry_month,
            self.entry_day
        ]:
            entry.delete(0, "end")

        self.result_value.configure(text="0.0000 kWh")
        self.result_desc.configure(text="Predict to see the estimated solar energy output.")
        self.energy_progress.set(0)
        self.percentage_label.configure(text="0%")
        self.summary_status.configure(text="System Ready")
        self.summary_text.configure(text="Use the panel below to estimate solar energy output.")
        self.card_current.value_label.configure(text="—")
        self.card_status.value_label.configure(text="Ready")
        self.card_status.subtitle_label.configure(text="Model loaded successfully")

    def load_noon_example(self):
        self.clear_inputs()
        self.entry_h_sun.insert(0, "70")
        self.entry_temp.insert(0, "32")
        self.entry_wind.insert(0, "4")
        self.entry_hour.insert(0, "12")
        self.entry_month.insert(0, "5")
        self.entry_day.insert(0, "2")

    def load_night_example(self):
        self.clear_inputs()
        self.entry_h_sun.insert(0, "0")
        self.entry_temp.insert(0, "26")
        self.entry_wind.insert(0, "2")
        self.entry_hour.insert(0, "23")
        self.entry_month.insert(0, "5")
        self.entry_day.insert(0, "2")

    def predict_energy(self):
        try:
            h_sun = float(self.entry_h_sun.get())
            temperature = float(self.entry_temp.get())
            wind_speed = float(self.entry_wind.get())
            hour = float(self.entry_hour.get())
            month = float(self.entry_month.get())
            day_of_week = float(self.entry_day.get())

            error_message = validate_inputs(
                h_sun,
                temperature,
                wind_speed,
                hour,
                month,
                day_of_week
            )

            if error_message:
                messagebox.showerror("Input Error", error_message)
                return

            energy_kwh = predict_energy_output(
                self.model,
                self.scaler_X,
                self.scaler_y,
                h_sun,
                temperature,
                wind_speed,
                hour,
                month,
                day_of_week
            )

            status, desc = get_energy_status(energy_kwh)
            progress, percentage = get_energy_percentage(energy_kwh)

            self.result_value.configure(text=f"{energy_kwh:.4f} kWh")
            self.result_desc.configure(text=desc)
            self.energy_progress.set(progress)
            self.percentage_label.configure(text=f"{percentage}%")
            self.summary_status.configure(text=status)
            self.summary_text.configure(
                text=f"Predicted solar energy output is {energy_kwh:.4f} kWh."
            )

            self.card_current.value_label.configure(text=f"{energy_kwh:.4f} kWh")
            self.card_status.value_label.configure(text=status)
            self.card_status.subtitle_label.configure(text=desc)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
        except Exception as e:
            messagebox.showerror("Error", str(e))