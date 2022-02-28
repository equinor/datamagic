"""My tool for working with LAS files in an azure storage container."""

import os
import sys
import azure.storage.blob


def is_probably_a_las_file(filename):
    """Check if filename has .LAS extension."""
    return filename.endswith('.LAS')


def listfiles(container, suffix=''):
    """List files in a container, filter on given suffix."""
    files = []
    for blob in container.list_blobs():
        if blob.name.endswith(suffix):
            files.append((blob.size, blob.name))
    return files


def printdirectory(files):
    """Print a pretty directory listing of files returned by listfiles()."""
    for (size, name) in files:
        print(f"{size:>20} {name}")


def readtextfile(container, filename):
    """Read given text file from container."""
    if not filename.endswith(".LAS"):
        raise Exception("Probably not a LAS file")
    blob_client = container.get_blob_client(filename)
    data = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in data.splitlines():
        lines.append(line.decode("ascii", errors='ignore'))
    return lines


def sectionindex(lines, prefix):
    """Find index of first line with given prefix."""
    idx = 0
    for line in lines:
        if line.strip().startswith(prefix):
            break
        idx += 1
    return idx


def headersection(lines):
    """Return the lines for the header section."""
    return lines[0:sectionindex(lines, '~A')]


def printheadersection(lines):
    """Print the header section."""
    for line in headersection(lines):
        print(line)


def datasection(lines):
    """Return the lines for the data section."""
    return lines[sectionindex(lines, '~A')+1:]


def printdatasection(lines):
    """Print the data section."""
    for line in datasection(lines):
        print(line)


def curvemnemonics(lines):
    """Return list of curve mnemonics."""
    startidx = sectionindex(lines, "~C")
    endidx = sectionindex(lines[startidx+1:], "~")
    mnemonics = []
    for line in lines[startidx+1:startidx+1+endidx]:
        if line.startswith('#'):
            continue
        (mnem, *_) = line.split('.')
        mnemonics.append(mnem.strip())
    return mnemonics


def printcurves(lines):
    """Print the curve mnemonics."""
    print(*curvemnemonics(lines))


def getcontainer():
    """Create a container by using the CONTAINER_URL env variable."""
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)


def printhelp_and_die():
    """Print help message and call exit."""
    app = sys.argv[0]
    print(f"""usage: {app} <command> [filename]
eg:    {app} list
       {app} header <filename>
       {app} data <filename>
       {app} curves <filename>""")
    sys.exit(1)


def main(argv):
    """Parse as list of arguments and do magic."""
    container = getcontainer()

    if len(argv) == 1 or argv[1] not in ('list', 'header', 'data', 'curves'):
        printhelp_and_die()

    command = argv[1]

    if command == 'list':
        lasfiles = listfiles(container, ".LAS")
        printdirectory(lasfiles)
        return 0

    if len(argv) != 3:
        print('error: expected a filename')
        printhelp_and_die()

    filename = argv[2]
    lines = readtextfile(container, filename)

    if command == 'header':
        printheadersection(lines)
    elif command == 'data':
        printdatasection(lines)
    elif command == 'curves':
        printcurves(lines)
    else:
        raise Exception("Unexpected command:" + command)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[:]))

# References:
# https://www.cwls.org/wp-content/uploads/2017/02/Las2_Update_Feb2017.pdf
# https://docs.microsoft.com/en-us/python/api/azure-storage-blob/?view=azure-python
