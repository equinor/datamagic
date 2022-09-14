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

def read_lasfile(container, filename):
    """Read given LAS file from container."""
    if not filename.upper().endswith('.LAS'):
        raise OSError("Probably not a LAS file")
    blob_client = container.get_blob_client(filename)
    data = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in data.splitlines():
        lines.append(line.decode('ascii', errors='ignore'))
    return lines

def find_section_index(lines, prefix):
    """Find index of first line with given prefix."""
    idx = 0
    for line in lines:
        if line.startswith(prefix):
            break
        idx += 1
    return idx

def get_header_section(lines):
    return lines[:find_section_index(lines, '~A')]

def print_header_section(lines):
    for line in get_header_section(lines):
        print(line)

def get_data_section(lines):
    return lines[find_section_index(lines, '~A')+1:]

def print_data_section(lines):
    for line in get_data_section(lines):
        print(line)

def main():
    container = get_container()
    #files = get_list_of_lasfiles(container)
    #print_list_of_files(files)

    lasfile = '31_5-7 Eos/07.Borehole_Seismic/TZV_TIME_SYNSEIS_2020-01-17_2.LAS'
    lines = read_lasfile(container, lasfile)
    print_header_section(lines)
    #print_data_section(lines)

if __name__ == '__main__':
    main()
