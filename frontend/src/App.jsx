import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import "./App.css";

// Main pages
import Landing from "./pages/Landing";
import Login from "./pages/Login";

// Dashboards
import BusinessDashboard from "./pages/BusinessDashboard";
import InvestorDashboard from "./pages/InvestorDashboard";
import AdminDashboard from "./pages/AdminDashboard";

// Business modules
import Forecast from "./pages/Forecast";
import ModulePage from "./pages/ModulePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* =====================================================
            LANDING & AUTHENTICATION
        ====================================================== */}

        <Route
          path="/"
          element={<Landing />}
        />

        <Route
          path="/login"
          element={<Login />}
        />


        {/* =====================================================
            BUSINESS DASHBOARD
        ====================================================== */}

        <Route
          path="/dashboard"
          element={<BusinessDashboard />}
        />

        <Route
          path="/business"
          element={<BusinessDashboard />}
        />


        {/* =====================================================
            DEMAND FORECASTING
        ====================================================== */}

        <Route
          path="/forecast"
          element={<Forecast />}
        />


        {/* =====================================================
            BUSINESS INTELLIGENCE MODULES
        ====================================================== */}

        <Route
          path="/inventory"
          element={<ModulePage />}
        />

        <Route
          path="/analytics"
          element={<ModulePage />}
        />

        <Route
          path="/alerts"
          element={<ModulePage />}
        />


        {/* =====================================================
            FINANCIAL STOCKS
        ====================================================== */}

        <Route
          path="/investor"
          element={<InvestorDashboard />}
        />

        <Route
          path="/stocks"
          element={<InvestorDashboard />}
        />


        {/* =====================================================
            INVESTOR MODULES
        ====================================================== */}

        <Route
          path="/portfolio"
          element={<ModulePage />}
        />

        <Route
          path="/transactions"
          element={<ModulePage />}
        />


        {/* =====================================================
            ADMINISTRATION
        ====================================================== */}

        <Route
          path="/admin"
          element={<AdminDashboard />}
        />


        {/* =====================================================
            FALLBACK
            Any unknown URL goes back to landing page.
        ====================================================== */}

        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;