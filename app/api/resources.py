"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

import logging

from flask import request
from flask_restplus import Resource

from app.api.utils.Text import Text
from app.api.utils.correlation import calculate_correlation
from . import api_rest

logger = logging.getLogger()


@api_rest.route('/results/calculate')
class ResourceOne(Resource):

    def post(self):
        json_payload = request.json
        # logger.info(f'Received json payload: {json_payload}')

        attributes = {k: v for k, v in json_payload['attributes'].items() if v['checked'] is True}
        first_text_results = Text(json_payload['first_text'], json_payload['first_text_genre'],
                                  attributes).calculate_results()
        second_text_results = Text(json_payload['second_text'], json_payload['second_text_genre'],
                                   attributes).calculate_results()
        correlation = calculate_correlation(
            list(map(lambda k: k[1]['result'], first_text_results[0].items())),
            list(map(lambda k: k[1]['result'], second_text_results[0].items()))
        )

        payload = {
            'correlation': round(correlation, 4),
            'attributes': [{'id': ind, 'name': v['name'],
                            'first_text': round(v['result'], 4) if type(v['result']) is not str else v['result'],
                            'second_text': round(second_text_results[0][k]['result'], 4) if type(
                                second_text_results[0][k]['result']) is not str else second_text_results[0][k]['result']
                            } for ind, (k, v) in enumerate(first_text_results[0].items(), start=1)],
            'extended_attributes': [{'id': ind, 'description': v['description'], 'name': k,
                                     'first_text': {
                                         'value': round(v['value'], 4) if type(v['value']) is not str else v['value'],
                                         'debug': v['debug']},
                                     'second_text': {'value': round(second_text_results[1][k]['value'], 4) if type(
                                         second_text_results[1][k]['value']) is not str else second_text_results[1][k][
                                         'value'],
                                                     'debug': second_text_results[1][k]['debug']}
                                     } for ind, (k, v) in enumerate(first_text_results[1].items(), start=1)],
        }
        logger.info(f'Results: {payload}')
        return {'results': payload}, 200
