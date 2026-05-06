from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "ann_real_pvgis_iloilo_model.weights.h5"

SCALER_X_PATH = BASE_DIR / "artifacts" / "scaler_X.pkl"
SCALER_Y_PATH = BASE_DIR / "artifacts" / "scaler_y.pkl"
FEATURES_PATH = BASE_DIR / "artifacts" / "features.pkl"

APP_TITLE = "Energy ANN Dashboard"
WINDOW_SIZE = "1360x860"
MIN_WIDTH = 1200
MIN_HEIGHT = 780

ANN_RMSE = 0.068857
ANN_MAE = 0.045875
ANN_R2 = 0.913024

LR_RMSE = 0.087915
LR_MAE = 0.058099
LR_R2 = 0.858216