import flask

app = flask.Flask("flaskdemo")

@app.route('/')
def index():
    return "This is data magic!"

def main():
    app.run()

if __name__ == "__main__":
    main()
