"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
import logging
from flask import request, current_app
from flask_restplus import Resource

from . import api_rest
from app.api.utils.Text import Text
from app.api.utils.correlation import calculate_correlation

logger = logging.getLogger()


@api_rest.route('/results/calculate')
class ResourceOne(Resource):

    def post(self):
        json_payload = request.json
        current_app.logger.info(f'Received json payload: {json_payload}')

        attributes = {k: v for k, v in json_payload['attributes'].items() if v['checked'] is True}
        first_text_results = Text(json_payload['first_text'], attributes).calculate_results()
        second_text_results = Text(json_payload['second_text'], attributes).calculate_results()
        correlation = calculate_correlation(
            list(map(lambda k: k[1]['result'], first_text_results.items())),
            list(map(lambda k: k[1]['result'], second_text_results.items()))
        )

        payload = {
            'correlation': correlation,
            'attributes': [{'id': ind, 'name': v['name'],
                            'first_text': round(v['result'], 2),
                            'second_text': round(second_text_results[k]['result'], 2)
                            } for ind, (k, v) in enumerate(first_text_results.items(), start=1)],
        }
        current_app.logger.info(f'Results: {payload}')
        return {'results': payload}, 200
