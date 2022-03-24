import os
import sys
import azure.storage.blob

def get_container():
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)

def is_lasfile(filename):
    return filename.endswith('.LAS')

def get_list_of_lasfiles(container):
    files = []
    for blob in container.list_blobs():
        if is_lasfile(blob.name):
            files.append(blob.name)
    return files

def print_lasfiles(container):
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


def find_section_index(lines, prefix):
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


def print_helpmessage():
    """Print help message."""
    print("usage: mylastool.py <command> [file]")
    print("examples:")
    print("    python mylastool.py list")
    print("    python mylastool.py header A/B/C.LAS")
    print("    python mylastool.py data   A/B/C.LAS")
    print("also, remember to set CONTAINER_URL")

def main(argv):

    if len(argv) < 2:
        print_helpmessage()
        return 1

    command = argv[1]

    if command not in ('list', 'header', 'data'):
        print('error: unknown command')
        print_helpmessage()
        return 1

    container = get_container()

    if command == 'list':
        print_lasfiles(container)
        return 0

    if len(argv) < 3:
        print('error: expected a filename')
        print_helpmessage()
        return 1

    lasfile = argv[2]
    lines = read_lasfile(container, lasfile)

    if command == 'header':
        print_header_section(lines)
        return 0

    if command == 'data':
        print_data_section(lines)
        return 0

    print('Huh?')
    print_helpmessage()
    return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))


