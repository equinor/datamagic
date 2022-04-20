import os
import azure.storage.blob

def get_container():
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)

def get_list_of_lasfiles(container):
    files = []
    for blob in container.list_blobs():
        if blob.name.endswith('.LAS'):
            files.append(blob.name)
    return files

def print_list_of_lasfiles(container):
    lasfiles = get_list_of_lasfiles(container)
    for file in lasfiles:
        print(file)

def read_lasfile(container, filename):
    if not filename.endswith(".LAS"):
        raise OSError("Probably not a LAS file")
    blob_client = container.get_blob_client(filename)
    data = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in data.splitlines():
        lines.append(line.decode("ascii", errors="ignore"))
    return lines

def get_header_section(lines):
    headerlines = []
    for line in lines:
        if line.startswith("~A"):
            break
        headerlines.append(line)
    return headerlines

def get_data_section(lines):
    datalines = []
    idx = 0
    for line in lines:
        if line.startswith("~A"):
            break
        idx += 1
    return lines[idx+1:]

def print_header_section(lines):
    headerlines = get_header_section(lines)
    for line in headerlines:
        print(line)

def print_data_section(lines):
    datalines = get_data_section(lines)
    for line in datalines:
        print(line)

def main():
    container = get_container()
    lines = read_lasfile(container, "31_5-7 Eos/07.Borehole_Seismic/TZV_TIME_SYNSEIS_2020-01-17_2.LAS")
    #print_header_section(lines)
    print_data_section(lines)

if __name__ == '__main__':
    main()


