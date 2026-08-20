from flask import Flask

app = Flask(__name__)
app.secret_key = "DemandIQ_Secret_Key_2026"

from routes.auth import auth_bp
from routes.business import business_bp
from routes.investor import investor_bp
from routes.analytics import analytics_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(business_bp)
app.register_blueprint(investor_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)