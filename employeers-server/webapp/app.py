from flask import Flask
from .apis import api
from .errors_handler import configure_error_handling

app = Flask(__name__)
api.init_app(app)
configure_error_handling(api)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
