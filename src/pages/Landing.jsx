```jsx
import { ArrowRight, BarChart3, Boxes, TrendingUp } from "lucide-react";
import { useNavigate } from "react-router-dom";

function Landing() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      <header className="landing-header">
        <div className="landing-logo">
          <div className="brand-mark">D</div>

          <div>
            <strong>DemandIQ</strong>
            <span>Intelligent Business Intelligence</span>
          </div>
        </div>

        <button
          className="header-login-button"
          onClick={() => navigate("/login")}
        >
          Sign In
        </button>
      </header>

      <main>
        <section className="hero-section">
          <div className="hero-content">
            <div className="hero-badge">
              Intelligent Demand & Market Analytics
            </div>

            <h1>
              Make smarter decisions with
              <span> DemandIQ.</span>
            </h1>

            <p>
              A unified platform for demand forecasting, inventory
              intelligence, and financial market analytics.
            </p>
```
