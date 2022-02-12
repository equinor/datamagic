import os
import collections
import azure.storage.blob

#URL = r'https://datavillagesa.blob.core.windows.net/volve?sv=2018-03-28&sr=c&sig=2CCvEBPWiojChDE1N%2BJw%2ByZ%2Fn5oMf3iXSEUZBm5XMq8%3D&se=2022-03-13T23%3A04%3A36Z&sp=rl'
URL = r'https://datavillagesa.blob.core.windows.net/northernlights?sv=2018-03-28&sr=c&sig=VTWTxWY%2BT7KQ8Y3m93%2B298%2FUjVMi6ebEyEee%2Ffu16SY%3D&se=2022-03-03T22%3A16%3A48Z&sp=rl'

container = azure.storage.blob.ContainerClient.from_container_url(URL)

blobs = []
for blob in container.list_blobs():
    blobs.append(blob)

for blob in blobs:
    print(f'{blob.size:>20,} {blob.name}')

total_size = sum(blob.size for blob in blobs)
MB = 1024*1024
TB = MB*MB

print('=== TOTAL')
print(f'{total_size:>20,} {len(blobs):>8} files ({total_size/MB:.2f} MB, {total_size/TB:.2f} TB)')

tally_bytes = collections.defaultdict(int)
tally_count = collections.defaultdict(int)
for blob in blobs:
    (_, ext) = os.path.splitext(blob.name)
    ext = ext.upper()[1:]
    tally_bytes[ext] += blob.size
    tally_count[ext] += 1

print('=== FILETYPES')
for (ext,_) in sorted(tally_count.items(), key=lambda item: item[1], reverse=True):
    print(f'{tally_bytes[ext]:>20,} {tally_count[ext]:>8} {ext:<20}')
