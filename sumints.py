import fileinput

total = 0
with fileinput.input() as f:
    for line in f:
        total += int(line)
print(total)
