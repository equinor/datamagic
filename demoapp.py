# Before running this program, you might need to do:
#
#     python -m pip install azure-storage-blob numpy matplotlib flask
#
# and the CONTAINER_URL you can get from:
#
#     https://data.equinor.com/dataset/NorthernLights
#
# Enjoy!
#

import os
import azure.storage.blob
import numpy
import matplotlib.pyplot as plt
import flask

#
# Create a connection into an Azure Storage Blob
#

url = os.environ.get('CONTAINER_URL')
if not url:
    url = input("Please provide CONTAINER_URL: ")
container = azure.storage.blob.ContainerClient.from_container_url(url)
acc_info = container.get_account_information()
sku_name = acc_info['sku_name']
account_kind = acc_info['account_kind']
print(f"--- Connected to storage blob: {sku_name} / {account_kind}")
input()

#
# Get a list of all files
#

nfiles = 0
nbytes = 0
with open("files.dat", 'w') as f:
    for blob in container.list_blobs():
        nfiles += 1
        nbytes += blob.size
        print(f"{blob.size:<20} {blob.name}", file=f)

print(f"--- Found {nfiles} files in storage blob ({nbytes/(1024.0*1024):.2f} MB)")
input()

#
# Get list of all LAS files
#

lasfiles = []
for blob in container.list_blobs():
    if blob.name.endswith(".LAS"):
        lasfiles.append(blob.name)
print(f"--- Found {len(lasfiles)} LAS files")
input()

#
# Get path for a particular LAS file
#

filepath = None
for name in lasfiles:
    if name.endswith("TZV_TIME_SYNSEIS_2020-01-17_2.LAS"):
        filepath = name
        break
print(f"--- Filepath: {filepath}")
input()

#
# Read LAS file into memory
#

blob_client = container.get_blob_client(filepath)
data = blob_client.download_blob().content_as_bytes()
lines = []
for line in data.splitlines():
    lines.append(line.decode("ascii", errors="ignore"))
print(f"--- Read {len(lines)} lines of text")
input()

#
# Save LAS file to disk
#

filename = os.path.basename(filepath)
with open(filename, 'w') as f:
    for line in lines:
        print(line, file=f)
print(f"--- Wrote all lines to {filename}")
input()

#
# Find index of data section
#

idx = 0
for line in lines:
    if line.startswith('~A'):
        break
    idx += 1
print(f"--- Data section starts at line {idx}")
input()

#
# Extract a curve
#

curve = []
for row in lines[idx+1:]:
    cols = row.split()
    cell = cols[1]
    curve.append(float(cell))
print(f"--- Extracted {len(curve)} values. minvalue={min(curve)}, maxvalue={max(curve)}")
input()

#
# Clean up values in curve
#

import numpy as np
curve = np.array(curve)
curve = np.where(curve==-999.25, np.nan, curve)
print(f"--- Cleaned up curve (replacing -999.25 with NaN)")
input()

#
# Plot curve
#

plotfilename = 'demoapp.png'
import matplotlib.pyplot as plt
plt.plot(curve)
plt.savefig(plotfilename)
print(f"--- Curve plotted into: {plotfilename}")
input()

#
# Start webapp to serve the plot
#

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.send_file('./demoapp.png', mimetype='image/png')

app.run()
