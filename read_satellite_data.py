import numpy as np
import pyspedas
import pytplot

# function to download and read PSP data
def get_PSP_data(start_time, end_time, data_products):
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
                                          datatype='mag_RTN_4_Sa_per_Cyc', level='l2', time_clip=True, no_update=True,
                                          username='sbdas', password='SlapHappeeGranpappy02138')
        
        time_fld = pytplot.data_quants['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'].time.data
        BRTN = pytplot.data_quants['psp_fld_l2_mag_RTN_4_Sa_per_Cyc'].data.T

        # saving the magnetic field in RTN format as a (3, Ntimes) array
        retrieved_data_products['time_B'] = time_fld
        retrieved_data_products['B'] = BRTN

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
        mag_vars = pyspedas.stereo.mag(trange=[start_time, end_time], probe='a', time_clip=True, no_update=False)
        
        time_stereo = pytplot.data_quants['BFIELD'].time
        BRTN = pytplot.data_quants['BFIELD'].data.T[:3]

        # saving the magnetic field in RTN format as a (3, Ntimes) array
        retrieved_data_products['time_B'] = time_stereo
        retrieved_data_products['B'] = BRTN

    return retrieved_data_products