import numpy as np


def predict_from_model(model, scaler_X, scaler_y, values):
    input_data = np.array([values], dtype=float)

    input_scaled = scaler_X.transform(input_data)
    prediction_scaled = model.predict(input_scaled, verbose=0)
    prediction = scaler_y.inverse_transform(prediction_scaled)

    return max(0.0, float(prediction[0][0]))


def get_solar_status(energy_kwh):
    if energy_kwh < 0.10:
        return "Low Output", "Likely low solar production due to weak sunlight or night conditions."
    if energy_kwh < 0.40:
        return "Moderate Output", "Solar production is active but not at peak level."
    return "High Output", "Strong solar production detected from current conditions."


def get_heating_status(heating_load):
    if heating_load < 15:
        return "Low Heating Load", "The building design requires relatively low heating energy."
    if heating_load < 30:
        return "Moderate Heating Load", "The building design has moderate heating demand."
    return "High Heating Load", "The building design requires high heating energy."


def get_energy_percentage(value, max_expected):
    progress = min(value / max_expected, 1.0)
    percentage = int(progress * 100)
    return progress, percentage