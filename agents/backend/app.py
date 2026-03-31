from flask import Flask
from settings import Config

# import blueprints
from pages.index import question_bp


app = Flask(__name__)
app.config.from_object(Config)

# register blueprints)
app.register_blueprint(question_bp)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=Config.port, host=Config.host, use_reloader=True)
