"""Download file from a storage container."""

import os
import sys
import azure.storage.blob as asb


def download_file(container_url, path):
    """Download file a storage container."""
    container = asb.ContainerClient.from_container_url(container_url)
    filename = os.path.basename(path)
    blob_client = container.get_blob_client(path)
    if blob_client.exists():
        data = blob_client.download_blob().readall()
        with open(filename, "wb") as file:
            file.write(data)
    else:
        print(f'File not found: {path}')
        return 1
    return 0


def main(argv):
    """Parse arguments and run program."""
    if len(argv) == 1:
        print(f"usage: {argv[0]} [FILE]... - download FILE(s) from container")
        print("Hint: Environment variable CONTAINER_URL must be defined")
        return 1

    url = os.environ.get('CONTAINER_URL')
    if not url:
        print('Please specify the container in CONTAINER_URL')
        return 1

    for filename in argv[1:]:
        retval = download_file(url, filename)
        if retval != 0:
            sys.exit(retval)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
