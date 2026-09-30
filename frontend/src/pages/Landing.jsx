import React from "react";
import { Link } from "react-router-dom";

function Landing() {
  return (
    <div className="landing-page">
      {/* =====================================================
          NAVBAR
      ====================================================== */}

      <header className="landing-navbar">
        <div className="landing-brand">
          <div className="landing-brand-mark">D</div>

          <div>
            <h2>DemandIQ</h2>
            <span>Intelligent Decisions</span>
          </div>
        </div>

        <div className="landing-nav-actions">
          <Link
            to="/login"
            className="landing-login-link"
          >
            Sign In
          </Link>

          <Link
            to="/login"
            className="landing-nav-button"
          >
            Get Started
          </Link>
        </div>
      </header>


      {/* =====================================================
          HERO SECTION
      ====================================================== */}

      <main className="landing-main">

        <section className="landing-hero">

          <div className="landing-hero-content">

            <div className="landing-badge">
              <span></span>
              Intelligent Demand Forecasting
            </div>

            <h1>
              Make Smarter Decisions
              <br />
              <span>Before Demand Happens.</span>
            </h1>

            <p>
              DemandIQ helps businesses understand demand,
              forecast future requirements and make better
              inventory decisions using intelligent analytics.
            </p>

            <div className="landing-hero-actions">

              <Link
                to="/login"
                className="landing-primary-button"
              >
                Enter the Platform
                <span>→</span>
              </Link>

              <a
                href="#features"
                className="landing-secondary-button"
              >
                Explore Platform
              </a>

            </div>

            <div className="landing-trust-row">

              <div>
                <span className="trust-icon">✓</span>
                AI-powered insights
              </div>

              <div>
                <span className="trust-icon">✓</span>
                Demand forecasting
              </div>

              <div>
                <span className="trust-icon">✓</span>
                Inventory intelligence
              </div>

            </div>

          </div>


          {/* =================================================
              HERO VISUAL
          ================================================== */}

          <div className="landing-hero-visual">

            <div className="landing-glow"></div>

            <div className="landing-dashboard-preview">

              <div className="preview-topbar">

                <div className="preview-brand">
                  <div className="preview-logo">D</div>

                  <div>
                    <strong>DemandIQ</strong>
                    <span>Business Intelligence</span>
                  </div>
                </div>

                <div className="preview-status">
                  <span></span>
                  Live
                </div>

              </div>


              <div className="preview-content">

                <div className="preview-heading">
                  <div>
                    <span>BUSINESS OVERVIEW</span>
                    <h3>Demand Intelligence</h3>
                  </div>

                  <div className="preview-date">
                    September 2026
                  </div>
                </div>


                {/* STAT CARDS */}

                <div className="preview-stats">

                  <div className="preview-stat-card">
                    <span>Total Products</span>
                    <strong>95</strong>
                    <small>+8.4% this month</small>
                  </div>

                  <div className="preview-stat-card">
                    <span>Forecasted Demand</span>
                    <strong>244</strong>
                    <small>Next 7 days</small>
                  </div>

                  <div className="preview-stat-card">
                    <span>Inventory</span>
                    <strong>293</strong>
                    <small>Units available</small>
                  </div>

                </div>


                {/* CHART */}

                <div className="preview-chart-card">

                  <div className="preview-chart-header">
                    <div>
                      <strong>Demand Trend</strong>
                      <span>Actual vs Forecast</span>
                    </div>

                    <div className="preview-chart-value">
                      +18.4%
                    </div>
                  </div>

                  <div className="preview-chart">

                    <div className="chart-grid-line line-1"></div>
                    <div className="chart-grid-line line-2"></div>
                    <div className="chart-grid-line line-3"></div>
                    <div className="chart-grid-line line-4"></div>

                    <div className="chart-line chart-line-one"></div>
                    <div className="chart-line chart-line-two"></div>

                    <div className="chart-point point-1"></div>
                    <div className="chart-point point-2"></div>
                    <div className="chart-point point-3"></div>
                    <div className="chart-point point-4"></div>
                    <div className="chart-point point-5"></div>
                    <div className="chart-point point-6"></div>

                  </div>

                </div>


                {/* ALERT */}

                <div className="preview-alert">

                  <div className="preview-alert-icon">
                    !
                  </div>

                  <div>
                    <strong>Inventory Alert</strong>
                    <span>
                      Wireless Headphones may require
                      replenishment soon.
                    </span>
                  </div>

                  <span className="preview-alert-action">
                    Review →
                  </span>

                </div>

              </div>

            </div>

          </div>

        </section>


        {/* =====================================================
            FEATURES
        ====================================================== */}

        <section
          id="features"
          className="landing-features"
        >

          <div className="landing-section-heading">

            <span>WHY DEMANDIQ</span>

            <h2>
              Turn Data Into
              <br />
              <strong>Better Decisions.</strong>
            </h2>

            <p>
              A smarter way to understand what your business
              needs today and what it may need tomorrow.
            </p>

          </div>


          <div className="landing-feature-grid">

            <div className="landing-feature-card">

              <div className="feature-icon">
                ↗
              </div>

              <h3>Demand Forecasting</h3>

              <p>
                Understand upcoming demand patterns and
                prepare your business before changes happen.
              </p>

            </div>


            <div className="landing-feature-card">

              <div className="feature-icon">
                ◫
              </div>

              <h3>Inventory Intelligence</h3>

              <p>
                Identify stock risks and make informed
                replenishment decisions using intelligent
                insights.
              </p>

            </div>


            <div className="landing-feature-card">

              <div className="feature-icon">
                ◈
              </div>

              <h3>Business Analytics</h3>

              <p>
                Transform business data into clear,
                actionable information through intuitive
                analytics.
              </p>

            </div>


            <div className="landing-feature-card">

              <div className="feature-icon">
                $
              </div>

              <h3>Financial Intelligence</h3>

              <p>
                Explore market information and monitor
                investment positions from one workspace.
              </p>

            </div>

          </div>

        </section>


        {/* =====================================================
            CTA
        ====================================================== */}

        <section className="landing-cta">

          <div>

            <span>READY TO GET STARTED?</span>

            <h2>
              Make your next decision
              <br />
              <strong>with intelligence.</strong>
            </h2>

            <p>
              Bring your business data and decisions together
              with DemandIQ.
            </p>

          </div>

          <Link
            to="/login"
            className="landing-cta-button"
          >
            Enter the Platform
            <span>→</span>
          </Link>

        </section>

      </main>


      {/* =====================================================
          FOOTER
      ====================================================== */}

      <footer className="landing-footer">

        <div className="landing-footer-brand">

          <div className="landing-brand-mark">
            D
          </div>

          <div>
            <strong>DemandIQ</strong>
            <span>
              Intelligent Decisions
            </span>
          </div>

        </div>

        <span>
          © 2026 DemandIQ. Intelligent decisions,
          powered by data.
        </span>

      </footer>

    </div>
  );
}

export default Landing;