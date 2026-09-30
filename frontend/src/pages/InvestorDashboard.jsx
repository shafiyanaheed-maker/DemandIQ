import React, { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const stocks = [
  {
    symbol: "RELIANCE",
    name: "Reliance Industries",
    sector: "Energy",
    price: 2948.45,
    change: 2.34,
    volume: "8.42M",
    marketCap: "₹19.96T",
  },
  {
    symbol: "TCS",
    name: "Tata Consultancy Services",
    sector: "Technology",
    price: 4215.8,
    change: 1.72,
    volume: "3.18M",
    marketCap: "₹15.28T",
  },
  {
    symbol: "INFY",
    name: "Infosys",
    sector: "Technology",
    price: 1892.3,
    change: -0.64,
    volume: "5.72M",
    marketCap: "₹7.84T",
  },
  {
    symbol: "HDFCBANK",
    name: "HDFC Bank",
    sector: "Banking",
    price: 1768.55,
    change: 0.91,
    volume: "6.21M",
    marketCap: "₹13.47T",
  },
  {
    symbol: "ICICIBANK",
    name: "ICICI Bank",
    sector: "Banking",
    price: 1324.7,
    change: 1.18,
    volume: "4.83M",
    marketCap: "₹9.31T",
  },
  {
    symbol: "ITC",
    name: "ITC Limited",
    sector: "FMCG",
    price: 487.25,
    change: -0.32,
    volume: "7.14M",
    marketCap: "₹6.08T",
  },
];

const portfolio = [
  {
    symbol: "RELIANCE",
    name: "Reliance Industries",
    shares: 24,
    avgPrice: 2740,
    currentPrice: 2948.45,
  },
  {
    symbol: "TCS",
    name: "Tata Consultancy Services",
    shares: 12,
    avgPrice: 3950,
    currentPrice: 4215.8,
  },
  {
    symbol: "HDFCBANK",
    name: "HDFC Bank",
    shares: 30,
    avgPrice: 1645,
    currentPrice: 1768.55,
  },
];

function InvestorDashboard() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [selectedSector, setSelectedSector] = useState("All");
  const [activeTab, setActiveTab] = useState("Stocks");

  const sectors = [
    "All",
    "Technology",
    "Banking",
    "Energy",
    "FMCG",
  ];

  const filteredStocks = useMemo(() => {
    return stocks.filter((stock) => {
      const searchText = search.toLowerCase();

      const matchesSearch =
        stock.symbol.toLowerCase().includes(searchText) ||
        stock.name.toLowerCase().includes(searchText);

      const matchesSector =
        selectedSector === "All" ||
        stock.sector === selectedSector;

      return matchesSearch && matchesSector;
    });
  }, [search, selectedSector]);

  const handleAction = (action, stock) => {
    alert(
      `${action} ${stock.symbol} — Demo action for prototype`
    );
  };

  return (
    <div className="investor-page">
      {/* =====================================================
          SIDEBAR
      ====================================================== */}

      <aside className="investor-sidebar">
        <div className="investor-brand">
          <div className="investor-brand-mark">D</div>

          <div>
            <h2>DemandIQ</h2>
            <span>Intelligent Decisions</span>
          </div>
        </div>

        <div className="investor-profile">
          <div className="investor-avatar">A</div>

          <div>
            <strong>Investor</strong>
            <span>Financial Workspace</span>
          </div>
        </div>

        <nav className="investor-nav">
          <div className="investor-nav-label">
            MAIN
          </div>

          <Link
            to="/dashboard"
            className="investor-nav-item"
          >
            <span>⌂</span>
            Dashboard
          </Link>

          <Link
            to="/forecast"
            className="investor-nav-item"
          >
            <span>⌁</span>
            Forecast
          </Link>

          <Link
            to="/inventory"
            className="investor-nav-item"
          >
            <span>▣</span>
            Inventory
          </Link>

          <Link
            to="/analytics"
            className="investor-nav-item"
          >
            <span>◫</span>
            Analytics
          </Link>

          <Link
            to="/alerts"
            className="investor-nav-item"
          >
            <span>⚠</span>
            Alerts
          </Link>

          <div className="investor-nav-label">
            FINANCIAL
          </div>

          <Link
            to="/investor"
            className="investor-nav-item active"
          >
            <span>↗</span>
            Financial Stocks
          </Link>

          <Link
            to="/portfolio"
            className="investor-nav-item"
          >
            <span>▤</span>
            Portfolio
          </Link>

          <Link
            to="/transactions"
            className="investor-nav-item"
          >
            <span>↔</span>
            Transactions
          </Link>

          <div className="investor-nav-label">
            ADMINISTRATION
          </div>

          <Link
            to="/admin"
            className="investor-nav-item"
          >
            <span>⚙</span>
            Admin Panel
          </Link>
        </nav>

        <button
          className="investor-logout"
          onClick={() => navigate("/")}
        >
          <span>⇥</span>
          Logout
        </button>
      </aside>

      {/* =====================================================
          MAIN CONTENT
      ====================================================== */}

      <main className="investor-main">
        {/* HEADER */}

        <header className="investor-header">
          <div>
            <div className="investor-breadcrumb">
              DemandIQ <span>/</span> Financial
            </div>

            <h1>Financial Stocks</h1>

            <p>
              Track market movements, monitor stocks and
              manage your investment intelligence.
            </p>
          </div>

          <div className="investor-header-actions">
            <div className="market-status">
              <span className="status-dot"></span>
              Market Open
            </div>

            <button
              className="investor-refresh"
              onClick={() =>
                alert("Market data refreshed")
              }
            >
              ↻ Refresh
            </button>
          </div>
        </header>

        {/* MARKET CARDS */}

        <section className="investor-market-cards">
          <div className="market-card">
            <div className="market-card-top">
              <span>NIFTY 50</span>
              <span className="positive">
                +0.84%
              </span>
            </div>

            <strong>24,315.95</strong>

            <small>+203.40 today</small>
          </div>

          <div className="market-card">
            <div className="market-card-top">
              <span>SENSEX</span>
              <span className="positive">
                +0.72%
              </span>
            </div>

            <strong>79,802.79</strong>

            <small>+568.42 today</small>
          </div>

          <div className="market-card">
            <div className="market-card-top">
              <span>BANK NIFTY</span>
              <span className="positive">
                +0.58%
              </span>
            </div>

            <strong>52,184.25</strong>

            <small>+301.75 today</small>
          </div>

          <div className="market-card">
            <div className="market-card-top">
              <span>YOUR PORTFOLIO</span>
              <span className="positive">
                +12.27%
              </span>
            </div>

            <strong>₹8.42L</strong>

            <small>+₹92,000 overall</small>
          </div>
        </section>

        {/* MAIN CONTENT GRID */}

        <section className="investor-content-grid">
          {/* STOCK TABLE */}

          <div className="investor-panel stocks-panel">
            <div className="panel-header">
              <div>
                <h2>Market Stocks</h2>
                <p>
                  Explore selected market instruments
                </p>
              </div>

              <div className="stock-count">
                {filteredStocks.length} Stocks
              </div>
            </div>

            <div className="stock-toolbar">
              <div className="stock-search">
                <span>⌕</span>

                <input
                  type="text"
                  placeholder="Search stocks..."
                  value={search}
                  onChange={(event) =>
                    setSearch(event.target.value)
                  }
                />
              </div>

              <select
                value={selectedSector}
                onChange={(event) =>
                  setSelectedSector(
                    event.target.value
                  )
                }
              >
                {sectors.map((sector) => (
                  <option
                    key={sector}
                    value={sector}
                  >
                    {sector}
                  </option>
                ))}
              </select>
            </div>

            <div className="stock-table-wrapper">
              <table className="stock-table">
                <thead>
                  <tr>
                    <th>STOCK</th>
                    <th>PRICE</th>
                    <th>CHANGE</th>
                    <th>VOLUME</th>
                    <th>MARKET CAP</th>
                    <th>ACTION</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredStocks.map((stock) => (
                    <tr key={stock.symbol}>
                      <td>
                        <div className="stock-name-cell">
                          <div className="stock-logo">
                            {stock.symbol.charAt(0)}
                          </div>

                          <div>
                            <strong>
                              {stock.symbol}
                            </strong>

                            <span>
                              {stock.name}
                            </span>
                          </div>
                        </div>
                      </td>

                      <td>
                        <strong>
                          ₹
                          {stock.price.toLocaleString(
                            "en-IN",
                            {
                              minimumFractionDigits: 2,
                            }
                          )}
                        </strong>
                      </td>

                      <td>
                        <span
                          className={
                            stock.change >= 0
                              ? "stock-change positive"
                              : "stock-change negative"
                          }
                        >
                          {stock.change >= 0
                            ? "+"
                            : ""}
                          {stock.change}%
                        </span>
                      </td>

                      <td>{stock.volume}</td>

                      <td>{stock.marketCap}</td>

                      <td>
                        <div className="stock-actions">
                          <button
                            className="buy-btn"
                            onClick={() =>
                              handleAction(
                                "Buy",
                                stock
                              )
                            }
                          >
                            Buy
                          </button>

                          <button
                            className="sell-btn"
                            onClick={() =>
                              handleAction(
                                "Sell",
                                stock
                              )
                            }
                          >
                            Sell
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {filteredStocks.length === 0 && (
                <div className="empty-stocks">
                  No stocks found for your search.
                </div>
              )}
            </div>
          </div>

          {/* RIGHT COLUMN */}

          <div className="investor-right-column">
            {/* WATCHLIST */}

            <div className="investor-panel watchlist-panel">
              <div className="panel-header">
                <div>
                  <h2>Watchlist</h2>
                  <p>
                    Stocks you're monitoring
                  </p>
                </div>

                <button
                  className="view-all-btn"
                  onClick={() =>
                    setSearch("")
                  }
                >
                  View all
                </button>
              </div>

              <div className="watchlist">
                {stocks
                  .slice(0, 4)
                  .map((stock) => (
                    <div
                      className="watchlist-row"
                      key={stock.symbol}
                    >
                      <div className="watchlist-info">
                        <div className="mini-stock-logo">
                          {stock.symbol.charAt(0)}
                        </div>

                        <div>
                          <strong>
                            {stock.symbol}
                          </strong>

                          <span>
                            {stock.sector}
                          </span>
                        </div>
                      </div>

                      <div className="watchlist-price">
                        <strong>
                          ₹
                          {stock.price.toLocaleString(
                            "en-IN",
                            {
                              maximumFractionDigits: 2,
                            }
                          )}
                        </strong>

                        <span
                          className={
                            stock.change >= 0
                              ? "positive"
                              : "negative"
                          }
                        >
                          {stock.change >= 0
                            ? "+"
                            : ""}
                          {stock.change}%
                        </span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            {/* PORTFOLIO SUMMARY */}

            <div className="investor-panel portfolio-summary">
              <div className="panel-header">
                <div>
                  <h2>
                    Portfolio Summary
                  </h2>

                  <p>
                    Current investment position
                  </p>
                </div>
              </div>

              <div className="portfolio-value">
                <span>Total Value</span>

                <strong>₹8,42,000</strong>

                <small className="positive">
                  +₹92,000 (+12.27%)
                </small>
              </div>

              <div className="portfolio-stats">
                <div>
                  <span>Invested</span>
                  <strong>
                    ₹7,50,000
                  </strong>
                </div>

                <div>
                  <span>Holdings</span>
                  <strong>6</strong>
                </div>
              </div>

              <Link
                to="/portfolio"
                className="portfolio-btn"
              >
                View Portfolio
                <span>→</span>
              </Link>
            </div>
          </div>
        </section>

        {/* HOLDINGS */}

        <section className="investor-panel holdings-panel">
          <div className="panel-header">
            <div>
              <h2>Top Holdings</h2>

              <p>
                Your current stock positions
              </p>
            </div>

            <div className="holdings-tabs">
              <button
                className={
                  activeTab === "Stocks"
                    ? "active"
                    : ""
                }
                onClick={() =>
                  setActiveTab("Stocks")
                }
              >
                Stocks
              </button>

              <button
                className={
                  activeTab === "Performance"
                    ? "active"
                    : ""
                }
                onClick={() =>
                  setActiveTab(
                    "Performance"
                  )
                }
              >
                Performance
              </button>
            </div>
          </div>

          {activeTab === "Stocks" ? (
            <div className="holdings-grid">
              {portfolio.map((item) => {
                const profit =
                  (item.currentPrice -
                    item.avgPrice) *
                  item.shares;

                const profitPercent =
                  ((item.currentPrice -
                    item.avgPrice) /
                    item.avgPrice) *
                  100;

                return (
                  <div
                    className="holding-card"
                    key={item.symbol}
                  >
                    <div className="holding-top">
                      <div className="stock-name-cell">
                        <div className="stock-logo">
                          {item.symbol.charAt(0)}
                        </div>

                        <div>
                          <strong>
                            {item.symbol}
                          </strong>

                          <span>
                            {item.name}
                          </span>
                        </div>
                      </div>

                      <span className="holding-tag">
                        {item.shares} Shares
                      </span>
                    </div>

                    <div className="holding-details">
                      <div>
                        <span>
                          Avg. Price
                        </span>

                        <strong>
                          ₹
                          {item.avgPrice.toLocaleString(
                            "en-IN"
                          )}
                        </strong>
                      </div>

                      <div>
                        <span>Current</span>

                        <strong>
                          ₹
                          {item.currentPrice.toLocaleString(
                            "en-IN"
                          )}
                        </strong>
                      </div>

                      <div>
                        <span>Returns</span>

                        <strong className="positive">
                          +₹
                          {profit.toLocaleString(
                            "en-IN"
                          )}
                        </strong>
                      </div>
                    </div>

                    <div className="holding-progress">
                      <div
                        style={{
                          width: `${Math.min(
                            Math.max(
                              profitPercent * 5,
                              15
                            ),
                            100
                          )}%`,
                        }}
                      ></div>
                    </div>

                    <span className="holding-return">
                      +
                      {profitPercent.toFixed(
                        2
                      )}
                      % return
                    </span>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="performance-message">
              <div className="performance-icon">
                ↗
              </div>

              <h3>
                Portfolio Performance
              </h3>

              <p>
                Your portfolio has generated
                a total return of
                <strong> +12.27%</strong> based
                on the static prototype data.
              </p>
            </div>
          )}
        </section>

        {/* QUICK ACTIONS */}

        <section className="quick-actions">
          <button
            onClick={() =>
              alert("Buy Stock demo opened")
            }
          >
            <span>+</span>

            <div>
              <strong>Buy Stock</strong>
              <small>
                Place a demo buy order
              </small>
            </div>
          </button>

          <button
            onClick={() =>
              alert("Sell Stock demo opened")
            }
          >
            <span>−</span>

            <div>
              <strong>Sell Stock</strong>
              <small>
                Place a demo sell order
              </small>
            </div>
          </button>

          <Link to="/portfolio">
            <span>▤</span>

            <div>
              <strong>Portfolio</strong>
              <small>
                View your holdings
              </small>
            </div>
          </Link>

          <Link to="/transactions">
            <span>↔</span>

            <div>
              <strong>Transactions</strong>
              <small>
                View transaction history
              </small>
            </div>
          </Link>
        </section>
      </main>
    </div>
  );
}

export default InvestorDashboard;