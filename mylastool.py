import os
import azure.storage.blob

def get_container():
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)

def print_list_of_lasfiles(container):
    for blob in container.list_blobs():
        if blob.name.endswith('.LAS'):
            print(f"{blob.size:<20}{blob.name}")

def main():
    container = get_container()
    print_list_of_lasfiles(container)

if __name__ == '__main__':
    main()