import os
import sys
import azure.storage.blob

def download_file(container_url, path):
    container = azure.storage.blob.ContainerClient.from_container_url(container_url)
    filename = os.path.basename(path)
    blob_client = container.get_blob_client(path)
    if blob_client.exists():
        bytes = blob_client.download_blob().readall()
        with open(filename, "wb") as file:
            file.write(bytes)
    else:
        print(f'File not found: {path}')
        return 1
    return 0

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print(f"usage: {sys.argv[0]} [FILE]... - download FILE(s) from container")
        print(f"Hint: Environment variable CONTAINER_URL must be defined")
        sys.exit(1)

    URL = os.environ.get('CONTAINER_URL')
    if URL == None:
        print('Please specify the container in CONTAINER_URL')
        sys.exit(1)

    for filename in sys.argv[1:]:
        retval = download_file(URL, filename)
        if retval != 0:
            sys.exit(retval)

    sys.exit(0)
