import flask
from flask import Blueprint

from Api.Routes import BaseRoute, ChamberApi


class ChamberRoute(BaseRoute.BaseRoute):
    _blueprint = Blueprint('chamber', __name__)

    @_blueprint.route('/list', methods=['GET'])
    def listChamberItems(self):
        return ChamberApi.ChamberApi.getItems()

    @_blueprint.route('/delete/<str:itemId>', methods=['DELETE'])
    def deleteChamberItem(self, itemId: str):
        ChamberApi.ChamberApi.deleteItem(itemId)
        return {'id': itemId}

    @_blueprint.route('/', methods=['POST'])
    def createChamberItem(self):
        body = flask.request.json
        return ChamberApi.ChamberApi.createItem(body['name'], body['ferment'])
