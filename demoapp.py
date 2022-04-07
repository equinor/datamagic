import os
import azure.storage.blob
import numpy
import matplotlib.pyplot as plt
import flask

#
# Create a connection into an Azure Storage Blob
#

url = os.environ['CONTAINER_URL']
container = azure.storage.blob.ContainerClient.from_container_url(url)
print(f"Connected to storage blob")

#
# Get list of all LAS files
#

files = []
for blob in container.list_blobs():
    if blob.name.endswith(".LAS"):
        files.append(blob.name)
print(f"Found {len(files)} LAS files")

#
# Get path for a particular LAS file
#

filename = None
for name in files:
    if name.endswith("TZV_TIME_SYNSEIS_2020-01-17_2.LAS"):
        filename = name
        break
print(f"Filename: {filename}")

#
# Read LAS file into memory
#

blob_client = container.get_blob_client(filename)
data = blob_client.download_blob().content_as_bytes()
lines = []
for line in data.splitlines():
    lines.append(line.decode("ascii", errors="ignore"))
print(f"Read {len(lines)} lines of text")

#
# Find index of data section
#

idx = 0
for line in lines:
    if line.startswith('~A'):
        break
    idx += 1
print(f"Data section starts at line {idx}")

#
# Extract a curve
#

curve = []
for row in lines[idx+1:]:
    cols = row.split()
    cell = cols[1]
    curve.append(float(cell))
print(f"Extracted {len(curve)} values. minvalue={min(curve)}, maxvalue={max(curve)}")

#
# Clean up values in curve
#

import numpy as np
curve = np.array(curve)
curve = np.where(curve==-999.25, np.nan, curve)
print(f"Cleaned up curve")

#
# Plot curve
#

import matplotlib.pyplot as plt
plt.plot(curve)
plt.savefig('demoapp.png')
print(f"Curve plotted")

#
# Start webapp to serve the plot
#

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.send_file('./demoapp.png', mimetype='image/png')

app.run()
