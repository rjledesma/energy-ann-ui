def validate_inputs(h_sun, temperature, wind_speed, hour, month, day_of_week):
    if not 0 <= h_sun <= 90:
        return "Sun height H_sun must be between 0 and 90."

    if not 15 <= temperature <= 45:
        return "Temperature should be between 15°C and 45°C."

    if not 0 <= wind_speed <= 20:
        return "Wind speed must be between 0 and 20 m/s."

    if not 0 <= hour <= 23:
        return "Hour must be between 0 and 23."

    if not 1 <= month <= 12:
        return "Month must be between 1 and 12."

    if not 0 <= day_of_week <= 6:
        return "Day of week must be between 0 and 6."

    return None