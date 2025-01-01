from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
        app.logger.error(f"HTTP error occurred: {e}")
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.error(f"Unexpected error: {e}")
        response = {
            "code": 500,
            "name": "Internal Server Error",
            "description": "An unexpected error occurred"
        }
        return jsonify(response), 500
