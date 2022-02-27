"""Demonstrate segyio."""

import segyio
import matplotlib.pyplot as plt

traces = []
with segyio.open('VSPZO_RAW_2020-01-17_4.SEGY', strict=False) as f:
    for trace in f.trace:
        traces.append(list(trace))
plt.imshow(traces, vmin=-0.01, vmax=0.01)
plt.savefig('plotsegydemo.png')
