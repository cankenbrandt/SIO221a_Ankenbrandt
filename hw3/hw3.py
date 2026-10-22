import os
from dataclasses import dataclass, field

import datetime
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd


#Question 1

#read in 2015 data
buoy_data2015 = pd.read_csv(r"C:\Users\cva43\SIO221a_Ankenbrandt\data\46047_2015.txt", 
                        sep=r"\s+", 
                        skiprows=[1], 
                        parse_dates=True, 
                        na_values=["99.0", "999", "999.0", "9999.0", "99.00"],)

#read in 2016 data
buoy_data2016 = pd.read_csv(r"C:\Users\cva43\SIO221a_Ankenbrandt\data\46047_2016.txt", 
                        sep=r"\s+", 
                        skiprows=[1], 
                        parse_dates=True, 
                        na_values=["99.0", "999", "999.0", "9999.0", "99.00"],)

#combine years into a single df
buoy_data = pd.concat([buoy_data2015, buoy_data2016], ignore_index=True)

#convert date columns to datetime format
buoy_data['date'] = pd.to_datetime({'year': buoy_data['#YY'], 
                                    'month': buoy_data['MM'], 
                                    'day': buoy_data['DD'], 
                                    'hour': buoy_data['hh'], 
                                    'minute': buoy_data['mm']})

#remove original date columns + set datetime as index
buoy_data.drop(columns=['#YY', 'MM', 'DD', 'hh', 'mm'], inplace=True)
buoy_data.set_index('date', inplace=True)


#plot wind speed data for 2015-2016
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(buoy_data.index, buoy_data['WSPD'], linewidth=.75)
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax.tick_params(axis='x', which='major', labelsize=12, length=8)
ax.tick_params(axis='x', which='minor', labelsize=9) 
ax.set_xlim(buoy_data.index.min(), buoy_data.index.max())
ax.set_xlabel('year', fontsize=14)
ax.set_ylabel('wind speed (m/s)', fontsize=14)
ax.set_title('NOAA buoy 46047 - Wind Speed 2015 - 2016', fontsize=14)
ax.grid(True)

#plot wave height for 2015-2016
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(buoy_data.index, buoy_data['WVHT'], linewidth=.75)
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax1.xaxis.set_minor_locator(mdates.MonthLocator())
ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax1.tick_params(axis='x', which='major', labelsize=12, length=8)
ax1.tick_params(axis='x', which='minor', labelsize=9) 
ax1.set_xlim(buoy_data.index.min(), buoy_data.index.max())
ax1.set_xlabel('year', fontsize=14)
ax1.set_ylabel('wave height (m)', fontsize=14)
ax1.set_title('NOAA buoy 46047 - Wave Height 2015 - 2016', fontsize=14)
ax1.grid(True)

#plot water temperature for 2015-2016
fig, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(buoy_data.index, buoy_data['WTMP'], linewidth=.75)
ax2.xaxis.set_major_locator(mdates.YearLocator())
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax2.xaxis.set_minor_locator(mdates.MonthLocator())
ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax2.tick_params(axis='x', which='major', labelsize=12, length=8)
ax2.tick_params(axis='x', which='minor', labelsize=9) 
ax2.set_xlim(buoy_data.index.min(), buoy_data.index.max())
ax2.set_xlabel('year', fontsize=14)
ax2.set_ylabel('water temperature (°C)', fontsize=14)
ax2.set_title('NOAA buoy 46047 - Water Temperature 2015 - 2016', fontsize=14)
ax2.grid(True)

#plot air temperature for 2015-2016
fig, ax3 = plt.subplots(figsize=(10, 6))
ax3.plot(buoy_data.index, buoy_data['ATMP'], linewidth=.75)
ax3.xaxis.set_major_locator(mdates.YearLocator())
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax3.xaxis.set_minor_locator(mdates.MonthLocator())
ax3.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax3.tick_params(axis='x', which='major', labelsize=12, length=8)
ax3.tick_params(axis='x', which='minor', labelsize=9) 
ax3.set_xlim(buoy_data.index.min(), buoy_data.index.max())
ax3.set_xlabel('year', fontsize=14)
ax3.set_ylabel('air temperature (°C)', fontsize=14)
ax3.set_title('NOAA buoy 46047 - Air Temperature 2015 - 2016', fontsize=14)
ax3.grid(True)

#Question 2 

# cutting off 2014 and 2017 data for prettier plots
buoy_data = buoy_data.iloc[1:-1]

# getting monthly means of everything at MonthStart (MS) for plotting
monthly_mean_buoy_data = buoy_data.resample('MS').mean()
monthly_std_buoy_data = buoy_data.resample('MS').std()
n_eff = pd.Series(monthly_mean_buoy_data.index.days_in_month / 7, index=monthly_mean_buoy_data.index) # type: ignore
#lmao I just spent 10 minutes chasing the error of why feb16 doesnt have 28 dyas

