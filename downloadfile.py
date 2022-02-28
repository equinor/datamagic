"""Download file from a storage container."""

import os
import azure.storage.blob

url = os.environ['CONTAINER_URL']
container = azure.storage.blob.ContainerClient.from_container_url(url)
path = '31_5-7 Eos/07.Borehole_Seismic/TZV_TIME_SYNSEIS_2020-01-17_2.LAS'
blob_client = container.get_blob_client(path)
data = blob_client.download_blob().readall()
filename = os.path.basename(path)
with open(filename, "wb") as file:
    file.write(data)
