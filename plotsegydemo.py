import segyio
import numpy as np
import matplotlib.pyplot as plt

traces = []
filename = 'VSPZO_RAW_2020-01-17_4.SEGY'
with segyio.open(filename, strict=False) as f:
    for trace in f.trace:
        traces.append(list(trace))
plt.imshow(traces, vmin=-0.01, vmax=0.01)
plt.savefig('plotsegydemo.png')
