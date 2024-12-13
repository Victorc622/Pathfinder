import os
from flask import Flask, render_template, request, session, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager
from .models import db, User
from .api.user_routes import user_routes
from .api.auth_routes import auth_routes
from .api.trip_routes import trip_routes
from .api.itinerary_item_routes import itinerary_item_routes
from .api.destination_routes import destination_routes
from .api.collaboration_routes import collaboration_routes
from .api.comment_routes import comment_routes
from .api.media_routes import media_routes
from .seeds import seed_commands
from .config import Config

app = Flask(__name__, static_folder="../react-vite/dist", static_url_path="/")

# Setup login manager
login = LoginManager(app)
login.login_view = "auth.unauthorized"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Tell flask about our seed commands
app.cli.add_command(seed_commands)

# Set app configuration
app.config.from_object(Config)

# Register all blueprints for routes
app.register_blueprint(user_routes, url_prefix="/api/users")
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(trip_routes, url_prefix="/api/trips")
app.register_blueprint(itinerary_item_routes, url_prefix="/api/itinerary-items")
app.register_blueprint(destination_routes, url_prefix="/api/destinations")
app.register_blueprint(collaboration_routes, url_prefix="/api/collaborations")
app.register_blueprint(comment_routes, url_prefix="/api/comments")
app.register_blueprint(media_routes, url_prefix="/api/media")

# Initialize the database
db.init_app(app)

# Set up migrations
Migrate(app, db)

# Application Security
CORS(app)

# Redirect HTTP to HTTPS in production
@app.before_request
def https_redirect():
    if os.environ.get("FLASK_ENV") == "production":
        if request.headers.get("X-Forwarded-Proto") == "http":
            url = request.url.replace("http://", "https://", 1)
            code = 301
            return redirect(url, code=code)


# Inject CSRF token after every request
@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        "csrf_token",
        generate_csrf(),
        secure=True if os.environ.get("FLASK_ENV") == "production" else False,
        samesite="Strict" if os.environ.get("FLASK_ENV") == "production" else None,
        httponly=True,
    )
    return response


# API documentation route
@app.route("/api/docs")
def api_help():
    """
    Returns all API routes and their doc strings
    """
    acceptable_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    route_list = {
        rule.rule: [
            [method for method in rule.methods if method in acceptable_methods],
            app.view_functions[rule.endpoint].__doc__,
        ]
        for rule in app.url_map.iter_rules()
        if rule.endpoint != "static"
    }
    return route_list


# React static files handler
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def react_root(path):
    """
    This route will direct to the public directory in our
    React builds in the production environment for favicon
    or index.html requests
    """
    if path == "favicon.ico":
        return app.send_from_directory("public", "favicon.ico")
    return app.send_static_file("index.html")


# Error handler for 404 errors
@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")