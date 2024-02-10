import numpy as np
import re
import pytplot
import xarray

def get_filenames(prefix, all_days, suffix):
    filenames = []

    for day in all_days:
        yyyy, mm, dd = re.split('[-]', str(day))
        filenames.append(f'{prefix}_{yyyy}{mm}{dd}_{suffix}.cdf')
    
    return filenames


def read_cdf(start_time, end_time, cdf_files_dir, file_prefix, file_suffix, datatype):
    '''
    Alternative way to read local files if not using pyspedas.

    Parameters:
    -----------
    file_prefix : string
                  The prefix string for the files to read.

    start_time : string
                 The starting time in array form.

    end_time : string
               The ending time in array form.

    file_suffix : string
                  The suffix string for the files to read.
    '''
    # getting the start time of the first date and the end time of the last date
    start_date, start_time = re.split('[/]', start_time)
    end_date, end_time = re.split('[/]', end_time)

    # calculating the days between start date and end date
    all_days = np.arange(np.datetime64(start_date), np.datetime64(end_date) + 1)

    # making the array of filenames to read in sequence
    filenames = get_filenames(file_prefix, all_days, file_suffix)

    # getting the start and end times in datetime64
    start_time = np.datetime64(f'{start_date}T{start_time}')
    end_time = np.datetime64(f'{end_date}T{end_time}')

    # if it is just one day
    if(len(filenames)==1):
        mag = pytplot.cdf_to_tplot(f'{cdf_files_dir}/{filenames[0]}')
        data = pytplot.data_quants[datatype]
        time = data.time
        time_mask = time > start_time
        data_total = data[time_mask]

    # if it is two days
    elif(len(filenames)==2):
        # day 1
        mag = pytplot.cdf_to_tplot(f'{cdf_files_dir}/{filenames[0]}')
        data = pytplot.data_quants[datatype]
        time = data.time
        time_mask = time > start_time
        data_total = data[time_mask]

        # day 2
        mag = pytplot.cdf_to_tplot(f'{cdf_files_dir}/{filenames[1]}')
        data = pytplot.data_quants[datatype]
        time = data.time
        time_mask = time < end_time
        data_total = xarray.concat([data_total, data[time_mask]], "time")

    # if it is more than two days
    else:
        # day 1
        mag = pytplot.cdf_to_tplot(f'{cdf_files_dir}/{filenames[0]}')
        data = pytplot.data_quants[datatype]
        time = data.time
        time_mask = time > start_time
        data_total = data[time_mask]

        # appending the intermediate days 
        for i in range(1, len(filenames)-1):
            mag = pytplot.cdf_to_tplot(f'{cdf_files_dir}/{filenames[i]}')
            data = pytplot.data_quants[datatype]
            # appending the full day without any slicing in time
            data_total = xarray.concat([data_total, data], "time")

        # day -1
        mag = pytplot.cdf_to_tplot(f'{cdf_files_dir}/{filenames[-1]}')
        data = pytplot.data_quants[datatype]
        time = data.time
        time_mask = time < end_time
        data_total = xarray.concat([data_total, data[time_mask]], "time")

    return data_total