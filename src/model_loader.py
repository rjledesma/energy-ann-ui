import joblib
from tensorflow import keras

from src.config import MODEL_PATH, SCALER_X_PATH, SCALER_Y_PATH, FEATURES_PATH


def build_model():
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

    return model


def load_model_and_artifacts():
    model = build_model()
    model.load_weights(MODEL_PATH)

    scaler_X = joblib.load(SCALER_X_PATH)
    scaler_y = joblib.load(SCALER_Y_PATH)
    features = joblib.load(FEATURES_PATH)

    return model, scaler_X, scaler_y, features