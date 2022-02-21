import fileinput

total = 0
with fileinput.input() as f:
    for line in f:
        if line.strip():
            total += int(line)
print(total)
