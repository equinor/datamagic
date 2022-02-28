"""My tool for working with LAS files in an azure storage container."""

import os
import sys
import azure.storage.blob


def list_files(container, *, suffix=''):
    """List files in a container, filter on given suffix."""
    files = []
    for blob in container.list_blobs():
        if blob.name.endswith(suffix):
            files.append((blob.size, blob.name))
    return files


def print_directory(files):
    """Print a pretty directory listing of files returned by list_files()."""
    for (size, name) in files:
        print(f"{size:>20} {name}")


def read_lasfile(container, filename):
    """Read given text file from container."""
    if not filename.endswith(".LAS"):
        raise OSError("Probably not a LAS file")
    blob_client = container.get_blob_client(filename)
    data = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in data.splitlines():
        lines.append(line.decode("ascii", errors='ignore'))
    return lines


def find_section_index(lines, prefix):
    """Find index of first line with given prefix."""
    idx = 0
    for line in lines:
        if line.strip().startswith(prefix):
            break
        idx += 1
    return idx


def get_header_section(lines):
    """Return the lines for the header section."""
    return lines[0:find_section_index(lines, '~A')]


def print_header_section(lines):
    """Print the header section."""
    for line in get_header_section(lines):
        print(line)


def get_data_section(lines):
    """Return the lines for the data section."""
    return lines[find_section_index(lines, '~A')+1:]


def print_data_section(lines):
    """Print the data section."""
    for line in get_data_section(lines):
        print(line)


def get_curve_mnemonics(lines):
    """Return list of curve mnemonics."""
    startidx = find_section_index(lines, "~C")
    endidx = find_section_index(lines[startidx+1:], "~")
    mnemonics = []
    for line in lines[startidx+1:startidx+1+endidx]:
        if line.startswith('#'):
            continue
        (mnem, *_) = line.split('.')
        mnemonics.append(mnem.strip())
    return mnemonics


def print_curve_mnemonics(lines):
    """Print the curve mnemonics."""
    print(*get_curve_mnemonics(lines))


def get_container():
    """Create a container by using the CONTAINER_URL env variable."""
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)


def print_helpmessage():
    """Print help message and call exit."""
    app = sys.argv[0]
    print(f"""usage: {app} <command> [filename]
eg:    {app} list
       {app} header <filename>
       {app} data <filename>
       {app} curves <filename>""")


def main(argv):
    """Parse as list of arguments and do magic."""
    container = get_container()

    if len(argv) == 1 or argv[1] not in ('list', 'header', 'data', 'curves'):
        print_helpmessage()
        return 1

    command = argv[1]

    if command == 'list':
        lasfiles = list_files(container, suffix=".LAS")
        print_directory(lasfiles)
        return 0

    if len(argv) != 3:
        print('error: expected a filename')
        print_helpmessage()
        return 1

    filename = argv[2]
    lines = read_lasfile(container, filename)

    if command == 'header':
        print_header_section(lines)
    elif command == 'data':
        print_data_section(lines)
    elif command == 'curves':
        print_curve_mnemonics(lines)
    else:
        raise OSError("Unexpected command:" + command)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[:]))

# References:
# https://www.cwls.org/wp-content/uploads/2017/02/Las2_Update_Feb2017.pdf
# https://docs.microsoft.com/en-us/python/api/azure-storage-blob/?view=azure-python