#get that standard error of the mean babbyyyyyy
monthly_sem_buoy_data = monthly_std_buoy_data.div(np.sqrt(n_eff), axis=0)

#I ended up having to ask Claude for help with data structures in python
#as I accidentally ended up with half data frames and half arrays of some kind

#plot wind speed data monthly averages w errorbars for 2015-2016
fig, ax4 = plt.subplots(figsize=(10, 6))
#python equivalent of matlab errorbar function
ax4.errorbar(monthly_mean_buoy_data.index, 
             monthly_mean_buoy_data['WSPD'], 
             yerr=monthly_sem_buoy_data['WSPD'], 
             fmt='-o', 
             linewidth=.75, 
             capsize=5)
ax4.xaxis.set_major_locator(mdates.YearLocator())
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax4.xaxis.set_minor_locator(mdates.MonthLocator())
ax4.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax4.tick_params(axis='x', which='major', labelsize=12, length=8)
ax4.tick_params(axis='x', which='minor', labelsize=9) 
ax4.set_xlim(pd.Timestamp('2014-12-15'), pd.Timestamp('2016-12-31')) # type: ignore
ax4.set_xlabel('year', fontsize=14)
ax4.set_ylabel('wind speed (m/s)', fontsize=14)
ax4.set_title('NOAA buoy 46047 - Wind Speed 2015 - 2016', fontsize=14)
ax4.grid(True)


#plot wave height data monthly averages w errorbars for 2015-2016
fig, ax5 = plt.subplots(figsize=(10, 6))
#python equivalent of matlab errorbar function
ax5.errorbar(monthly_mean_buoy_data.index, 
             monthly_mean_buoy_data['WVHT'], 
             yerr=monthly_sem_buoy_data['WVHT'], 
             fmt='-o', 
             linewidth=.75, 
             capsize=5)
ax5.xaxis.set_major_locator(mdates.YearLocator())
ax5.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax5.xaxis.set_minor_locator(mdates.MonthLocator())
ax5.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax5.tick_params(axis='x', which='major', labelsize=12, length=8)
ax5.tick_params(axis='x', which='minor', labelsize=9) 
ax5.set_xlim(pd.Timestamp('2014-12-15'), pd.Timestamp('2016-12-31')) # type: ignore
ax5.set_xlabel('year', fontsize=14)
ax5.set_ylabel('wave height (m)', fontsize=14)
ax5.set_title('NOAA buoy 46047 - Wave Height 2015 - 2016', fontsize=14)
ax5.grid(True)


#plot water temperature data monthly averages w errorbars for 2015-2016
fig, ax6 = plt.subplots(figsize=(10, 6))
#python equivalent of matlab errorbar function
ax6.errorbar(monthly_mean_buoy_data.index, 
             monthly_mean_buoy_data['WTMP'], 
             yerr=monthly_sem_buoy_data['WTMP'], 
             fmt='-o', 
             linewidth=.75, 
             capsize=5)
ax6.xaxis.set_major_locator(mdates.YearLocator())
ax6.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax6.xaxis.set_minor_locator(mdates.MonthLocator())
ax6.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax6.tick_params(axis='x', which='major', labelsize=12, length=8)
ax6.tick_params(axis='x', which='minor', labelsize=9) 
ax6.set_xlim(pd.Timestamp('2014-12-15'), pd.Timestamp('2016-12-31')) # type: ignore
ax6.set_xlabel('year', fontsize=14)
ax6.set_ylabel('water temperature (°C)', fontsize=14)
ax6.set_title('NOAA buoy 46047 - Water Temperature 2015 - 2016', fontsize=14)
ax6.grid(True)

#plot air temperature data monthly averages w errorbars for 2015-2016
fig, ax7 = plt.subplots(figsize=(10, 6))
#python equivalent of matlab errorbar function
ax7.errorbar(monthly_mean_buoy_data.index, 
             monthly_mean_buoy_data['ATMP'], 
             yerr=monthly_sem_buoy_data['ATMP'], 
             fmt='-o', 
             linewidth=.75, 
             capsize=5)
ax7.xaxis.set_major_locator(mdates.YearLocator())
ax7.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax7.xaxis.set_minor_locator(mdates.MonthLocator())
ax7.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax7.tick_params(axis='x', which='major', labelsize=12, length=8)
ax7.tick_params(axis='x', which='minor', labelsize=9) 
ax7.set_xlim(pd.Timestamp('2014-12-15'), pd.Timestamp('2016-12-31')) # type: ignore
ax7.set_xlabel('year', fontsize=14)
ax7.set_ylabel('air temperature (°C)', fontsize=14)
ax7.set_title('NOAA buoy 46047 - Air Temperature 2015 - 2016', fontsize=14)
ax7.grid(True)
plt.show()
