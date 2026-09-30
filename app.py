from flask import Flask, jsonify

from config import Config


def create_app():
    """Create and configure the DemandIQ Flask application."""

    app = Flask(__name__)
    app.config.from_object(Config)

    # Register route blueprints
    from routes.auth import auth_bp
    from routes.business import business_bp
    from routes.investor import investor_bp
    from routes.analytics import analytics_bp
    from routes.admin import admin_bp
    from routes.product_api import product_api_bp
    from routes.sales_api import sales_api_bp
    from routes.forecast_api import forecast_api_bp
    from routes.intelligence_api import intelligence_api_bp
    from routes.market_api import market_api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(investor_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(product_api_bp)
    app.register_blueprint(sales_api_bp)
    app.register_blueprint(forecast_api_bp)
    app.register_blueprint(intelligence_api_bp)
    app.register_blueprint(market_api_bp)

    # Health check
    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "success",
            "service": "DemandIQ Backend",
            "message": "Backend is running"
        })

    # Global 404 response for API routes
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    # Global 500 response
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )