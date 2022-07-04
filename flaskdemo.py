import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return 'This is <a href="http://vg.no">data magic</a>!'

def main():
    app.run()

if __name__ == "__main__":
    main()

# remember to 'pip install flask'