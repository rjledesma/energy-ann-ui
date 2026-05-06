def validate_pvgis_inputs(values):
    h_sun, temperature, wind_speed, hour, month, day_of_week = values

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


def validate_uci_inputs(values):
    (
        relative_compactness,
        surface_area,
        wall_area,
        roof_area,
        overall_height,
        orientation,
        glazing_area,
        glazing_area_distribution,
    ) = values

    if not 0.5 <= relative_compactness <= 1.0:
        return "Relative compactness should be between 0.5 and 1.0."
    if not 500 <= surface_area <= 900:
        return "Surface area should be between 500 and 900."
    if not 200 <= wall_area <= 450:
        return "Wall area should be between 200 and 450."
    if not 100 <= roof_area <= 250:
        return "Roof area should be between 100 and 250."
    if overall_height not in [3.5, 7.0]:
        return "Overall height should be 3.5 or 7.0."
    if orientation not in [2, 3, 4, 5]:
        return "Orientation should be 2, 3, 4, or 5."
    if not 0 <= glazing_area <= 0.4:
        return "Glazing area should be between 0 and 0.4."
    if glazing_area_distribution not in [0, 1, 2, 3, 4, 5]:
        return "Glazing area distribution should be 0 to 5."

    return None