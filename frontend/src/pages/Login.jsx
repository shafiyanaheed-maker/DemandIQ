import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Login() {
  const navigate = useNavigate();

  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();

    // Static prototype login
    // Any User ID and Password will continue to the dashboard.
    navigate("/dashboard");
  };

  return (
    <div className="login-page">

      {/* =====================================================
          LEFT SIDE
      ====================================================== */}

      <section className="login-left">

        <div className="login-left-content">

          {/* BRAND */}

          <Link
            to="/"
            className="login-brand"
          >
            <div className="login-brand-mark">
              D
            </div>

            <div>
              <h2>DemandIQ</h2>
              <span>Intelligent Decisions</span>
            </div>
          </Link>


          {/* MESSAGE */}

          <div className="login-message">

            <div className="login-badge">
              <span></span>
              Intelligent Business Platform
            </div>

            <h1>
              Turn demand into
              <br />
              <strong>better decisions.</strong>
            </h1>

            <p>
              Access your DemandIQ workspace and
              transform business data into intelligent,
              actionable insights.
            </p>


            <div className="login-benefits">

              <div className="login-benefit">
                <span>✓</span>
                Demand forecasting
              </div>

              <div className="login-benefit">
                <span>✓</span>
                Inventory intelligence
              </div>

              <div className="login-benefit">
                <span>✓</span>
                Business analytics
              </div>

            </div>

          </div>


          {/* FOOTER */}

          <div className="login-left-footer">
            <span>© 2026 DemandIQ</span>
            <span>Intelligent Decisions</span>
          </div>

        </div>

      </section>


      {/* =====================================================
          RIGHT SIDE
      ====================================================== */}

      <section className="login-right">

        <div className="login-card">

          {/* MOBILE BRAND */}

          <div className="login-mobile-brand">

            <div className="login-brand-mark">
              D
            </div>

            <div>
              <strong>DemandIQ</strong>
              <span>Intelligent Decisions</span>
            </div>

          </div>


          {/* HEADER */}

          <div className="login-card-header">

            <span className="login-overline">
              WELCOME BACK
            </span>

            <h1>
              Sign in to your account
            </h1>

            <p>
              Enter your User ID and password to
              access your workspace.
            </p>

          </div>


          {/* =================================================
              FORM
          ================================================== */}

          <form
            className="login-form"
            onSubmit={handleSubmit}
          >

            {/* USER ID */}

            <div className="login-field">

              <label htmlFor="userId">
                User ID
              </label>

              <div className="login-input-wrapper">

                <span className="login-input-icon">
                  ID
                </span>

                <input
                  id="userId"
                  type="text"
                  placeholder="Enter your User ID"
                  value={userId}
                  onChange={(event) =>
                    setUserId(event.target.value)
                  }
                  autoComplete="username"
                  required
                />

              </div>

            </div>


            {/* PASSWORD */}

            <div className="login-field">

              <div className="login-label-row">

                <label htmlFor="password">
                  Password
                </label>

                <button
                  type="button"
                  className="forgot-password"
                  onClick={() =>
                    alert(
                      "Password recovery is available in the full version."
                    )
                  }
                >
                  Forgot password?
                </button>

              </div>

              <div className="login-input-wrapper">

                <span className="login-input-icon">
                  •
                </span>

                <input
                  id="password"
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={password}
                  onChange={(event) =>
                    setPassword(event.target.value)
                  }
                  autoComplete="current-password"
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() =>
                    setShowPassword(
                      !showPassword
                    )
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                >
                  {showPassword ? "◉" : "○"}
                </button>

              </div>

            </div>


            {/* REMEMBER ME */}

            <div className="login-options">

              <label className="remember-option">

                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(event) =>
                    setRememberMe(
                      event.target.checked
                    )
                  }
                />

                <span>
                  Remember me
                </span>

              </label>

            </div>


            {/* SIGN IN */}

            <button
              type="submit"
              className="login-submit"
            >
              Sign In
              <span>→</span>
            </button>

          </form>


          {/* PROTOTYPE NOTE */}

          <div className="login-demo-note">

            <span>i</span>

            <div>

              <strong>
                Prototype Mode
              </strong>

              <p>
                This demonstration uses a static
                authentication flow. Enter any User ID
                and password to continue.
              </p>

            </div>

          </div>


          {/* DIVIDER */}

          <div className="login-divider">
            <span>OR</span>
          </div>


          {/* BACK */}

          <Link
            to="/"
            className="back-home"
          >
            ← Back to homepage
          </Link>

        </div>

      </section>

    </div>
  );
}

export default Login;