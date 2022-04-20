import flask
import mylastool

app = flask.Flask(__name__)

url = mylastool.get_container_url()
container = mylastool.get_container_from_url(url)
lasfiles = mylastool.get_list_of_lasfiles(container)

@app.route('/')
def index():
    lines = []
    lines.append('<!doctype html>')
    lines.append('<html lang=en>')
    lines.append('<head><meta charset=utf-8><title>My webapp</title></head>')
    lines.append('<body>')
    lines.append('<pre>')
    for (idx, filename) in enumerate(lasfiles):
        lines.append(f'<a href="/header/{idx}">{filename}</a>')
    lines.append('</pre>')
    lines.append('</body>')
    lines.append('</html>')
    return '\n'.join(lines)

@app.route('/header/<idx>')
def header(idx):
    """Return header of LAS file from container."""
    filename = lasfiles[int(idx)]
    lasfile = mylastool.read_lasfile(container, filename)
    headersection = mylastool.get_header_section(lasfile)
    lines = []
    lines.append('<!doctype html>')
    lines.append('<html lang=en>')
    lines.append('<head><meta charset=utf-8><title>My webapp</title></head>')
    lines.append('<body>')
    lines.append('<pre>')
    lines.extend(headersection)
    lines.append('</pre>')
    lines.append('</body>')
    lines.append('</html>')
    return '\n'.join(lines)

def main():
    app.run()

if __name__ == "__main__":
    main()

