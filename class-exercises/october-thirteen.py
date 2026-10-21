import os
from dataclasses import dataclass, field

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.stats as stats
from scipy.stats import rayleigh

n = 2

# Define an array with n columns of random values, each with 100000 elements.
rng = np.random.default_rng(221) # so the figure is reproducible
b = rng.random((10000, n))

result = []
for i in range(10000):
    result.append(np.sqrt(np.sum(b[i,:]**2)))

fig, ax1 = plt.subplots(figsize=(10, 6))
pdf = ax1.hist(result, bins=100, density=True) # type: ignore
ax1.set_ylabel('probability density', fontsize=14)
ax1.set_xlabel('something', fontsize=14)
ax1.set_title('PDF', fontsize=16)







