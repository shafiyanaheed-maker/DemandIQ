import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import {
  alerts,
  dashboardStats,
  demandTrend,
  inventorySummary,
  prototypeProducts,
} from "../data/prototypeData";

/* =========================================================
   SMALL COMPONENTS
   ========================================================= */

function StatCard({ title, value, subtitle, icon }) {
  return (
    <div className="dashboard-stat-card">
      <div className="stat-card-top">
        <span className="stat-title">{title}</span>
        <span className="stat-icon">{icon}</span>
      </div>

      <div className="stat-value">{value}</div>

      <div className="stat-subtitle">{subtitle}</div>
    </div>
  );
}

function StatusBadge({ status }) {
  const labels = {
    HEALTHY: "Healthy",
    LOW_STOCK: "Low Stock",
    REORDER_SOON: "Reorder Soon",
    STOCKOUT_RISK: "Stockout Risk",
    OUT_OF_STOCK: "Out of Stock",
  };

  return (
    <span className={`status-badge ${status.toLowerCase()}`}>
      {labels[status] || status}
    </span>
  );
}

function RiskBadge({ risk }) {
  return (
    <span className={`risk-badge ${risk.toLowerCase()}`}>
      {risk}
    </span>
  );
}

/* =========================================================
   BUSINESS DASHBOARD
   ========================================================= */

