import os
import azure.storage.blob

def get_container():
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)

def get_list_of_lasfiles(container):
    """Get list of LAS files in a container"""
    files = []
    for blob in container.list_blobs():
        if blob.name.upper().endswith('.LAS'):
            files.append(blob.name)
    return files

def print_list_of_files(files):
    for filename in files:
        print(filename)

def main():
    container = get_container()
    files = get_list_of_lasfiles(container)
    print_list_of_files(files)

if __name__ == '__main__':
    main()
