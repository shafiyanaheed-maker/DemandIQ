import { useState } from "react";
import { Link } from "react-router-dom";
import { alerts, inventorySummary } from "../data/prototypeData";

function Alerts() {
  const [filter, setFilter] = useState("ALL");

  const filteredAlerts =
    filter === "ALL"
      ? alerts
      : alerts.filter((alert) => alert.severity === filter);

  return (
    <div className="alerts-page">
      {/* Sidebar */}
      <aside className="alerts-sidebar">
        <div className="alerts-brand">
          <div className="alerts-brand-mark">D</div>

          <div>
            <strong>DemandIQ</strong>
            <span>Intelligent Decisions</span>
          </div>
        </div>

        <nav>
          <Link to="/dashboard">
            <span>▦</span>
            Dashboard
          </Link>

          <Link to="/forecast">
            <span>◫</span>
            Forecast
          </Link>

          <Link to="/inventory">
            <span>▤</span>
            Inventory
          </Link>

          <Link to="/analytics">
            <span>◌</span>
            Analytics
          </Link>

          <Link to="/alerts" className="active">
            <span>⚠</span>
            Alerts
            <span className="alerts-count">
              {inventorySummary.highRiskItems}
            </span>
          </Link>

          <div className="alerts-nav-title">FINANCIAL</div>

          <Link to="/stocks">
            <span>↗</span>
            Financial Stocks
          </Link>

          <Link to="/portfolio">
            <span>◉</span>
            Portfolio
          </Link>

          <Link to="/transactions">
            <span>↔</span>
            Transactions
          </Link>
        </nav>

        <div className="alerts-sidebar-bottom">
          <button
            className="alerts-logout"
            onClick={() => {
              window.location.href = "/login";
            }}
          >
            <span>↪</span>
            Logout
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="alerts-main">
        <header className="alerts-header">
          <div>
            <h1>Inventory Alerts</h1>
            <p>
              Review important inventory conditions and recommended
              actions.
            </p>
          </div>

          <div className="alerts-user">
            <div className="alerts-avatar">B</div>

            <div>
              <strong>Business User</strong>
              <span>Inventory Manager</span>
            </div>
          </div>
        </header>

        {/* Alert Summary */}
        <section className="alerts-summary-grid">
          <div className="alerts-summary-card">
            <span>Total Alerts</span>
            <strong>{alerts.length}</strong>
            <small>Current prototype alerts</small>
          </div>

          <div className="alerts-summary-card high">
            <span>High Priority</span>
            <strong>
              {alerts.filter(
                (alert) => alert.severity === "HIGH"
              ).length}
            </strong>
            <small>Immediate attention</small>
          </div>

          <div className="alerts-summary-card medium">
            <span>Medium Priority</span>
            <strong>
              {alerts.filter(
                (alert) => alert.severity === "MEDIUM"
              ).length}
            </strong>
            <small>Monitor closely</small>
          </div>

          <div className="alerts-summary-card">
            <span>Reorder Units</span>
            <strong>{inventorySummary.recommendedReorderUnits}</strong>
            <small>Recommended inventory action</small>
          </div>
        </section>

        {/* Alerts Panel */}
        <section className="alerts-panel">
          <div className="alerts-panel-header">
            <div>
              <h2>Active Alerts</h2>
              <p>
                DemandIQ detected the following inventory conditions.
              </p>
            </div>

            <div className="alerts-filter">
              <button
                className={filter === "ALL" ? "active" : ""}
                onClick={() => setFilter("ALL")}
              >
                All
              </button>

              <button
                className={filter === "HIGH" ? "active" : ""}
                onClick={() => setFilter("HIGH")}
              >
                High
              </button>

              <button
                className={filter === "MEDIUM" ? "active" : ""}
                onClick={() => setFilter("MEDIUM")}
              >
                Medium
              </button>
            </div>
          </div>

          <div className="alerts-list-page">
            {filteredAlerts.map((alert) => (
              <div
                className={`alert-card-page ${alert.severity.toLowerCase()}`}
                key={alert.id}
              >
                <div
                  className={`alert-page-icon ${alert.severity.toLowerCase()}`}
                >
                  {alert.severity === "HIGH" ? "!" : "⚠"}
                </div>

                <div className="alert-page-content">
                  <div className="alert-page-top">
                    <div>
                      <span className="alert-type">
                        {alert.type.replaceAll("_", " ")}
                      </span>

                      <h3>{alert.product}</h3>
                    </div>

                    <span
                      className={`alert-severity ${alert.severity.toLowerCase()}`}
                    >
                      {alert.severity}
                    </span>
                  </div>

                  <p>{alert.message}</p>

                  <div className="alert-page-footer">
                    <span>Recommended Action</span>

                    <strong>{alert.action}</strong>
                  </div>
                </div>
              </div>
            ))}

            {filteredAlerts.length === 0 && (
              <div className="alerts-empty">
                No alerts found for this filter.
              </div>
            )}
          </div>
        </section>

        {/* Alert Explanation */}
        <section className="alert-info-panel">
          <div className="alert-info-icon">i</div>

          <div>
            <h3>How DemandIQ generates alerts</h3>
            <p>
              Alerts are based on the relationship between current
              inventory, predicted demand and projected stock levels.
              Products with elevated stockout risk are highlighted so
              business users can take action before inventory is
              depleted.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Alerts;