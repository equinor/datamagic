"""My LAS tool."""

import os
import azure.storage.blob
import sys


def get_container():
    """Get a handle to an Azure Storage Blob container."""
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)


def get_list_of_lasfiles(container):
    """Get list of LAS files in a container."""
    files = []
    for blob in container.list_blobs():
        if blob.name.endswith('.LAS'):
            files.append(blob.name)
    return files


def print_list_of_lasfiles(container):
    """Print pretty directory listing of LAS files in a container."""
    for name in get_list_of_lasfiles(container):
        print(name)


def read_lasfile(container, filename):
    """Read given LAS file from container."""
    if not filename.endswith('.LAS'):
        raise OSError("Probably not a LAS file")
    blob_client = container.get_blob_client(filename)
    data = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in data.splitlines():
        lines.append(line.decode("ascii", errors='ignore'))
    return lines


def print_header_section(lines):
    for line in lines:
        if line.startswith('~A'):
            break
        print(line)
        
def main(argv):
    """My LAS file tool."""

    container = get_container()

    if len(argv) == 1:
        print_list_of_lasfiles(container)
        return 0

    if len(argv) == 2:
        filename = argv[1]
        lines = read_lasfile(container, filename)
        print_header_section(lines)
        return 0

    print('Unknown arguments')
    return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
