from flask import Flask


def create_app():
    app = Flask (__name__)
    
    @app.route("/")

    def hello():
        return "liberty app or bust!"
    
    return app
