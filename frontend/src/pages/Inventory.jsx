import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  prototypeProducts,
  inventorySummary,
} from "../data/prototypeData";

function Inventory() {
  const [selectedId, setSelectedId] = useState(1);
  const [filter, setFilter] = useState("ALL");

  const selectedProduct = prototypeProducts.find(
    (product) => product.id === selectedId
  );

  const filteredProducts = useMemo(() => {
    if (filter === "ALL") {
      return prototypeProducts;
    }

    return prototypeProducts.filter(
      (product) => product.status === filter
    );
  }, [filter]);

  const getStatusLabel = (status) => {
    switch (status) {
      case "HEALTHY":
        return "Healthy";
      case "LOW_STOCK":
        return "Low Stock";
      case "REORDER_SOON":
        return "Reorder Soon";
      case "STOCKOUT_RISK":
        return "Stockout Risk";
      case "OUT_OF_STOCK":
        return "Out of Stock";
      default:
        return status;
    }
  };

  return (
    <div className="inventory-page">
      {/* Sidebar */}
      <aside className="inventory-sidebar">
        <div className="inventory-brand">
          <div className="inventory-brand-mark">D</div>

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

          <Link to="/inventory" className="active">
            <span>▤</span>
            Inventory
          </Link>

          <Link to="/analytics">
            <span>◌</span>
            Analytics
          </Link>

          <Link to="/alerts">
            <span>⚠</span>
            Alerts
            <span className="inventory-alert-count">
              {inventorySummary.highRiskItems}
            </span>
          </Link>

          <div className="inventory-nav-title">FINANCIAL</div>

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

        <div className="inventory-sidebar-bottom">
          <button
            className="inventory-logout"
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
      <main className="inventory-main">
        <header className="inventory-header">
          <div>
            <h1>Inventory Intelligence</h1>
            <p>
              Monitor stock levels, demand pressure and reorder
              requirements.
            </p>
          </div>

          <div className="inventory-user">
            <div className="inventory-avatar">B</div>

            <div>
              <strong>Business User</strong>
              <span>Inventory Manager</span>
            </div>
          </div>
        </header>

        {/* Summary Cards */}
        <section className="inventory-summary-cards">
          <div className="inventory-stat-card">
            <span>Total Inventory</span>
            <strong>{inventorySummary.totalItems}</strong>
            <small>Units currently tracked</small>
          </div>

          <div className="inventory-stat-card healthy-card">
            <span>Healthy Items</span>
            <strong>{inventorySummary.healthyItems}</strong>
            <small>Normal stock position</small>
          </div>

          <div className="inventory-stat-card warning-card">
            <span>Low Stock</span>
            <strong>{inventorySummary.lowStockItems}</strong>
            <small>Need attention</small>
          </div>

          <div className="inventory-stat-card danger-card">
            <span>Stockout Risk</span>
            <strong>{inventorySummary.stockoutRiskItems}</strong>
            <small>High priority items</small>
          </div>
        </section>

        {/* Main Grid */}
        <section className="inventory-content-grid">
          {/* Product Table */}
          <div className="inventory-panel">
            <div className="inventory-panel-header">
              <div>
                <h2>Product Inventory</h2>
                <p>
                  Current stock compared with predicted demand.
                </p>
              </div>

              <select
                value={filter}
                onChange={(event) => setFilter(event.target.value)}
              >
                <option value="ALL">All Products</option>
                <option value="HEALTHY">Healthy</option>
                <option value="LOW_STOCK">Low Stock</option>
                <option value="STOCKOUT_RISK">
                  Stockout Risk
                </option>
              </select>
            </div>

            <div className="inventory-table-wrapper">
              <table className="inventory-table">
                <thead>
                  <tr>
                    <th>Product</th>
                    <th>Stock</th>
                    <th>7-Day Demand</th>
                    <th>Projected</th>
                    <th>Status</th>
                    <th>Reorder</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredProducts.map((product) => (
                    <tr
                      key={product.id}
                      className={
                        selectedId === product.id
                          ? "selected-row"
                          : ""
                      }
                      onClick={() => setSelectedId(product.id)}
                    >
                      <td>
                        <strong>{product.name}</strong>
                        <span>{product.category}</span>
                      </td>

                      <td>{product.stock}</td>

                      <td>{product.predictedDemand}</td>

                      <td
                        className={
                          product.projectedStock < 0
                            ? "inventory-danger-text"
                            : ""
                        }
                      >
                        {product.projectedStock}
                      </td>

                      <td>
                        <span
                          className={`inventory-status ${product.status.toLowerCase()}`}
                        >
                          {getStatusLabel(product.status)}
                        </span>
                      </td>

                      <td>
                        {product.reorder > 0
                          ? `${product.reorder} units`
                          : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Product Intelligence */}
          <div className="inventory-panel inventory-detail-panel">
            <div className="inventory-panel-header">
              <div>
                <h2>Inventory Intelligence</h2>
                <p>Selected product analysis.</p>
              </div>
            </div>

            {selectedProduct && (
              <>
                <div className="inventory-selected-product">
                  <div>
                    <strong>{selectedProduct.name}</strong>
                    <span>{selectedProduct.category}</span>
                  </div>

                  <span
                    className={`inventory-status ${selectedProduct.status.toLowerCase()}`}
                  >
                    {getStatusLabel(selectedProduct.status)}
                  </span>
                </div>

                <div className="inventory-detail-grid">
                  <div>
                    <span>Current Stock</span>
                    <strong>{selectedProduct.stock}</strong>
                  </div>

                  <div>
                    <span>Predicted Demand</span>
                    <strong>{selectedProduct.predictedDemand}</strong>
                  </div>

                  <div>
                    <span>Projected Stock</span>
                    <strong
                      className={
                        selectedProduct.projectedStock < 0
                          ? "inventory-danger-text"
                          : ""
                      }
                    >
                      {selectedProduct.projectedStock}
                    </strong>
                  </div>

                  <div>
                    <span>Recommended Reorder</span>
                    <strong>
                      {selectedProduct.reorder} units
                    </strong>
                  </div>
                </div>

                <div className="inventory-risk-box">
                  <span>Risk Level</span>

                  <strong
                    className={`risk-${selectedProduct.risk.toLowerCase()}`}
                  >
                    {selectedProduct.risk}
                  </strong>
                </div>

                <div className="inventory-recommendation">
                  <span>Recommendation</span>

                  <strong>
                    {selectedProduct.reorder > 0
                      ? `Reorder ${selectedProduct.reorder} units to reduce stockout risk.`
                      : "Current inventory is sufficient for the forecast period."}
                  </strong>
                </div>
              </>
            )}
          </div>
        </section>

        {/* Inventory Health */}
        <section className="inventory-health-panel">
          <div className="inventory-panel-header">
            <div>
              <h2>Inventory Health Overview</h2>
              <p>Distribution of inventory conditions.</p>
            </div>

            <span className="inventory-health-total">
              {inventorySummary.totalItems} units
            </span>
          </div>

          <div className="inventory-health-content">
            <div className="inventory-health-bar">
              <div
                className="health-segment healthy"
                style={{
                  width: `${
                    (inventorySummary.healthyItems /
                      inventorySummary.totalItems) *
                    100
                  }%`,
                }}
              />

              <div
                className="health-segment warning"
                style={{
                  width: `${
                    (inventorySummary.lowStockItems /
                      inventorySummary.totalItems) *
                    100
                  }%`,
                }}
              />

              <div
                className="health-segment danger"
                style={{
                  width: `${
                    (inventorySummary.stockoutRiskItems /
                      inventorySummary.totalItems) *
                    100
                  }%`,
                }}
              />
            </div>

            <div className="inventory-health-legend">
              <div>
                <span className="health-dot healthy" />
                <strong>{inventorySummary.healthyItems}</strong>
                Healthy
              </div>

              <div>
                <span className="health-dot warning" />
                <strong>{inventorySummary.lowStockItems}</strong>
                Low Stock
              </div>

              <div>
                <span className="health-dot danger" />
                <strong>{inventorySummary.stockoutRiskItems}</strong>
                Stockout Risk
              </div>

              <div>
                <span className="health-dot neutral" />
                <strong>{inventorySummary.reorderSoonItems}</strong>
                Reorder Soon
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Inventory;