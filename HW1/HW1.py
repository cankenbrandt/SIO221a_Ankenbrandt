import os
from dataclasses import dataclass, field

import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import get_xyear_pier_data

temperature_2021 = get_xyear_pier_data.get_pier_data(xyear = 2021)

print('The mean is:', np.mean(temperature_2021.temperature)) # type: ignore
print('The standard deviation is:', np.std(temperature_2021.temperature, ddof=1))


fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(temperature_2021.dnum, temperature_2021.temperature, linewidth=.75)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.tick_params(labelsize=14)
ax.set_xlabel('month', fontsize=14)
ax.set_ylabel('temperature (°C)', fontsize=14)
ax.set_title('Scripps Pier Data - 2021', fontsize=14)
ax.grid(True)


pdfbins = np.arange(temperature_2021.temperature.min(), temperature_2021.temperature.max(), 0.25)

fig, ax1 = plt.subplots(figsize=(10, 6))
pdf = ax1.hist(temperature_2021.temperature, bins=pdfbins, density=True) # type: ignore
ax1.set_ylabel('probability density', fontsize=14)
ax1.set_xlabel('temperature (°C)', fontsize=14)
ax1.set_title('PDF', fontsize=16)




#for question 2
#building the whole timeseries
pier_record = get_xyear_pier_data.get_pier_data(xyear = 2005)
for i in range(2006, 2022): 
    pier_record.temperature = np.concatenate([pier_record.temperature, get_xyear_pier_data.get_pier_data(xyear = i).temperature])
    pier_record.dnum = np.concatenate([pier_record.dnum, get_xyear_pier_data.get_pier_data(xyear = i).dnum])
    pier_record.pressure = np.concatenate([pier_record.pressure, get_xyear_pier_data.get_pier_data(xyear = i).pressure])

#plotting the larger timeseries, cutting off the outlier
fig, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(pier_record.dnum, pier_record.temperature, linewidth=.4)
ax2.xaxis.set_major_locator(mdates.YearLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax2.tick_params(labelsize=9)
ax2.set_ylim(top=27, bottom = 8)
ax2.set_xlabel('year', fontsize=14)
ax2.set_ylabel('temperature (°C)', fontsize=14)
ax2.set_title('Scripps Pier Data 2005-2021', fontsize=14)
ax2.grid(True)

#Now that we can see it, lets look at the mean and std of the longer timeseries
print('The mean is:', np.mean(pier_record.temperature))
print('The standard deviation is:', np.std(pier_record.temperature, ddof=1))


#Now let's look at the summer of 2016
temperature_2016 = get_xyear_pier_data.get_pier_data(xyear = 2016, date_start = '2016-07-01', date_end = '2016-09-30')


fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(temperature_2016.dnum, temperature_2016.temperature, linewidth=.75)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.tick_params(labelsize=14)
ax.set_xlabel('month', fontsize=14)
ax.set_ylabel('temperature (°C)', fontsize=14)
ax.set_title('Scripps Pier Data - Summer 2016', fontsize=14)
ax.grid(True)
plt.show()