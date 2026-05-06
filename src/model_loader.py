import joblib
from tensorflow import keras

from src.config import (
    PVGIS_MODEL_PATH,
    UCI_MODEL_PATH,
    PVGIS_SCALER_X_PATH,
    PVGIS_SCALER_Y_PATH,
    PVGIS_FEATURES_PATH,
    UCI_SCALER_X_PATH,
    UCI_SCALER_Y_PATH,
    UCI_FEATURES_PATH,
)


def build_ann_model(input_shape):
    model = keras.Sequential([
        keras.layers.Input(shape=(input_shape,)),
        keras.layers.Dense(10, activation="relu"),
        keras.layers.Dense(8, activation="relu"),
        keras.layers.Dense(1, activation="linear")
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss="mse",
        metrics=["mae"]
    )

    return model


def load_all_models_and_artifacts():
    pvgis_scaler_X = joblib.load(PVGIS_SCALER_X_PATH)
    pvgis_scaler_y = joblib.load(PVGIS_SCALER_Y_PATH)
    pvgis_features = joblib.load(PVGIS_FEATURES_PATH)

    uci_scaler_X = joblib.load(UCI_SCALER_X_PATH)
    uci_scaler_y = joblib.load(UCI_SCALER_Y_PATH)
    uci_features = joblib.load(UCI_FEATURES_PATH)

    pvgis_model = build_ann_model(input_shape=len(pvgis_features))
    pvgis_model.load_weights(PVGIS_MODEL_PATH)

    uci_model = build_ann_model(input_shape=len(uci_features))
    uci_model.load_weights(UCI_MODEL_PATH)

    return {
        "pvgis": {
            "model": pvgis_model,
            "scaler_X": pvgis_scaler_X,
            "scaler_y": pvgis_scaler_y,
            "features": pvgis_features,
        },
        "uci": {
            "model": uci_model,
            "scaler_X": uci_scaler_X,
            "scaler_y": uci_scaler_y,
            "features": uci_features,
        },
    }