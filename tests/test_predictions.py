from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.model_loader import load_all_models_and_artifacts
from src.predictor import predict_from_model
from src.validation import validate_pvgis_inputs, validate_uci_inputs


def assert_condition(condition, message):
    if not condition:
        raise AssertionError(message)


def test_pvgis_prediction(models):
    print("\nTesting PVGIS Solar model...")

    pvgis = models["pvgis"]

    assert_condition(len(pvgis["features"]) == 6, "PVGIS should have 6 features.")

    noon_values = [70, 32, 4, 12, 5, 2]
    night_values = [0, 26, 2, 23, 5, 2]

    assert_condition(
        validate_pvgis_inputs(noon_values) is None,
        "Valid PVGIS noon input failed validation."
    )

    assert_condition(
        validate_pvgis_inputs(night_values) is None,
        "Valid PVGIS night input failed validation."
    )

    noon_prediction = predict_from_model(
        pvgis["model"],
        pvgis["scaler_X"],
        pvgis["scaler_y"],
        noon_values
    )

    night_prediction = predict_from_model(
        pvgis["model"],
        pvgis["scaler_X"],
        pvgis["scaler_y"],
        night_values
    )

    print(f"PVGIS noon prediction: {noon_prediction:.4f} kWh")
    print(f"PVGIS night prediction: {night_prediction:.4f} kWh")

    assert_condition(noon_prediction >= 0, "PVGIS noon prediction should not be negative.")
    assert_condition(night_prediction >= 0, "PVGIS night prediction should not be negative.")
    assert_condition(noon_prediction > night_prediction, "PVGIS noon output should be higher than night output.")
    assert_condition(noon_prediction <= 1.2, "PVGIS noon prediction is unrealistically high for a 1 kWp system.")
    assert_condition(night_prediction <= 0.2, "PVGIS night prediction should be low.")

    invalid_hour = [70, 32, 4, 30, 5, 2]
    validation_error = validate_pvgis_inputs(invalid_hour)

    assert_condition(
        validation_error is not None,
        "Invalid PVGIS hour was not caught."
    )

    print("PVGIS tests passed.")


def test_uci_prediction(models):
    print("\nTesting UCI Heating Load model...")

    uci = models["uci"]

    assert_condition(len(uci["features"]) == 8, "UCI should have 8 features.")

    sample_values = [0.76, 661.5, 416.5, 122.5, 7.0, 3, 0.25, 3]
    lower_load_values = [0.98, 514.5, 294.0, 110.25, 7.0, 2, 0.0, 0]

    assert_condition(
        validate_uci_inputs(sample_values) is None,
        "Valid UCI sample input failed validation."
    )

    assert_condition(
        validate_uci_inputs(lower_load_values) is None,
        "Valid UCI lower-load input failed validation."
    )

    sample_prediction = predict_from_model(
        uci["model"],
        uci["scaler_X"],
        uci["scaler_y"],
        sample_values
    )

    lower_load_prediction = predict_from_model(
        uci["model"],
        uci["scaler_X"],
        uci["scaler_y"],
        lower_load_values
    )

    print(f"UCI sample prediction: {sample_prediction:.4f} HL")
    print(f"UCI comparison prediction: {lower_load_prediction:.4f} HL")

    assert_condition(sample_prediction >= 0, "UCI sample prediction should not be negative.")
    assert_condition(lower_load_prediction >= 0, "UCI comparison prediction should not be negative.")
    assert_condition(sample_prediction <= 60, "UCI sample prediction is unrealistically high.")
    assert_condition(lower_load_prediction <= 60, "UCI comparison prediction is unrealistically high.")
    assert_condition(
        abs(sample_prediction - lower_load_prediction) > 0.1,
        "Different UCI inputs should produce different predictions."
    )

    invalid_height = [0.76, 661.5, 416.5, 122.5, 5.0, 3, 0.25, 3]
    validation_error = validate_uci_inputs(invalid_height)

    assert_condition(
        validation_error is not None,
        "Invalid UCI height was not caught."
    )

    print("UCI tests passed.")


def main():
    print("Loading models and artifacts...")
    models = load_all_models_and_artifacts()

    assert_condition("pvgis" in models, "PVGIS model bundle missing.")
    assert_condition("uci" in models, "UCI model bundle missing.")

    test_pvgis_prediction(models)
    test_uci_prediction(models)

    print("\nAll prediction tests passed successfully.")


if __name__ == "__main__":
    main()