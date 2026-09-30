import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import "./App.css";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import BusinessDashboard from "./pages/BusinessDashboard";
import InvestorDashboard from "./pages/InvestorDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import Forecast from "./pages/Forecast";
import ModulePage from "./pages/ModulePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ================================================
            MAIN
            ================================================ */}

        <Route
          path="/"
          element={<Landing />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        {/* ================================================
            BUSINESS
            ================================================ */}

        <Route
          path="/dashboard"
          element={<BusinessDashboard />}
        />

        <Route
          path="/business"
          element={<BusinessDashboard />}
        />

        <Route
          path="/forecast"
          element={<Forecast />}
        />

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

        {/* ================================================
            INVESTOR
            ================================================ */}

        <Route
          path="/investor"
          element={<InvestorDashboard />}
        />

        <Route
          path="/portfolio"
          element={<ModulePage />}
        />

        <Route
          path="/transactions"
          element={<ModulePage />}
        />

        <Route
          path="/stocks"
          element={<InvestorDashboard />}
        />

        {/* ================================================
            ADMIN
            ================================================ */}

        <Route
          path="/admin"
          element={<AdminDashboard />}
        />

        {/* ================================================
            FALLBACK
            ================================================ */}

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