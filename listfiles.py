import os
import azure.storage.blob

# remember export CONTAINER_URL="https://datavillagesa.blob.core.windows.net/northernlights?s.....sp=rl"

URL = os.environ['CONTAINER_URL']

container = azure.storage.blob.ContainerClient.from_container_url(URL)

for blob in container.list_blobs():
    print(f"{blob.size:<20} {blob.name}")


