import os
import azure.storage.blob

def get_container_url():
    return os.environ['CONTAINER_URL']

def create_container_client(url):
    return azure.storage.blob.ContainerClient.from_container_url(url)

def all_files(container):
    files = []
    for blob in container.list_blobs():
        name = blob.name
        ext = name.split('.')[-1].upper()
        size = blob.size
        files.append((name, ext, size))
    return files

def main():
    url = get_container_url()
    container = create_container_client(url)
    files = all_files(container)

    print("Number of files in container:", len(files))

    lasfiles = [name for name, ext, size in files if ext == 'LAS']
    print("Number of LAS files in container:", len(lasfiles))

    gb = 1024 ** 3
    totalsize = sum(size for _, _, size in files)
    print(f"Total size in GB: {totalsize / gb:.2f}")

    filetypes = {}
    for _, ext, size in files:
        if ext in filetypes:
            filetypes[ext].append(size)
        else:
            filetypes[ext] = [size]

    for filetype, sizes in filetypes.items():
        print(f"{len(sizes):>4} {filetype:<8} {sum(sizes)}")

if __name__ == '__main__':
    main()

