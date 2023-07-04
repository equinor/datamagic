import os
import azure.storage.blob

def main():
    url = os.environ['CONTAINER_URL']

    container = azure.storage.blob.ContainerClient.from_container_url(url)

    for blob in container.list_blobs():
        print(f'{blob.size:<20}{blob.name}')

if __name__ == "__main__":
    main()