export default function BusinessDashboard() {
  const [selectedProductId, setSelectedProductId] = useState(
    prototypeProducts[0].id
  );

  const selectedProduct = useMemo(() => {
    return (
      prototypeProducts.find(
        (product) => product.id === selectedProductId
      ) || prototypeProducts[0]
    );
  }, [selectedProductId]);

  const selectedForecast = {
    demand: selectedProduct.predictedDemand,
    stock: selectedProduct.stock,
    projectedStock: selectedProduct.projectedStock,
    reorder: selectedProduct.reorder,
  };

  const inventoryHealthPercentage = Math.round(
    (inventorySummary.healthyItems / inventorySummary.totalItems) * 100
  );

  const handleLogout = () => {
    /*
      Prototype mode:
      No backend dependency is required for logout.
    */
    window.location.href = "/";
  };

  return (
    <div className="dashboard-page">
      {/* =====================================================
          SIDEBAR
          ===================================================== */}

      <aside className="dashboard-sidebar">
        <div className="dashboard-brand">
          <div className="brand-mark">D</div>

          <div>
            <div className="brand-name">DemandIQ</div>
            <div className="brand-subtitle">
              Intelligent Decisions
            </div>
          </div>
        </div>

        <nav className="dashboard-nav">
          <Link
            className="nav-item active"
            to="/dashboard"
          >
            <span>▦</span>
            Dashboard
          </Link>

          <Link
            className="nav-item"
            to="/forecast"
          >
            <span>⌁</span>
            Forecast
          </Link>

          <Link
            className="nav-item"
            to="/inventory"
          >
            <span>▣</span>
            Inventory
          </Link>

          <Link
            className="nav-item"
            to="/analytics"
          >
            <span>◫</span>
            Analytics
          </Link>

          <Link
            className="nav-item"
            to="/alerts"
          >
            <span>!</span>
            Alerts

            <span className="nav-alert-count">
              {alerts.length}
            </span>
          </Link>

          <div className="nav-section-title">
            FINANCIAL
          </div>

          <Link
            className="nav-item"
            to="/investor"
          >
            <span>↗</span>
            Financial Stocks
          </Link>

          <Link
            className="nav-item"
            to="/investor"
          >
            <span>◉</span>
            Portfolio
          </Link>

          <Link
            className="nav-item"
            to="/investor"
          >
            <span>↔</span>
            Transactions
          </Link>
        </nav>

        <div className="sidebar-bottom">
          <button
            className="logout-button"
            onClick={handleLogout}
          >
            <span>↪</span>
            Logout
          </button>
        </div>
      </aside>

      {/* =====================================================
          MAIN CONTENT
          ===================================================== */}

      <main className="dashboard-main">
        {/* Header */}

        <header className="dashboard-header">
          <div>
            <h1>Business Dashboard</h1>

            <p>
              Monitor demand, inventory health and forecast
              insights in one place.
            </p>
          </div>

          <div className="header-user">
            <div className="user-avatar">B</div>

            <div>
              <strong>Business User</strong>
              <span>Business</span>
            </div>
          </div>
        </header>

        {/* =================================================
            KPI CARDS
            ================================================= */}

        <section className="stats-grid">
          <StatCard
            title="Total Products"
            value={dashboardStats.totalProducts}
            subtitle="Products tracked"
            icon="◈"
          />

          <StatCard
            title="Total Revenue"
            value={`₹${(
              dashboardStats.totalRevenue / 100000
            ).toFixed(1)}L`}
            subtitle="Total recorded revenue"
            icon="₹"
          />

          <StatCard
            title="Forecasted Demand"
            value={dashboardStats.forecastedDemand.toLocaleString()}
            subtitle="Expected next 7 days"
            icon="⌁"
          />

          <StatCard
            title="Active Alerts"
            value={dashboardStats.activeAlerts}
            subtitle="Require attention"
            icon="!"
          />
        </section>

        {/* =================================================
            DEMAND + INVENTORY
            ================================================= */}

        <section className="dashboard-content-grid">
          {/* Demand Trend */}

          <div className="dashboard-panel demand-panel">
            <div className="panel-header">
              <div>
                <h2>Demand Trend</h2>

                <p>
                  Historical demand and upcoming forecast
                </p>
              </div>

              <span className="chart-period">
                14 Days
              </span>
            </div>

            <div className="demand-chart">
              <div className="chart-y-axis">
                <span>600</span>
                <span>450</span>
                <span>300</span>
                <span>150</span>
                <span>0</span>
              </div>

              <div className="chart-area">
                <div className="chart-grid-lines">
                  <span />
                  <span />
                  <span />
                  <span />
                  <span />
                </div>

                <div className="chart-bars">
                  {demandTrend.map((item) => {
                    const value =
                      item.actual ?? item.forecast ?? 0;

                    const height = Math.max(
                      8,
                      (value / 650) * 100
                    );

                    const isForecast =
                      item.actual === null &&
                      item.forecast !== null;

                    return (
                      <div
                        className="chart-column"
                        key={item.date}
                      >
                        <div
                          className={`chart-bar ${
                            isForecast
                              ? "forecast-bar"
                              : "actual-bar"
                          }`}
                          style={{
                            height: `${height}%`,
                          }}
                          title={`${item.date}: ${value} units`}
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

            <div className="chart-legend">
              <span>
                <i className="legend-dot actual" />
                Historical Demand
              </span>

              <span>
                <i className="legend-dot forecast" />
                Forecasted Demand
              </span>
            </div>
          </div>

          {/* Inventory Health */}

          <div className="dashboard-panel inventory-panel">
            <div className="panel-header">
              <div>
                <h2>Inventory Health</h2>

                <p>
                  Current inventory intelligence
                </p>
              </div>

              <Link
                to="/inventory"
                className="secondary-button"
              >
                View Inventory
              </Link>
            </div>

            <div className="inventory-summary-grid">
              <div className="inventory-summary-item healthy">
                <strong>
                  {inventorySummary.healthyItems}
                </strong>

                <span>Healthy</span>
              </div>

              <div className="inventory-summary-item warning">
                <strong>
                  {inventorySummary.lowStockItems}
                </strong>

                <span>Low Stock</span>
              </div>

              <div className="inventory-summary-item danger">
                <strong>
                  {inventorySummary.stockoutRiskItems}
                </strong>

                <span>Stockout Risk</span>
              </div>

              <div className="inventory-summary-item neutral">
                <strong>
                  {inventorySummary.outOfStockItems}
                </strong>

                <span>Out of Stock</span>
              </div>
            </div>

            <div className="inventory-progress">
              <div className="progress-label">
                <span>Inventory Health</span>

                <strong>
                  {inventoryHealthPercentage}%
                </strong>
              </div>

              <div className="progress-track">
                <div
                  className="progress-fill"
                  style={{
                    width: `${inventoryHealthPercentage}%`,
                  }}
                />
              </div>
            </div>
          </div>
        </section>

        {/* =================================================
            FORECAST + ALERTS
            ================================================= */}

        <section className="dashboard-content-grid lower-grid">
          {/* Product Forecast */}

          <div className="dashboard-panel forecast-panel">
            <div className="panel-header">
              <div>
                <h2>Product Forecast</h2>

                <p>
                  Preview demand and inventory impact
                </p>
              </div>

              <select
                value={selectedProduct.id}
                onChange={(event) => {
                  setSelectedProductId(
                    Number(event.target.value)
                  );
                }}
              >
                {prototypeProducts.map((product) => (
                  <option
                    key={product.id}
                    value={product.id}
                  >
                    {product.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="selected-product">
              <div>
                <h3>
                  {selectedProduct.name}
                </h3>

                <span>
                  {selectedProduct.category}
                </span>
              </div>

              <StatusBadge
                status={selectedProduct.status}
              />
            </div>

            <div className="forecast-metrics">
              <div>
                <span>Current Stock</span>

                <strong>
                  {selectedForecast.stock}
                </strong>
              </div>

              <div>
                <span>Predicted Demand</span>

                <strong>
                  {selectedForecast.demand}
                </strong>
              </div>

              <div>
                <span>Projected Stock</span>

                <strong
                  className={
                    selectedForecast.projectedStock < 0
                      ? "danger-text"
                      : ""
                  }
                >
                  {selectedForecast.projectedStock}
                </strong>
              </div>

              <div>
                <span>Recommended Reorder</span>

                <strong>
                  {selectedForecast.reorder}
                </strong>
              </div>
            </div>

            <div className="forecast-footer">
              <div>
                <span>Risk Level</span>

                <RiskBadge
                  risk={selectedProduct.risk}
                />
              </div>

              <Link
                className="primary-button"
                to="/forecast"
              >
                View Forecast
              </Link>
            </div>
          </div>

          {/* Priority Alerts */}

          <div className="dashboard-panel alerts-panel">
            <div className="panel-header">
              <div>
                <h2>Priority Alerts</h2>

                <p>
                  Items requiring attention
                </p>
              </div>

              <span className="alert-count">
                {alerts.length}
              </span>
            </div>

            <div className="alerts-list">
              {alerts.map((alert) => (
                <div
                  className="alert-item"
                  key={alert.id}
                >
                  <div
                    className={`alert-icon ${alert.severity.toLowerCase()}`}
                  >
                    !
                  </div>

                  <div className="alert-content">
                    <div className="alert-title-row">
                      <strong>
                        {alert.product}
                      </strong>

                      <span
                        className={`severity ${alert.severity.toLowerCase()}`}
                      >
                        {alert.severity}
                      </span>
                    </div>

                    <p>
                      {alert.message}
                    </p>

                    <span className="alert-action">
                      {alert.action}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <Link
              className="secondary-button full-width"
              to="/alerts"
            >
              View All Alerts
            </Link>
          </div>
        </section>

        {/* =================================================
            QUICK ACTIONS
            ================================================= */}

        <section
          className="dashboard-panel"
          style={{
            marginTop: "20px",
            padding: "18px 20px",
          }}
        >
          <div className="panel-header">
            <div>
              <h2>Quick Actions</h2>

              <p>
                Move directly to the areas that need attention.
              </p>
            </div>
          </div>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "10px",
              paddingTop: "15px",
            }}
          >
            <Link
              to="/forecast"
              className="primary-button"
            >
              View Demand Forecast
            </Link>

            <Link
              to="/inventory"
              className="secondary-button"
            >
              Check Inventory
            </Link>

            <Link
              to="/alerts"
              className="secondary-button"
            >
              Review Alerts
            </Link>

            <Link
              to="/investor"
              className="secondary-button"
            >
              Financial Dashboard
            </Link>
          </div>
        </section>
      </main>
    </div>
  );
}