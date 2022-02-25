"""My webapp showing all LAS files in an azure storage container."""

import flask
import mylastool

app = flask.Flask(__name__)

container = mylastool.getcontainer()
lasfiles = mylastool.listfiles(container, ".LAS")


@app.route('/')
def index():
    """Build and return a list of all files in storage account."""
    lines = []
    lines.append('<!doctype html>')
    lines.append('<html lang=en>')
    lines.append('<head><meta charset=utf-8><title>My webapp</title></head>')
    lines.append('<body>')
    lines.append('<pre>')
    for (idx, (size, filename)) in enumerate(lasfiles):
        lines.append(f'{size:>20} <a href="/header/{idx}">{filename}</a>')
    lines.append('</pre>')
    lines.append('</body>')
    lines.append('</html>')
    return '\n'.join(lines)


@app.route('/header/<idx>')
def header(idx):
    """Return header of LAS file from container."""
    (_, filename) = lasfiles[int(idx)]
    lasfile = mylastool.readtextfile(container, filename)
    headersection = mylastool.headersection(lasfile)
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
    """Run main function of the program."""
    app.debug = True
    app.run()


if __name__ == '__main__':
    main()
