import os
import azure.storage.blob

def get_container():
    URL = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(URL)

def get_list_of_lasfiles(container):
    files = []
    for blob in container.list_blobs():
        if blob.name.endswith('.LAS'):
            files.append(blob.name)
    return files

def print_list_of_lasfiles(container):
    files = get_list_of_lasfiles(container)
    for name in files:
        print(name)

def main():
    container = get_container()
    files = get_list_of_lasfiles(container)
    print(len(files))
    
    print_list_of_lasfiles(container)

if __name__ == '__main__':
    main()
