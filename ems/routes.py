from flask import session, jsonify
from ems import app
from ems.models import *

@app.errorhandler(403)
def error_403(error):
    return jsonify({'error': error}), 403

@app.errorhandler(404)
def error_404(error):
    return jsonify({'error': error}), 404


@app.errorhandler(500)
def error_500(error):
    return jsonify({'error': error}), 500