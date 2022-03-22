import os
import azure.storage.blob
import segyio
import matplotlib.pyplot as plt
import flask

#
# Download a SEGY file from an Azure Storage Blob
#

URL = os.environ['CONTAINER_URL']
container = azure.storage.blob.ContainerClient.from_container_url(URL)
path = '31_5-7 Eos/07.Borehole_Seismic/VSPZO_RAW_2020-01-17_4.SEGY'
data = container.get_blob_client(path).download_blob().readall()
filename = os.path.basename(path)
with open(filename, "wb") as file:
    file.write(data)

#
# Plot the SEGY file
#

traces = []
with segyio.open(filename, strict=False) as f:
    for trace in f.trace:
        traces.append(list(trace))
plt.imshow(traces, vmin=-0.01, vmax=0.01)
plt.savefig('demoapp.png')

#
# Start webapp to serve the plot
#

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.send_file('./demoapp.png', mimetype='image/png')

app.run()
