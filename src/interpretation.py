def compare_models(dataset_name, ann_rmse, ann_mae, ann_r2, lr_rmse, lr_mae, lr_r2):
    ann_better_rmse = ann_rmse < lr_rmse
    ann_better_mae = ann_mae < lr_mae
    ann_better_r2 = ann_r2 > lr_r2

    if ann_better_rmse and ann_better_mae and ann_better_r2:
        winner = "ANN"
        summary = (
            f"For the {dataset_name} dataset, the ANN performed better than Linear Regression. "
            f"It achieved lower RMSE and MAE values, meaning it had smaller prediction errors. "
            f"It also achieved a higher R² score, meaning it explained more variation in the target variable."
        )
    elif not ann_better_rmse and not ann_better_mae and not ann_better_r2:
        winner = "Linear Regression"
        summary = (
            f"For the {dataset_name} dataset, Linear Regression performed better than the ANN. "
            f"This suggests that the relationship between the selected features and the target variable may be mostly linear."
        )
    else:
        winner = "Mixed"
        summary = (
            f"For the {dataset_name} dataset, the results were mixed. "
            f"One model performed better on some metrics, while the other model performed better on others. "
            f"This means the results should be interpreted using all metrics together."
        )

    return {
        "winner": winner,
        "summary": summary,
        "details": (
            f"ANN: RMSE={ann_rmse:.4f}, MAE={ann_mae:.4f}, R²={ann_r2:.4f}. "
            f"Linear Regression: RMSE={lr_rmse:.4f}, MAE={lr_mae:.4f}, R²={lr_r2:.4f}."
        )
    }


def generate_overall_interpretation(pvgis_result, uci_result):
    if pvgis_result["winner"] == "ANN" and uci_result["winner"] == "ANN":
        return (
            "Overall, the ANN performed better on both datasets. This supports the use of neural networks "
            "for energy-related regression tasks, especially when the relationship between input features "
            "and output values may be nonlinear."
        )

    if pvgis_result["winner"] == "Linear Regression" and uci_result["winner"] == "Linear Regression":
        return (
            "Overall, Linear Regression performed better on both datasets. This suggests that the selected "
            "features may have a strong linear relationship with the target variables."
        )

    return (
        "Overall, the results show that model performance depends on the dataset. The ANN may perform better "
        "when nonlinear relationships are present, while Linear Regression can remain competitive when the "
        "relationship is mostly linear."
    )