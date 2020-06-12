""" API Blueprint Application """

from flask import Blueprint, current_app
from flask_restplus import Api

api_bp = Blueprint('api_bp', __name__, url_prefix='/api')
api_rest = Api(api_bp)



# Import resources to ensure view is registered
from .resources import * # NOQA
