import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "This is data magic!"

def main():
    app.run()
    
if __name__ == '__main__':
    main()
