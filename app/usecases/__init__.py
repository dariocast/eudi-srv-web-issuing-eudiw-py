from flask import Blueprint

# Import each use case blueprint
from .health_usecase import health_usecase
from .top_usecase import top_usecase

usecases_bp = Blueprint("usecases", __name__, url_prefix="/usecases")

# Register each use case blueprint
usecases_bp.register_blueprint(health_usecase)
usecases_bp.register_blueprint(top_usecase)