import flask
from flask import Blueprint

from Api.Routes import BoardApi, BaseRoute


class BoardRoute(BaseRoute.BaseRoute):
    _blueprint = Blueprint('control', __name__)

    @_blueprint.route('/', methods=['GET'])
    def getStatus(self):
        return BoardApi.BoardApi.getState()

    @_blueprint.route('/temp-bounds', methods=['POST'])
    def setTempBounds(self):
        json = flask.request.json
        return BoardApi.BoardApi.setTempBounds(json.get('lower'), json.get('upper'))
