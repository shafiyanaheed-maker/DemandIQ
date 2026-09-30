import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

const users = [
  {
    name: "Shaafiya",
    email: "shaafiya@demandiq.com",
    role: "Admin",
    status: "Active",
    joined: "Sep 12, 2026",
  },
  {
    name: "Asfiya",
    email: "asfiya@demandiq.com",
    role: "Business",
    status: "Active",
    joined: "Sep 14, 2026",
  },
  {
    name: "Rahul Kumar",
    email: "rahul@demandiq.com",
    role: "Investor",
    status: "Active",
    joined: "Sep 18, 2026",
  },
  {
    name: "Priya Sharma",
    email: "priya@demandiq.com",
    role: "Business",
    status: "Active",
    joined: "Sep 21, 2026",
  },
];

const activities = [
  {
    title: "New business account created",
    user: "Priya Sharma",
    time: "12 minutes ago",
    type: "user",
  },
  {
    title: "Forecast generated",
    user: "Asfiya",
    time: "28 minutes ago",
    type: "forecast",
  },
  {
    title: "Inventory alert reviewed",
    user: "Rahul Kumar",
    time: "45 minutes ago",
    type: "alert",
  },
  {
    title: "Portfolio data updated",
    user: "Shaafiya",
    time: "1 hour ago",
    type: "portfolio",
  },
];

