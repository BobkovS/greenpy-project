from app.api.errors import error_response as api_error_response
from app.errors import bp


@bp.app_errorhandler(500)
def internal_error(error):
    return api_error_response(500, error)
