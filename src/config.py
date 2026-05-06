from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PVGIS_MODEL_PATH = BASE_DIR / "models" / "pvgis_solar_ann_model.weights.h5"
UCI_MODEL_PATH = BASE_DIR / "models" / "uci_heating_ann_model.weights.h5"

PVGIS_SCALER_X_PATH = BASE_DIR / "artifacts" / "pvgis_scaler_X.pkl"
PVGIS_SCALER_Y_PATH = BASE_DIR / "artifacts" / "pvgis_scaler_y.pkl"
PVGIS_FEATURES_PATH = BASE_DIR / "artifacts" / "pvgis_features.pkl"

UCI_SCALER_X_PATH = BASE_DIR / "artifacts" / "uci_scaler_X.pkl"
UCI_SCALER_Y_PATH = BASE_DIR / "artifacts" / "uci_scaler_y.pkl"
UCI_FEATURES_PATH = BASE_DIR / "artifacts" / "uci_features.pkl"

APP_TITLE = "Energy ANN Dashboard"
WINDOW_WIDTH_RATIO = 0.85
WINDOW_HEIGHT_RATIO = 0.85

MIN_WIDTH = 1100
MIN_HEIGHT = 750
MAX_WIDTH = 1500
MAX_HEIGHT = 950

PVGIS_ANN_RMSE = 0.063716
PVGIS_ANN_MAE = 0.035680
PVGIS_ANN_R2 = 0.925529

PVGIS_LR_RMSE = 0.087915
PVGIS_LR_MAE = 0.058099
PVGIS_LR_R2 = 0.858216

UCI_ANN_RMSE = 2.716647
UCI_ANN_MAE = 1.901916
UCI_ANN_R2 = 0.924656

UCI_LR_RMSE = 2.773799
UCI_LR_MAE = 2.072221
UCI_LR_R2 = 0.921452