function AdminDashboard() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("Overview");

  const showDemoMessage = (message) => {
    alert(`${message} — Demo action`);
  };

  return (
    <div className="admin-page">
      {/* =========================
          SIDEBAR
      ========================== */}
      <aside className="admin-sidebar">
        <div className="admin-brand">
          <div className="admin-brand-mark">D</div>

          <div>
            <h2>DemandIQ</h2>
            <span>Intelligent Decisions</span>
          </div>
        </div>

        <div className="admin-profile">
          <div className="admin-avatar">A</div>

          <div>
            <strong>Administrator</strong>
            <span>System Management</span>
          </div>
        </div>

        <nav className="admin-nav">
          <div className="admin-nav-label">MAIN</div>

          <Link to="/dashboard" className="admin-nav-item">
            <span>⌂</span>
            Dashboard
          </Link>

          <Link to="/forecast" className="admin-nav-item">
            <span>⌁</span>
            Forecast
          </Link>

          <Link to="/inventory" className="admin-nav-item">
            <span>▣</span>
            Inventory
          </Link>

          <Link to="/analytics" className="admin-nav-item">
            <span>◫</span>
            Analytics
          </Link>

          <Link to="/alerts" className="admin-nav-item">
            <span>⚠</span>
            Alerts
          </Link>

          <div className="admin-nav-label">FINANCIAL</div>

          <Link to="/investor" className="admin-nav-item">
            <span>↗</span>
            Financial Stocks
          </Link>

          <Link to="/portfolio" className="admin-nav-item">
            <span>▤</span>
            Portfolio
          </Link>

          <Link to="/transactions" className="admin-nav-item">
            <span>↔</span>
            Transactions
          </Link>

          <div className="admin-nav-label">ADMINISTRATION</div>

          <Link to="/admin" className="admin-nav-item active">
            <span>⚙</span>
            Admin Panel
          </Link>
        </nav>

        <button
          className="admin-logout"
          onClick={() => navigate("/")}
        >
          <span>⇥</span>
          Logout
        </button>
      </aside>

      {/* =========================
          MAIN CONTENT
      ========================== */}
      <main className="admin-main">
        {/* HEADER */}
        <header className="admin-header">
          <div>
            <div className="admin-breadcrumb">
              DemandIQ <span>/</span> Administration
            </div>

            <h1>Admin Dashboard</h1>

            <p>
              Manage users, monitor platform activity and review
              system health.
            </p>
          </div>

          <div className="admin-header-actions">
            <div className="system-status">
              <span></span>
              All Systems Operational
            </div>

            <button
              className="admin-refresh"
              onClick={() =>
                showDemoMessage("System status refreshed")
              }
            >
              ↻ Refresh
            </button>
          </div>
        </header>

        {/* =========================
            STAT CARDS
        ========================== */}
        <section className="admin-stats">
          <div className="admin-stat-card">
            <div className="admin-stat-icon users">
              ♙
            </div>

            <div>
              <span>Total Users</span>
              <strong>248</strong>
              <small className="admin-positive">
                +18 this month
              </small>
            </div>
          </div>

          <div className="admin-stat-card">
            <div className="admin-stat-icon businesses">
              ◫
            </div>

            <div>
              <span>Business Accounts</span>
              <strong>95</strong>
              <small className="admin-positive">
                +8 this month
              </small>
            </div>
          </div>

          <div className="admin-stat-card">
            <div className="admin-stat-icon investors">
              ↗
            </div>

            <div>
              <span>Investors</span>
              <strong>126</strong>
              <small className="admin-positive">
                +11 this month
              </small>
            </div>
          </div>

          <div className="admin-stat-card">
            <div className="admin-stat-icon alerts">
              ⚠
            </div>

            <div>
              <span>Active Alerts</span>
              <strong>7</strong>
              <small className="admin-warning">
                3 require attention
              </small>
            </div>
          </div>
        </section>

        {/* =========================
            TOP SECTION
        ========================== */}
        <section className="admin-top-grid">
          {/* SYSTEM HEALTH */}
          <div className="admin-panel">
            <div className="admin-panel-header">
              <div>
                <h2>System Health</h2>
                <p>Current platform service status</p>
              </div>

              <span className="health-badge">
                Healthy
              </span>
            </div>

            <div className="health-list">
              <div className="health-row">
                <div>
                  <strong>API Server</strong>
                  <span>Core application services</span>
                </div>

                <div className="health-value">
                  <span className="health-dot"></span>
                  Operational
                </div>
              </div>

              <div className="health-row">
                <div>
                  <strong>Database</strong>
                  <span>Data persistence layer</span>
                </div>

                <div className="health-value">
                  <span className="health-dot"></span>
                  Operational
                </div>
              </div>

              <div className="health-row">
                <div>
                  <strong>Forecast Engine</strong>
                  <span>Demand prediction service</span>
                </div>

                <div className="health-value">
                  <span className="health-dot"></span>
                  Operational
                </div>
              </div>

              <div className="health-row">
                <div>
                  <strong>Financial Module</strong>
                  <span>Market intelligence service</span>
                </div>

                <div className="health-value">
                  <span className="health-dot"></span>
                  Operational
                </div>
              </div>
            </div>
          </div>

          {/* PLATFORM USAGE */}
          <div className="admin-panel">
            <div className="admin-panel-header">
              <div>
                <h2>Platform Usage</h2>
                <p>Current activity overview</p>
              </div>
            </div>

            <div className="usage-main">
              <div className="usage-circle">
                <div>
                  <strong>78%</strong>
                  <span>Capacity</span>
                </div>
              </div>

              <div className="usage-details">
                <div>
                  <span>Active Sessions</span>
                  <strong>84</strong>
                </div>

                <div>
                  <span>Forecast Jobs</span>
                  <strong>26</strong>
                </div>

                <div>
                  <span>API Requests</span>
                  <strong>12.4K</strong>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* =========================
            ADMINISTRATION
        ========================== */}
        <section className="admin-panel admin-management-panel">
          <div className="admin-panel-header">
            <div>
              <h2>Administration</h2>
              <p>Manage the DemandIQ platform</p>
            </div>

            <div className="admin-tabs">
              <button
                className={
                  activeTab === "Overview" ? "active" : ""
                }
                onClick={() => setActiveTab("Overview")}
              >
                Overview
              </button>

              <button
                className={
                  activeTab === "Users" ? "active" : ""
                }
                onClick={() => setActiveTab("Users")}
              >
                Users
              </button>

              <button
                className={
                  activeTab === "Activity" ? "active" : ""
                }
                onClick={() => setActiveTab("Activity")}
              >
                Activity
              </button>
            </div>
          </div>

          {/* OVERVIEW TAB */}
          {activeTab === "Overview" && (
            <div className="admin-overview">
              <div className="admin-action-card">
                <div className="admin-action-icon">
                  ♙
                </div>

                <div>
                  <h3>User Management</h3>

                  <p>
                    Review and manage registered DemandIQ
                    users.
                  </p>
                </div>

                <button
                  onClick={() => setActiveTab("Users")}
                >
                  Manage →
                </button>
              </div>

              <div className="admin-action-card">
                <div className="admin-action-icon">
                  ◫
                </div>

                <div>
                  <h3>Platform Activity</h3>

                  <p>
                    Review recent actions across the
                    platform.
                  </p>
                </div>

                <button
                  onClick={() => setActiveTab("Activity")}
                >
                  View →
                </button>
              </div>

              <div className="admin-action-card">
                <div className="admin-action-icon">
                  ⚙
                </div>

                <div>
                  <h3>System Settings</h3>

                  <p>
                    Review platform configuration and
                    services.
                  </p>
                </div>

                <button
                  onClick={() =>
                    showDemoMessage("System settings")
                  }
                >
                  Open →
                </button>
              </div>
            </div>
          )}

          {/* USERS TAB */}
          {activeTab === "Users" && (
            <div className="admin-users-table-wrapper">
              <table className="admin-users-table">
                <thead>
                  <tr>
                    <th>USER</th>
                    <th>ROLE</th>
                    <th>STATUS</th>
                    <th>JOINED</th>
                    <th>ACTION</th>
                  </tr>
                </thead>

                <tbody>
                  {users.map((user) => (
                    <tr key={user.email}>
                      <td>
                        <div className="admin-user-cell">
                          <div className="admin-user-avatar">
                            {user.name.charAt(0)}
                          </div>

                          <div>
                            <strong>{user.name}</strong>
                            <span>{user.email}</span>
                          </div>
                        </div>
                      </td>

                      <td>
                        <span className="role-badge">
                          {user.role}
                        </span>
                      </td>

                      <td>
                        <span className="user-status">
                          <i></i>
                          {user.status}
                        </span>
                      </td>

                      <td>{user.joined}</td>

                      <td>
                        <button
                          className="user-action"
                          onClick={() =>
                            showDemoMessage(
                              `Manage ${user.name}`
                            )
                          }
                        >
                          Manage
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* ACTIVITY TAB */}
          {activeTab === "Activity" && (
            <div className="activity-list">
              {activities.map((activity, index) => (
                <div
                  className="activity-row"
                  key={index}
                >
                  <div
                    className={`activity-icon ${activity.type}`}
                  >
                    {activity.type === "user" && "♙"}
                    {activity.type === "forecast" && "⌁"}
                    {activity.type === "alert" && "!"}
                    {activity.type === "portfolio" && "↗"}
                  </div>

                  <div className="activity-content">
                    <strong>{activity.title}</strong>

                    <span>
                      By {activity.user}
                    </span>
                  </div>

                  <time>{activity.time}</time>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* =========================
            QUICK ACTIONS
        ========================== */}
        <section className="admin-quick-actions">
          <button
            onClick={() =>
              showDemoMessage("Add new user")
            }
          >
            <span>+</span>

            <div>
              <strong>Add User</strong>
              <small>
                Create a new platform account
              </small>
            </div>
          </button>

          <button
            onClick={() =>
              showDemoMessage("System configuration")
            }
          >
            <span>⚙</span>

            <div>
              <strong>System Settings</strong>
              <small>
                Configure platform services
              </small>
            </div>
          </button>

          <button
            onClick={() =>
              showDemoMessage("Audit logs")
            }
          >
            <span>▤</span>

            <div>
              <strong>Audit Logs</strong>
              <small>
                Review administrative activity
              </small>
            </div>
          </button>

          <button
            onClick={() =>
              showDemoMessage("Generate report")
            }
          >
            <span>↗</span>

            <div>
              <strong>Generate Report</strong>
              <small>
                Create system overview report
              </small>
            </div>
          </button>
        </section>
      </main>
    </div>
  );
}

export default AdminDashboard;