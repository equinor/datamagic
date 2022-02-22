import os
import sys
import azure.storage.blob

def listfiles(container, suffix):
    lasfiles = []
    for blob in container.list_blobs():
        if blob.name.endswith(suffix):
            lasfiles.append((blob.size, blob.name))
    return lasfiles

def readlasfile(container, filename):
    blob_client = container.get_blob_client(filename)
    bytes = blob_client.download_blob().content_as_bytes()
    lines = []
    for line in bytes.splitlines():
        lines.append(line.decode("ascii", errors='ignore'))
    return lines

def printheader(container, filename):
    lines = readlasfile(container, filename)
    for line in lines:
        if line.startswith("~A"):
            return
        print(line)

def printdata(container, filename):
    lines = readlasfile(container, filename)
    inside_datasegment = False
    for line in lines:
        if inside_datasegment:
            print(line)
        if line.startswith("~A"):
            inside_datasegment = True

def getcontainer():
    url = os.environ['CONTAINER_URL']
    return azure.storage.blob.ContainerClient.from_container_url(url)

def printhelp_and_die(msg = "", retval = 1):
    if msg:
        print(msg)
    print(f'usage: {sys.argv[0]} <command> ...')
    sys.exit(retval)

def main(argv):
    commands = ['list', 'header', 'data', 'info', 'curves', 'download']
    if len(argv) == 1:
        printhelp_and_die()
    if argv[1] not in commands:
        printhelp_and_die("Command not recognized. Try:", *commands)
    container = getcontainer()
    lasfiles = listfiles(container, ".LAS")
    command = argv[1]
    if command == 'list':
        for ((idx, (size, name))) in enumerate(lasfiles):
            print(f"{'[' + str(idx) + ']':<6} {size:>20} {name}")
    elif command == 'header':
        if len(argv) < 3:
            printhelp_and_die(f"missing argument: {command} <idx>")
        idx = int(argv[2])
        (_, filename) = lasfiles[idx]
        printheader(container, filename)
    elif command == 'data':
        if len(argv) != 3:
            printhelp_and_die(f"missing argument: {command} <idx>")
        idx = int(argv[2])
        (_, filename) = lasfiles[idx]
        printdata(container, filename)
    else:
        print('not implemented yet')
    return 0

if __name__ == '__main__':
    retval = main(sys.argv[:])
    sys.exit(retval)
