import { Link, useLocation } from "react-router-dom";
import {
  alerts,
  dashboardStats,
  inventorySummary,
  prototypeProducts,
} from "../data/prototypeData";

const pageData = {
  inventory: {
    title: "Inventory",
    subtitle: "Monitor stock levels and inventory health.",
  },
  analytics: {
    title: "Analytics",
    subtitle: "Review business performance and demand insights.",
  },
  alerts: {
    title: "Alerts",
    subtitle: "Review inventory conditions requiring attention.",
  },
  portfolio: {
    title: "Portfolio",
    subtitle: "Track your investment portfolio and holdings.",
  },
  transactions: {
    title: "Transactions",
    subtitle: "Review recent investment transactions.",
  },
};

function ModulePage() {
  const location = useLocation();

  const pageKey = location.pathname.replace("/", "");

  const currentPage =
    pageData[pageKey] || {
      title: "DemandIQ",
      subtitle: "Intelligent business decisions.",
    };

  const isBusinessPage = [
    "inventory",
    "analytics",
    "alerts",
  ].includes(pageKey);

  const isFinancialPage = [
    "portfolio",
    "transactions",
  ].includes(pageKey);

  return (
    <div className="module-page">
      {/* =====================================================
          SIDEBAR
          ===================================================== */}

      <aside className="module-sidebar">
        <div className="module-brand">
          <div className="module-brand-mark">D</div>

          <div>
            <strong>DemandIQ</strong>
            <span>Intelligent Decisions</span>
          </div>
        </div>

        <nav className="module-nav">
          {/* BUSINESS */}

          <Link
            to="/dashboard"
            className={
              location.pathname === "/dashboard"
                ? "module-nav-item active"
                : "module-nav-item"
            }
          >
            <span>▦</span>
            Dashboard
          </Link>

          <Link
            to="/forecast"
            className="module-nav-item"
          >
            <span>⌁</span>
            Forecast
          </Link>

          <Link
            to="/inventory"
            className={
              pageKey === "inventory"
                ? "module-nav-item active"
                : "module-nav-item"
            }
          >
            <span>▣</span>
            Inventory
          </Link>

          <Link
            to="/analytics"
            className={
              pageKey === "analytics"
                ? "module-nav-item active"
                : "module-nav-item"
            }
          >
            <span>◫</span>
            Analytics
          </Link>

          <Link
            to="/alerts"
            className={
              pageKey === "alerts"
                ? "module-nav-item active"
                : "module-nav-item"
            }
          >
            <span>!</span>
            Alerts

            <span className="module-alert-count">
              {alerts.length}
            </span>
          </Link>

          <div className="module-section-title">
            FINANCIAL
          </div>

          <Link
            to="/investor"
            className="module-nav-item"
          >
            <span>↗</span>
            Financial Stocks
          </Link>

          <Link
            to="/portfolio"
            className={
              pageKey === "portfolio"
                ? "module-nav-item active"
                : "module-nav-item"
            }
          >
            <span>◉</span>
            Portfolio
          </Link>

          <Link
            to="/transactions"
            className={
              pageKey === "transactions"
                ? "module-nav-item active"
                : "module-nav-item"
            }
          >
            <span>↔</span>
            Transactions
          </Link>
        </nav>

        <div className="module-sidebar-bottom">
          <button
            className="module-logout"
            onClick={() => {
              window.location.href = "/";
            }}
          >
            <span>↪</span>
            Logout
          </button>
        </div>
      </aside>

      {/* =====================================================
          MAIN
          ===================================================== */}

      <main className="module-main">
        <header className="module-header">
          <div>
            <div className="module-breadcrumb">
              DemandIQ / {currentPage.title}
            </div>

            <h1>{currentPage.title}</h1>

            <p>{currentPage.subtitle}</p>
          </div>

          <div className="module-user">
            <div className="module-avatar">
              {isFinancialPage ? "I" : "B"}
            </div>

            <div>
              <strong>
                {isFinancialPage
                  ? "Investor User"
                  : "Business User"}
              </strong>

              <span>
                {isFinancialPage
                  ? "Investor"
                  : "Business"}
              </span>
            </div>
          </div>
        </header>

        {/* =====================================================
            INVENTORY
            ===================================================== */}

        {pageKey === "inventory" && (
          <>
            <section className="module-stats">
              <div className="module-stat-card">
                <span>Total Inventory</span>
                <strong>
                  {inventorySummary.totalItems}
                </strong>
                <small>Units tracked</small>
              </div>

              <div className="module-stat-card healthy">
                <span>Healthy Items</span>
                <strong>
                  {inventorySummary.healthyItems}
                </strong>
                <small>Normal stock</small>
              </div>

              <div className="module-stat-card warning">
                <span>Low Stock</span>
                <strong>
                  {inventorySummary.lowStockItems}
                </strong>
                <small>Needs attention</small>
              </div>

              <div className="module-stat-card danger">
                <span>Stockout Risk</span>
                <strong>
                  {inventorySummary.stockoutRiskItems}
                </strong>
                <small>High priority</small>
              </div>
            </section>

            <section className="module-card">
              <div className="module-card-header">
                <div>
                  <h2>Product Inventory</h2>
                  <p>
                    Current stock and predicted demand.
                  </p>
                </div>
              </div>

              <div className="module-table-wrapper">
                <table className="module-table">
                  <thead>
                    <tr>
                      <th>Product</th>
                      <th>Category</th>
                      <th>Stock</th>
                      <th>Predicted Demand</th>
                      <th>Projected Stock</th>
                      <th>Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    {prototypeProducts.map((product) => (
                      <tr key={product.id}>
                        <td>
                          <strong>{product.name}</strong>
                        </td>

                        <td>{product.category}</td>

                        <td>{product.stock}</td>

                        <td>
                          {product.predictedDemand}
                        </td>

                        <td
                          className={
                            product.projectedStock < 0
                              ? "module-danger"
                              : ""
                          }
                        >
                          {product.projectedStock}
                        </td>

                        <td>
                          <span
                            className={`module-status ${product.status.toLowerCase()}`}
                          >
                            {product.status.replaceAll(
                              "_",
                              " "
                            )}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}

        {/* =====================================================
            ANALYTICS
            ===================================================== */}

        {pageKey === "analytics" && (
          <>
            <section className="module-stats">
              <div className="module-stat-card">
                <span>Total Products</span>
                <strong>
                  {dashboardStats.totalProducts}
                </strong>
                <small>Products tracked</small>
              </div>

              <div className="module-stat-card">
                <span>Units Sold</span>
                <strong>
                  {dashboardStats.totalUnitsSold.toLocaleString()}
                </strong>
                <small>Total recorded sales</small>
              </div>

              <div className="module-stat-card">
                <span>Revenue</span>
                <strong>
                  ₹
                  {(
                    dashboardStats.totalRevenue / 100000
                  ).toFixed(1)}
                  L
                </strong>
                <small>Total revenue</small>
              </div>

              <div className="module-stat-card">
                <span>Forecast Demand</span>
                <strong>
                  {dashboardStats.forecastedDemand}
                </strong>
                <small>Next 7 days</small>
              </div>
            </section>

            <section className="module-card">
              <div className="module-card-header">
                <div>
                  <h2>Business Analytics</h2>
                  <p>
                    Key prototype performance indicators.
                  </p>
                </div>
              </div>

              <div className="analytics-grid">
                <div className="analytics-box">
                  <span>Inventory Health</span>

                  <strong>
                    {Math.round(
                      (inventorySummary.healthyItems /
                        inventorySummary.totalItems) *
                        100
                    )}
                    %
                  </strong>

                  <div className="analytics-progress">
                    <div
                      style={{
                        width: `${
                          (inventorySummary.healthyItems /
                            inventorySummary.totalItems) *
                          100
                        }%`,
                      }}
                    />
                  </div>
                </div>

                <div className="analytics-box">
                  <span>Recommended Reorder</span>

                  <strong>
                    {inventorySummary.recommendedReorderUnits}
                  </strong>

                  <small>
                    units recommended
                  </small>
                </div>

                <div className="analytics-box">
                  <span>High Risk Items</span>

                  <strong>
                    {inventorySummary.highRiskItems}
                  </strong>

                  <small>
                    require attention
                  </small>
                </div>

                <div className="analytics-box">
                  <span>Active Alerts</span>

                  <strong>
                    {dashboardStats.activeAlerts}
                  </strong>

                  <small>
                    current alerts
                  </small>
                </div>
              </div>
            </section>
          </>
        )}

        {/* =====================================================
            ALERTS
            ===================================================== */}

        {pageKey === "alerts" && (
          <section className="module-card">
            <div className="module-card-header">
              <div>
                <h2>Active Alerts</h2>

                <p>
                  Inventory conditions requiring attention.
                </p>
              </div>

              <span className="module-alert-total">
                {alerts.length} Alerts
              </span>
            </div>

            <div className="module-alert-list">
              {alerts.map((alert) => (
                <div
                  className={`module-alert ${alert.severity.toLowerCase()}`}
                  key={alert.id}
                >
                  <div className="module-alert-icon">
                    !
                  </div>

                  <div className="module-alert-content">
                    <div>
                      <strong>
                        {alert.product}
                      </strong>

                      <span>
                        {alert.severity}
                      </span>
                    </div>

                    <p>{alert.message}</p>

                    <small>
                      Recommended: {alert.action}
                    </small>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* =====================================================
            PORTFOLIO
            ===================================================== */}

        {pageKey === "portfolio" && (
          <>
            <section className="module-stats">
              <div className="module-stat-card">
                <span>Portfolio Value</span>
                <strong>₹8.42L</strong>
                <small>Current prototype value</small>
              </div>

              <div className="module-stat-card healthy">
                <span>Total Investment</span>
                <strong>₹7.50L</strong>
                <small>Capital invested</small>
              </div>

              <div className="module-stat-card healthy">
                <span>Returns</span>
                <strong>₹92,000</strong>
                <small>Unrealized return</small>
              </div>

              <div className="module-stat-card">
                <span>Holdings</span>
                <strong>6</strong>
                <small>Stocks held</small>
              </div>
            </section>

            <section className="module-card">
              <div className="module-card-header">
                <div>
                  <h2>Portfolio Holdings</h2>
                  <p>
                    Current prototype investment positions.
                  </p>
                </div>
              </div>

              <div className="module-table-wrapper">
                <table className="module-table">
                  <thead>
                    <tr>
                      <th>Stock</th>
                      <th>Quantity</th>
                      <th>Avg. Price</th>
                      <th>Current Price</th>
                      <th>Value</th>
                      <th>Return</th>
                    </tr>
                  </thead>

                  <tbody>
                    <tr>
                      <td><strong>TCS</strong></td>
                      <td>20</td>
                      <td>₹3,420</td>
                      <td>₹3,610</td>
                      <td>₹72,200</td>
                      <td className="module-positive">+5.56%</td>
                    </tr>

                    <tr>
                      <td><strong>INFY</strong></td>
                      <td>30</td>
                      <td>₹1,480</td>
                      <td>₹1,545</td>
                      <td>₹46,350</td>
                      <td className="module-positive">+4.39%</td>
                    </tr>

                    <tr>
                      <td><strong>RELIANCE</strong></td>
                      <td>15</td>
                      <td>₹2,850</td>
                      <td>₹2,960</td>
                      <td>₹44,400</td>
                      <td className="module-positive">+3.86%</td>
                    </tr>

                    <tr>
                      <td><strong>HDFCBANK</strong></td>
                      <td>25</td>
                      <td>₹1,650</td>
                      <td>₹1,710</td>
                      <td>₹42,750</td>
                      <td className="module-positive">+3.64%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}

        {/* =====================================================
            TRANSACTIONS
            ===================================================== */}

        {pageKey === "transactions" && (
          <section className="module-card">
            <div className="module-card-header">
              <div>
                <h2>Recent Transactions</h2>
                <p>
                  Recent buying and selling activity.
                </p>
              </div>
            </div>

            <div className="module-table-wrapper">
              <table className="module-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Stock</th>
                    <th>Type</th>
                    <th>Quantity</th>
                    <th>Price</th>
                    <th>Total</th>
                  </tr>
                </thead>

                <tbody>
                  <tr>
                    <td>30 Sep 2026</td>
                    <td><strong>TCS</strong></td>
                    <td>
                      <span className="transaction-buy">
                        BUY
                      </span>
                    </td>
                    <td>10</td>
                    <td>₹3,610</td>
                    <td>₹36,100</td>
                  </tr>

                  <tr>
                    <td>28 Sep 2026</td>
                    <td><strong>INFY</strong></td>
                    <td>
                      <span className="transaction-buy">
                        BUY
                      </span>
                    </td>
                    <td>15</td>
                    <td>₹1,545</td>
                    <td>₹23,175</td>
                  </tr>

                  <tr>
                    <td>25 Sep 2026</td>
                    <td><strong>RELIANCE</strong></td>
                    <td>
                      <span className="transaction-sell">
                        SELL
                      </span>
                    </td>
                    <td>5</td>
                    <td>₹2,960</td>
                    <td>₹14,800</td>
                  </tr>

                  <tr>
                    <td>22 Sep 2026</td>
                    <td><strong>HDFCBANK</strong></td>
                    <td>
                      <span className="transaction-buy">
                        BUY
                      </span>
                    </td>
                    <td>10</td>
                    <td>₹1,710</td>
                    <td>₹17,100</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* =====================================================
            BACK BUTTON
            ===================================================== */}

        <div className="module-bottom-actions">
          {isBusinessPage && (
            <Link
              to="/dashboard"
              className="secondary-button"
            >
              ← Business Dashboard
            </Link>
          )}

          {isFinancialPage && (
            <Link
              to="/investor"
              className="secondary-button"
            >
              ← Investor Dashboard
            </Link>
          )}
        </div>
      </main>
    </div>
  );
}

export default ModulePage;