from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib
from tensorflow import keras


# Load files from the same folder as app.py
BASE_DIR = Path(__file__).resolve().parent

WEIGHTS_PATH = BASE_DIR / "ann_real_pvgis_iloilo_model.weights.h5"
SCALER_X_PATH = BASE_DIR / "scaler_X.pkl"
SCALER_Y_PATH = BASE_DIR / "scaler_y.pkl"
FEATURES_PATH = BASE_DIR / "features.pkl"


# Rebuild the same ANN architecture used in Colab
model = keras.Sequential([
    keras.layers.Input(shape=(6,)),
    keras.layers.Dense(10, activation="relu"),
    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dense(1, activation="linear")
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss="mse",
    metrics=["mae"]
)

# Load trained weights instead of full .keras model
model.load_weights(WEIGHTS_PATH)

# Load preprocessing files
scaler_X = joblib.load(SCALER_X_PATH)
scaler_y = joblib.load(SCALER_Y_PATH)
features = joblib.load(FEATURES_PATH)


def predict_energy():
    try:
        h_sun = float(entry_h_sun.get())
        temperature = float(entry_temp.get())
        wind_speed = float(entry_wind.get())
        hour = float(entry_hour.get())
        month = float(entry_month.get())
        day_of_week = float(entry_day.get())

        if not 0 <= hour <= 23:
            messagebox.showerror("Input Error", "Hour must be between 0 and 23.")
            return

        if not 1 <= month <= 12:
            messagebox.showerror("Input Error", "Month must be between 1 and 12.")
            return

        if not 0 <= day_of_week <= 6:
            messagebox.showerror("Input Error", "Day of week must be between 0 and 6.")
            return

        input_data = np.array([[
            h_sun,
            temperature,
            wind_speed,
            hour,
            month,
            day_of_week
        ]])

        input_scaled = scaler_X.transform(input_data)
        prediction_scaled = model.predict(input_scaled, verbose=0)
        prediction = scaler_y.inverse_transform(prediction_scaled)

        energy_kwh = prediction[0][0]

        result_label.config(
            text=f"Predicted Solar Energy Output: {energy_kwh:.4f} kWh"
        )

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Please enter valid numeric values for all fields."
        )
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Main window
root = tk.Tk()
root.title("Solar Energy Output Prediction")
root.geometry("500x500")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Solar Energy Output Prediction",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=20)

subtitle_label = tk.Label(
    root,
    text="ANN Model using PVGIS-ERA5 Data",
    font=("Arial", 11)
)
subtitle_label.pack(pady=5)

form_frame = tk.Frame(root)
form_frame.pack(pady=20)


def add_input(label_text, row):
    label = tk.Label(form_frame, text=label_text, font=("Arial", 11), anchor="w")
    label.grid(row=row, column=0, padx=10, pady=8, sticky="w")

    entry = tk.Entry(form_frame, width=25, font=("Arial", 11))
    entry.grid(row=row, column=1, padx=10, pady=8)

    return entry


entry_h_sun = add_input("Sun Height H_sun:", 0)
entry_temp = add_input("Temperature T2m (°C):", 1)
entry_wind = add_input("Wind Speed WS10m (m/s):", 2)
entry_hour = add_input("Hour (0-23):", 3)
entry_month = add_input("Month (1-12):", 4)
entry_day = add_input("Day of Week (0=Mon, 6=Sun):", 5)

predict_button = tk.Button(
    root,
    text="Predict Energy Output",
    font=("Arial", 12, "bold"),
    command=predict_energy,
    width=25
)
predict_button.pack(pady=20)

result_label = tk.Label(
    root,
    text="Predicted Solar Energy Output: ---",
    font=("Arial", 13, "bold"),
    wraplength=450
)
result_label.pack(pady=20)

sample_label = tk.Label(
    root,
    text="Example: H_sun=45, T2m=30, WS10m=3.5, Hour=12, Month=4, Day=2",
    font=("Arial", 9),
    wraplength=420
)
sample_label.pack(pady=10)

root.mainloop()