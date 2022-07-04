"""My LAS tool."""

import os
import azure.storage.blob


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


def main():
    """My LAS file tool."""
    container = get_container()
    print_list_of_lasfiles(container)

if __name__ == '__main__':
    main()
