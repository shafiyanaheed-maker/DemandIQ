import React, { useMemo, useState } from "react";
import {
  forecastData,
  prototypeProducts,
} from "../data/prototypeData";

export default function Forecast() {
  const [selectedId, setSelectedId] = useState(1);
  const [generated, setGenerated] = useState(false);

  const product = prototypeProducts.find(
    (item) => item.id === selectedId
  );

  const forecast = useMemo(
    () => forecastData[selectedId],
    [selectedId]
  );

  const chartData = [
    ...forecast.history.map((item) => ({
      ...item,
      type: "Historical",
    })),
    ...forecast.forecast.map((item) => ({
      ...item,
      type: "Forecast",
    })),
  ];

  const maxDemand = Math.max(
    ...chartData.map((item) => item.demand)
  );

  return (
    <div className="forecast-page">
      <aside className="forecast-sidebar">
        <div className="forecast-brand">
          <div className="forecast-brand-mark">D</div>
          <div>
            <strong>DemandIQ</strong>
            <span>Intelligent Decisions</span>
          </div>
        </div>

        <nav>
          <a href="/dashboard">▦ Dashboard</a>
          <a href="/forecast" className="active">
            ⌁ Forecast
          </a>
          <a href="/inventory">▣ Inventory</a>
          <a href="/analytics">◫ Analytics</a>
          <a href="/alerts">! Alerts</a>

          <div className="forecast-nav-title">
            FINANCIAL
          </div>

          <a href="/investor">↗ Financial Stocks</a>
          <a href="/portfolio">◉ Portfolio</a>
          <a href="/transactions">↔ Transactions</a>
        </nav>
      </aside>

      <main className="forecast-main">
        <header className="forecast-header">
          <div>
            <h1>Demand Forecast</h1>
            <p>
              Analyze historical demand and forecast future
              product requirements.
            </p>
          </div>

          <a
            href="/dashboard"
            className="forecast-back-button"
          >
            ← Dashboard
          </a>
        </header>

        <section className="forecast-control-panel">
          <div>
            <label>Select Product</label>

            <select
              value={selectedId}
              onChange={(event) => {
                setSelectedId(Number(event.target.value));
                setGenerated(false);
              }}
            >
              {prototypeProducts.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
            </select>
          </div>

          <div className="forecast-product-info">
            <span>{product.category}</span>
            <strong>{product.name}</strong>
          </div>

          <button
            className="forecast-generate-button"
            onClick={() => setGenerated(true)}
          >
            {generated
              ? "Forecast Generated ✓"
              : "Generate Forecast"}
          </button>
        </section>

        {generated && (
          <div className="forecast-success">
            ✓ 7-day demand forecast generated successfully.
          </div>
        )}

        <section className="forecast-metric-grid">
          <div className="forecast-metric-card">
            <span>Current Stock</span>
            <strong>{product.stock}</strong>
            <small>units available</small>
          </div>

          <div className="forecast-metric-card">
            <span>7-Day Forecast</span>
            <strong>{product.predictedDemand}</strong>
            <small>units expected</small>
          </div>

          <div className="forecast-metric-card">
            <span>MAE</span>
            <strong>{forecast.mae}</strong>
            <small>forecast error</small>
          </div>

          <div className="forecast-metric-card">
            <span>MAPE</span>
            <strong>{forecast.mape}%</strong>
            <small>prediction error</small>
          </div>
        </section>

        <section className="forecast-chart-panel">
          <div className="forecast-panel-heading">
            <div>
              <h2>Historical vs Forecasted Demand</h2>
              <p>
                Actual demand followed by the predicted
                seven-day demand.
              </p>
            </div>

            <div className="forecast-legend">
              <span>
                <i className="forecast-dot historical" />
                Historical
              </span>

              <span>
                <i className="forecast-dot predicted" />
                Forecast
              </span>
            </div>
          </div>

          <div className="forecast-chart">
            <div className="forecast-y-axis">
              <span>{maxDemand}</span>
              <span>{Math.round(maxDemand * 0.75)}</span>
              <span>{Math.round(maxDemand * 0.5)}</span>
              <span>{Math.round(maxDemand * 0.25)}</span>
              <span>0</span>
            </div>

            <div className="forecast-chart-area">
              <div className="forecast-grid">
                <span />
                <span />
                <span />
                <span />
                <span />
              </div>

              <div className="forecast-bars">
                {chartData.map((item, index) => {
                  const height =
                    (item.demand / maxDemand) * 100;

                  return (
                    <div
                      className="forecast-column"
                      key={`${item.date}-${index}`}
                    >
                      <div
                        className={`forecast-bar-column ${
                          item.type === "Forecast"
                            ? "predicted"
                            : "historical"
                        }`}
                        style={{
                          height: `${Math.max(
                            height,
                            8
                          )}%`,
                        }}
                        title={`${item.date}: ${item.demand} units`}
                      />

                      <span>
                        {item.date.replace("Sep ", "")}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </section>

        <section className="forecast-bottom-grid">
          <div className="forecast-detail-card">
            <h2>Forecast Performance</h2>

            <div className="performance-row">
              <span>MAE</span>
              <strong>{forecast.mae}</strong>
            </div>

            <div className="performance-row">
              <span>RMSE</span>
              <strong>{forecast.rmse}</strong>
            </div>

            <div className="performance-row">
              <span>MAPE</span>
              <strong>{forecast.mape}%</strong>
            </div>

            <div className="performance-note">
              Lower error values indicate closer agreement
              between predicted and actual demand.
            </div>
          </div>

          <div className="forecast-detail-card">
            <h2>Inventory Impact</h2>

            <div className="impact-item">
              <span>Current Stock</span>
              <strong>{product.stock} units</strong>
            </div>

            <div className="impact-item">
              <span>Predicted Demand</span>
              <strong>{product.predictedDemand} units</strong>
            </div>

            <div className="impact-item">
              <span>Projected Stock</span>
              <strong
                className={
                  product.projectedStock < 0
                    ? "forecast-danger"
                    : ""
                }
              >
                {product.projectedStock} units
              </strong>
            </div>

            <div className="impact-recommendation">
              <span>Recommendation</span>
              <strong>
                {product.reorder > 0
                  ? `Reorder ${product.reorder} units`
                  : "Inventory level is healthy"}
              </strong>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}