import numpy as np
import pyspedas
import pytplot
import re

import misc_functions as misc_FN

def time_str2dt64(time_str):
    '''
    Converts string time in yyyy-mm-dd/hh:mm:ss to yyyy-mm-ddThh:mm:ss in np.datetime64.

    Parameters:
    -----------
    time_str : string
               Input time string.
    
    Returns:
    --------
    time_dt64 : numpy.datetime64
                Time in datetime64 format.
    '''
    date, time = re.split('[/]', time_str)
    time_dt64 = np.datetime64(f'{date}T{time}')

    return time_dt64

# function to download and read PSP data
def get_PSP_data(start_time, end_time, data_products,
                 datatype='psp_fld_l2_mag_RTN_4_Sa_per_Cyc',
                 cdf_files_dir=None,
                 file_prefix='psp_fld_l2_mag_RTN_4_Sa_per_Cyc',
                 file_suffix='v02'):
    '''
    Function to download the specified data products from PSP
    between the given time intervals

    Parameters:
    -----------
    start_time : string in 'yyyy-mm-dd/hh:mm:ss' format
                 Starting time of the queried interval.

    end_time : string in 'yyyy-mm-dd/hh:mm:ss' format
               Ending time of the queried interval.

    data_products : array-like of strings
                    String array of the different keywords for different data products.
                    'B': magnetic fields
    
    cdf_files_dir : string
                    Directory containing the cdf files if we want to read off local files.

    Returns:
    --------
    retrieved_data_products : dictionary
                              Returns a dictionary of the different data products requested.
    '''
    # dictionary to be returned
    retrieved_data_products = {}

    if(cdf_files_dir == None):
        # downloading magnetic field data
        if(np.any(data_products == 'B')):
            # downloading magnetic field from FIELDS
            fields_vars = pyspedas.psp.fields(trange=[start_time, end_time], varnames=['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'],
                                            datatype='mag_RTN_4_Sa_per_Cyc', level='l2', time_clip=True, no_update=True,
                                            username='sbdas', password='SlapHappeeGranpappy02138')
            
            time_fld = pytplot.data_quants['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'].time.data
            BRTN = pytplot.data_quants['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'].data.T

            # saving the magnetic field in RTN format as a (3, Ntimes) array
            retrieved_data_products['time_B'] = time_fld
            retrieved_data_products['B'] = BRTN
    
    else:
        data = misc_FN.read_cdf(start_time, end_time, cdf_files_dir, file_prefix, file_suffix, datatype)

        # saving the magnetic field in RTN format as a (3, Ntimes) array
        retrieved_data_products['time_B'] = data.time
        retrieved_data_products['B'] = data.data.T

    return retrieved_data_products

# function to download and read Wind data 
def get_Wind_data(start_time, end_time, data_products):
    '''
    Function to download the specified data products from PSP
    between the given time intervals

    Parameters:
    -----------
    start_time : string in 'yyyy-mm-dd/hh:mm:ss' format
                 Starting time of the queried interval.

    end_time : string in 'yyyy-mm-dd/hh:mm:ss' format
               Ending time of the queried interval.

    data_products : array-like of strings
                    String array of the different keywords for different data products.
                    'B': magnetic fields

    Returns:
    --------
    retrieved_data_products : dictionary
                              Returns a dictionary of the different data products requested.
    '''
    # dictionary to be returned
    retrieved_data_products = {}

    # downloading magnetic field data
    if(np.any(data_products == 'B')):
        # downloading magnetic field from FIELDS
        fields_vars = pyspedas.psp.fields(trange=[start_time, end_time], varnames=['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'],
                                          datatype='mag_RTN_4_Sa_per_Cyc', level='l2', time_clip=True, no_update=False,
                                          username='sbdas', password='SlapHappeeGranpappy02138')
        
        time_fld = pytplot.data_quants['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'].time.data
        BRTN = pytplot.data_quants['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'].data.T

        # saving the magnetic field in RTN format as a (3, Ntimes) array
        retrieved_data_products['time_B'] = time_fld
        retrieved_data_products['B'] = BRTN

    return retrieved_data_products


# function to download and read Stereo-A data
def get_StereoA_data(start_time, end_time, data_products):
    '''
    Function to download the specified data products from PSP
    between the given time intervals

    Parameters:
    -----------
    start_time : string in 'yyyy-mm-dd/hh:mm:ss' format
                 Starting time of the queried interval.

    end_time : string in 'yyyy-mm-dd/hh:mm:ss' format
               Ending time of the queried interval.

    data_products : array-like of strings
                    String array of the different keywords for different data products.
                    'B': magnetic fields

    Returns:
    --------
    retrieved_data_products : dictionary
                              Returns a dictionary of the different data products requested.
    '''
    # dictionary to be returned
    retrieved_data_products = {}

    # downloading magnetic field data
    if(np.any(data_products == 'B')):
        # downloading magnetic field from magnetometer (MAG) onboard Stereo-A
        mag_vars = pyspedas.stereo.mag(trange=[start_time, end_time], probe='a', time_clip=True, no_update=True)
        
        time_stereo = pytplot.data_quants['BFIELD'].time
        BRTN = pytplot.data_quants['BFIELD'].data.T[:3]

        # saving the magnetic field in RTN format as a (3, Ntimes) array
        retrieved_data_products['time_B'] = time_stereo
        retrieved_data_products['B'] = BRTN

    return retrieved_data_products