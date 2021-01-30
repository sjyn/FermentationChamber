from flask import Flask
from Api.Routes.BoardRoute import BoardRoute
from Api.Routes.ChamberRoute import ChamberRoute

app = Flask(__name__)
app.register_blueprint(BoardRoute().getBlueprint())
app.register_blueprint(ChamberRoute().getBlueprint())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
