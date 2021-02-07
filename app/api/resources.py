"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""

from datetime import datetime
from flask import request
from flask_restx import Resource

from .security import require_auth
from . import api_rest

from .barcode import *
import os


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}


@api_rest.route('/uploadBarcode')
class UploadBarcode(Resource):
    def post(self):
        if 'file' not in request.files:
            return 'Please upload file', 400

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        root_dir = os.getcwd()
        img = Image.open(file)
        
        barcode_id = read_image_barcode(img)

        product_info = get_product_info(barcode_id)

        return product_info

