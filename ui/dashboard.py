from tkinter import messagebox
import customtkinter as ctk

from src.config import APP_TITLE, WINDOW_SIZE, MIN_WIDTH, MIN_HEIGHT
from src.model_loader import load_all_models_and_artifacts
from src.predictor import (
    predict_from_model,
    get_solar_status,
    get_heating_status,
    get_energy_percentage,
)
from src.validation import validate_pvgis_inputs, validate_uci_inputs

from ui.theme import BG, WHITE, ACCENT, ACCENT_DARK, TEXT
from ui.pages.overview_page import build_overview_page
from ui.pages.monitoring_page import build_monitoring_page
from ui.pages.analytics_page import build_analytics_page
from ui.pages.energy_page import build_energy_page


class EnergyDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.models = load_all_models_and_artifacts()
        self.current_mode = "pvgis"
        self.current_page = "Monitoring"
        self.nav_buttons = {}
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

        self.page_container = ctk.CTkFrame(self.wrapper, fg_color=BG, corner_radius=0)
        self.page_container.pack(fill="both", expand=True)

        self.show_page("Monitoring")

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

        nav_items = ["Overview", "Monitoring", "Analytics", "Energy"]

        for page_name in nav_items:
            is_active = page_name == self.current_page

            btn = ctk.CTkButton(
                center_frame,
                text=page_name,
                width=120,
                height=40,
                corner_radius=20,
                fg_color=ACCENT if is_active else WHITE,
                hover_color=ACCENT_DARK if is_active else "#F2F2F2",
                text_color="white" if is_active else "#555555",
                border_width=0,
                command=lambda page=page_name: self.show_page(page)
            )
            btn.pack(side="left", padx=8)

            self.nav_buttons[page_name] = btn

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

    def clear_page_container(self):
        for widget in self.page_container.winfo_children():
            widget.destroy()

    def update_navbar_active_state(self):
        for page_name, button in self.nav_buttons.items():
            is_active = page_name == self.current_page

            button.configure(
                fg_color=ACCENT if is_active else WHITE,
                hover_color=ACCENT_DARK if is_active else "#F2F2F2",
                text_color="white" if is_active else "#555555"
            )

    def show_page(self, page_name):
        self.current_page = page_name
        self.update_navbar_active_state()
        self.clear_page_container()

        if page_name == "Overview":
            build_overview_page(self)

        elif page_name == "Monitoring":
            build_monitoring_page(self)

        elif page_name == "Analytics":
            build_analytics_page(self)

        elif page_name == "Energy":
            build_energy_page(self)

    # ------------------------
    # Shared mode / prediction actions
    # ------------------------

    def on_mode_change(self, selected):
        if selected == "PVGIS Solar Output":
            self.current_mode = "pvgis"
        else:
            self.current_mode = "uci"

        if hasattr(self, "build_dynamic_fields"):
            self.build_dynamic_fields()

        self.clear_inputs()
        self.update_mode_labels()

        if hasattr(self, "update_metric_cards"):
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
            self.result_value.configure(text="0.0000 HL")
            self.card_dataset.value_label.configure(text="UCI Energy")
            self.card_dataset.subtitle_label.configure(text="Heating load prediction")
            self.summary_text.configure(text="UCI mode predicts building heating load.")

    def clear_inputs(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

        if hasattr(self, "result_value"):
            if self.current_mode == "pvgis":
                self.result_value.configure(text="0.0000 kWh")
            else:
                self.result_value.configure(text="0.0000 HL")

        if hasattr(self, "result_desc"):
            self.result_desc.configure(text="Predict to see the estimated output.")

        if hasattr(self, "energy_progress"):
            self.energy_progress.set(0)

        if hasattr(self, "percentage_label"):
            self.percentage_label.configure(text="0%")

        if hasattr(self, "summary_status"):
            self.summary_status.configure(text="System Ready")

        if hasattr(self, "card_current"):
            self.card_current.value_label.configure(text="—")

        if hasattr(self, "card_status"):
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

                self.result_value.configure(text=f"{prediction:.4f} HL")
                self.card_current.value_label.configure(text=f"{prediction:.4f} HL")

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