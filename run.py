from flask import Flask
from dash_app import register_dashboard

app = Flask(__name__)
with app.app_context():
    register_dashboard(app)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')