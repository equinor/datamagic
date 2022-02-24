"""Flask webapp demo."""

import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    """Return a default response."""
    return "Data Magic!"


def main():
    """Run main function of the program."""
    app.debug = True
    app.run()


if __name__ == '__main__':
    main()

# hint:
#   export FLASK_APP=flaskwebapp.py
#   flask run
# or
#   python flaskwebapp.py
