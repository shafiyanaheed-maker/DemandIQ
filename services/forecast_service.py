from datetime import date, timedelta

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from database import get_connection


FORECAST_DAYS = 7
MINIMUM_HISTORY_DAYS = 30


def get_sales_data(product_id):
    """Load historical daily sales for one product."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                sale_date,
                SUM(quantity_sold) AS quantity_sold
            FROM sales
            WHERE product_id = %s
            GROUP BY sale_date
            ORDER BY sale_date
            """,
            (product_id,)
        )

        rows = cursor.fetchall()

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows)

        df["sale_date"] = pd.to_datetime(df["sale_date"])
        df["quantity_sold"] = pd.to_numeric(
            df["quantity_sold"]
        )

        # Include dates where there were no sales.
        full_dates = pd.date_range(
            start=df["sale_date"].min(),
            end=df["sale_date"].max(),
            freq="D"
        )

        df = (
            df.set_index("sale_date")
            .reindex(full_dates, fill_value=0)
            .rename_axis("sale_date")
            .reset_index()
        )

        return df

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def create_features(df):
    """Create time-series features for the ML model."""

    data = df.copy()

    data["day_of_week"] = data["sale_date"].dt.dayofweek
    data["day_of_month"] = data["sale_date"].dt.day
    data["month"] = data["sale_date"].dt.month
    data["week_of_year"] = data["sale_date"].dt.isocalendar().week.astype(int)

    # Previous-day demand.
    data["lag_1"] = data["quantity_sold"].shift(1)

    # Previous-week demand.
    data["lag_7"] = data["quantity_sold"].shift(7)

    # Rolling averages.
    data["rolling_7"] = (
        data["quantity_sold"]
        .shift(1)
        .rolling(7)
        .mean()
    )

    data["rolling_14"] = (
        data["quantity_sold"]
        .shift(1)
        .rolling(14)
        .mean()
    )

    return data


def forecast_product(product_id, forecast_days=FORECAST_DAYS):
    """
    Generate future demand predictions for one product.

    Returns a list containing forecast date and predicted demand.
    """

    df = get_sales_data(product_id)

    if df.empty:
        raise ValueError("No sales history found for this product.")

    if len(df) < MINIMUM_HISTORY_DAYS:
        raise ValueError(
            f"At least {MINIMUM_HISTORY_DAYS} days of sales history "
            "are required for forecasting."
        )

    data = create_features(df)

    feature_columns = [
        "day_of_week",
        "day_of_month",
        "month",
        "week_of_year",
        "lag_1",
        "lag_7",
        "rolling_7",
        "rolling_14"
    ]

    training_data = data.dropna().copy()

    if len(training_data) < 14:
        raise ValueError(
            "Not enough valid historical records for forecasting."
        )

    X = training_data[feature_columns]
    y = training_data["quantity_sold"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        min_samples_leaf=2
    )

    model.fit(X, y)

    history = df.copy()

    predictions = []

    last_date = history["sale_date"].max()

    for _ in range(forecast_days):
        next_date = last_date + timedelta(days=1)

        recent_values = history["quantity_sold"].tolist()

        lag_1 = recent_values[-1]

        lag_7 = (
            recent_values[-7]
            if len(recent_values) >= 7
            else sum(recent_values) / len(recent_values)
        )

        rolling_7 = sum(recent_values[-7:]) / min(
            7,
            len(recent_values)
        )

        rolling_14 = sum(recent_values[-14:]) / min(
            14,
            len(recent_values)
        )

        features = pd.DataFrame([{
            "day_of_week": next_date.dayofweek,
            "day_of_month": next_date.day,
            "month": next_date.month,
            "week_of_year": next_date.isocalendar().week,
            "lag_1": lag_1,
            "lag_7": lag_7,
            "rolling_7": rolling_7,
            "rolling_14": rolling_14
        }])

        prediction = model.predict(features)[0]

        predicted_demand = max(
            0,
            round(float(prediction))
        )

        predictions.append({
            "product_id": product_id,
            "forecast_date": next_date.date(),
            "predicted_demand": predicted_demand
        })

        # Add prediction to history so the next forecast
        # can use the previous prediction as lagged demand.
        history.loc[len(history)] = [
            next_date,
            predicted_demand
        ]

        last_date = next_date

    return predictions


def save_forecasts(product_id, predictions):
    """Replace existing future forecasts for a product."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM forecast
            WHERE product_id = %s
              AND forecast_date >= CURDATE()
            """,
            (product_id,)
        )

        for prediction in predictions:
            cursor.execute(
                """
                INSERT INTO forecast (
                    product_id,
                    predicted_demand,
                    forecast_date
                )
                VALUES (%s, %s, %s)
                """,
                (
                    prediction["product_id"],
                    prediction["predicted_demand"],
                    prediction["forecast_date"]
                )
            )

        connection.commit()

    except Exception:
        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def generate_product_forecast(
    product_id,
    forecast_days=FORECAST_DAYS
):
    """Generate and save a forecast for one product."""

    predictions = forecast_product(
        product_id,
        forecast_days
    )

    save_forecasts(
        product_id,
        predictions
    )

    return predictions


def generate_all_forecasts(
    forecast_days=FORECAST_DAYS
):
    """Generate forecasts for every product with sufficient history."""

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT product_id
            FROM products
            ORDER BY product_id
            """
        )

        product_ids = [
            row[0]
            for row in cursor.fetchall()
        ]

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

    results = []
    skipped = []

    for product_id in product_ids:
        try:
            predictions = generate_product_forecast(
                product_id,
                forecast_days
            )

            results.append({
                "product_id": product_id,
                "forecast_days": len(predictions)
            })

        except ValueError as error:
            skipped.append({
                "product_id": product_id,
                "reason": str(error)
            })

    return {
        "generated": results,
        "skipped": skipped
    }