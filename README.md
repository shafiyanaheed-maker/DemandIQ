# DemandIQ

## Intelligent Demand Forecasting for Inventory Management

> **Predict Demand. Optimize Inventory. Drive Business Growth.** 🚀

DemandIQ is an AI-powered inventory management system designed to forecast future product demand using Machine Learning. The system analyzes historical sales and inventory data to identify demand patterns and provide predictive insights for better inventory planning.

It aims to help businesses reduce overstocking, prevent stock shortages, improve inventory planning, and support data-driven business decisions through dashboards and analytical reports.

---

## 📌 Problem Statement

Maintaining the right inventory level is a major challenge for businesses.

* **Overstocking** increases storage costs, ties up capital, and may lead to product waste.
* **Stockouts** result in missed sales and customer dissatisfaction.
* **Manual inventory management** makes it difficult to identify complex and changing demand patterns.

DemandIQ addresses these challenges by applying Machine Learning-based demand forecasting and inventory analysis.

---

## 🎯 Objectives

* Forecast future product demand using Machine Learning.
* Minimize overstocking and understocking situations.
* Improve inventory planning and management efficiency.
* Analyze historical sales patterns.
* Provide dashboards and visual analytics.
* Support business decision-making through predictive insights.

---

## ⚙️ How DemandIQ Works

```text
Historical Sales & Inventory Data
              │
              ▼
       Data Preprocessing
              │
              ▼
      Demand Forecasting
       Machine Learning
              │
              ▼
     Inventory Optimization
              │
              ▼
   Forecasts & Stock Insights
              │
              ▼
       Dashboard & Reports
```

### 1. Data Collection

Historical sales, inventory, product, and related business data are collected and stored for analysis.

### 2. Data Preprocessing

The collected data is cleaned, organized, and transformed into a suitable format for Machine Learning.

### 3. Demand Forecasting

The forecasting engine analyzes available sales patterns and generates predicted demand.

### 4. Inventory Optimization

Predicted demand can be compared with inventory levels to identify potential stock shortages or excess inventory.

### 5. Dashboard & Visualization

Forecasts and inventory information are presented through web-based dashboards and visualizations.

---

## 🧩 Core Modules

### Data Management

Handles product, sales, inventory, and related business information.

### Demand Forecasting

Uses the demand prediction engine to generate future demand estimates.

### Authentication

Provides application login and authentication functionality.

### Business Management

Provides functionality related to products, sales, inventory, and business operations.

### Admin Management

Provides administrative functionality and dashboard access.

### Analytics

Provides analytical views and demand/inventory insights.

### Investor Module

Provides investor-oriented dashboards, portfolio information, and transaction views.

### Dashboard & Visualization

Provides web interfaces for displaying operational information and forecasting results.

---

## ✨ Key Features

* 🤖 Machine Learning-based demand forecasting
* 📊 Demand and sales analytics
* 📦 Inventory management
* 🛒 Product management
* 💰 Sales management
* 🔔 Inventory and stock insights
* 📈 Forecast visualization
* 👤 Authentication system
* 🛠️ Admin dashboard
* 💼 Business dashboard
* 📊 Analytics dashboard
* 💹 Investor dashboard
* 📑 Portfolio and transaction management
* 🎨 Responsive web interface

---

## 🛠️ Technology Stack

| Technology       | Purpose                      |
| ---------------- | ---------------------------- |
| **Python**       | Backend and Machine Learning |
| **Flask**        | Web application framework    |
| **Pandas**       | Data processing              |
| **NumPy**        | Numerical computation        |
| **Scikit-Learn** | Machine Learning             |
| **MySQL**        | Database                     |
| **HTML**         | Frontend structure           |
| **CSS**          | Frontend styling             |
| **Jinja2**       | Dynamic web templates        |

---

## 📁 Project Structure

```text
DemandIQ/
│
├── app.py
├── config.py
├── database.py
├── demand_prediction.py
├── test_db.py
├── .gitignore
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── business.py
│   ├── admin.py
│   ├── analytics.py
│   └── investor.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── graphs/
│       └── forecast.png
│
└── templates/
    ├── index.html
    ├── login.html
    ├── products.html
    ├── products_list.html
    ├── sales.html
    ├── sales_list.html
    ├── inventory.html
    ├── stocks.html
    ├── buy_stock.html
    ├── forecast.html
    ├── business_dashboard.html
    ├── admin_dashboard.html
    ├── investor_dashboard.html
    ├── portfolio.html
    └── transactions.html
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shafiyanaheed-maker/DemandIQ.git
cd DemandIQ
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\activate
```

### 3. Install dependencies

If a `requirements.txt` file is available:

```powershell
pip install -r requirements.txt
```

Otherwise, install the required Python packages according to the project's current environment.

### 4. Configure the database

Configure the required MySQL database settings in the application configuration.

### 5. Run the application

```powershell
python app.py
```

Then open the local Flask URL shown in the terminal.

---

## 📊 Current Development Status

DemandIQ is currently under active development.

### Implemented Project Foundation

* [x] Flask application structure
* [x] Application configuration
* [x] Database layer
* [x] Demand prediction module
* [x] Authentication routes
* [x] Business routes
* [x] Admin routes
* [x] Analytics routes
* [x] Investor routes
* [x] Landing and login pages
* [x] Product management pages
* [x] Sales management pages
* [x] Inventory and stock pages
* [x] Forecast dashboard pages
* [x] Investor and transaction pages
* [x] Forecast visualization
* [x] Database testing foundation

### 🚧 Planned Development

* [ ] Improve and validate the Machine Learning forecasting pipeline
* [ ] Connect forecasting with live database data
* [ ] Implement inventory recommendation logic
* [ ] Add automated stockout and overstock alerts
* [ ] Improve dashboard analytics
* [ ] Add model evaluation metrics
* [ ] Add historical-vs-predicted demand comparisons
* [ ] Improve reporting functionality
* [ ] Add production-ready deployment configuration

---

## 🔮 Future Scope

* Advanced Deep Learning-based forecasting
* Multi-store inventory management
* Multi-warehouse support
* ERP and Supply Chain Management integration
* AI-powered automated stock replenishment
* Mobile application
* Cloud deployment
* Real-time market trend analysis
* Supplier and procurement analytics
* E-commerce platform integration

---

## 📈 Expected Outcomes

DemandIQ aims to provide:

* More accurate demand predictions
* Reduced inventory carrying costs
* Fewer stock shortages
* Reduced overstocking
* Improved operational efficiency
* Better inventory planning
* Data-driven business decisions

---

## 🎓 Project Type

**Mini Project**

**Domain:** Artificial Intelligence · Machine Learning · Inventory Management

---

## 👩‍💻 Contributors

* **Shaafiya Naheed**
* **A. Amulya**
* **B. Sai Preethi**

---

## 📄 License

This project is licensed under the **MIT License**.
