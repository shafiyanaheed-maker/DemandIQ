import { useNavigate } from "react-router-dom";

function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <nav className="navbar">
        <div className="logo">DemandIQ</div>

        <button
          className="login-button"
          onClick={() => navigate("/login")}
        >
          Login
        </button>
      </nav>

      <main className="hero">
        <div className="hero-content">
          <p className="eyebrow">AI-POWERED BUSINESS INTELLIGENCE</p>

          <h1>
            Predict demand.
            <br />
            <span>Make smarter decisions.</span>
          </h1>

          <p className="hero-text">
            DemandIQ helps businesses understand demand, manage inventory,
            forecast future sales, and make data-driven decisions.
          </p>

          <button
            className="primary-button"
            onClick={() => navigate("/login")}
          >
            Get Started →
          </button>
        </div>

        <div className="hero-card">
          <div className="card-header">
            <span>Demand Forecast</span>
            <span className="status">Live</span>
          </div>

          <div className="chart">
            <div className="bar bar-1"></div>
            <div className="bar bar-2"></div>
            <div className="bar bar-3"></div>
            <div className="bar bar-4"></div>
            <div className="bar bar-5"></div>
            <div className="bar bar-6"></div>
          </div>

          <div className="forecast-value">
            <strong>+24.8%</strong>
            <span>Expected demand growth</span>
          </div>
        </div>
      </main>

      <section className="features">
        <div>
          <h3>Demand Forecasting</h3>
          <p>Predict future product demand using historical data.</p>
        </div>

        <div>
          <h3>Inventory Intelligence</h3>
          <p>Identify stock risks and recommended reorder quantities.</p>
        </div>

        <div>
          <h3>Market Insights</h3>
          <p>Track market information and investment activity.</p>
        </div>
      </section>
    </div>
  );
}

export default Landing;