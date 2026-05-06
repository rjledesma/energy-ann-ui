import numpy as np


def predict_energy_output(
    model,
    scaler_X,
    scaler_y,
    h_sun,
    temperature,
    wind_speed,
    hour,
    month,
    day_of_week
):
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

    energy_kwh = float(prediction[0][0])
    return max(0.0, energy_kwh)


def get_energy_status(energy_kwh):
    if energy_kwh < 0.10:
        return (
            "Low Output",
            "Likely low solar production due to weak sunlight / night conditions."
        )

    if energy_kwh < 0.40:
        return (
            "Moderate Output",
            "Solar production is active but not at peak level."
        )

    return (
        "High Output",
        "Strong solar production detected from current conditions."
    )


def get_energy_percentage(energy_kwh):
    max_expected_output = 0.86
    progress = min(energy_kwh / max_expected_output, 1.0)
    percentage = int(progress * 100)
    return progress, percentage