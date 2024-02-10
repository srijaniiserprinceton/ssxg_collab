import numpy as np
import dtw
import sys

import read_satellite_data as load_data
import plot_functions as plot_FN

def dtw_Bvectors(Bdict_sat1, Bdict_sat2, downsampling_factors=[100, 1000]):
    '''
    Calculating the dtw between the different corresponding vector components across 
    two satellite measurements.

    Parameters:
    -----------
    Bdict_sat1 : dictionary
                 Dictionary containing the B-field vector and the time attributes from satellite 1.

    Bdict_sat2 : dictionary
                 Dictionary containing the B-field vector and the time attributes from satellite 2.

    Returns:
    --------
    '''
    # dictionary to store the alignment results of the three dtw
    alignment_dict = {}

    # looping over the three components
    for i in range(3):
        B1 = Bdict_sat1['B'][i,::downsampling_factors[0]]
        B2 = Bdict_sat2['B'][i,::downsampling_factors[1]]
        alignment_dict[i] = dtw.dtw(B1, B2, keep_internals=True)

    return alignment_dict


if __name__=='__main__':
    # the starting and ending times of interest for different satellites
    tstart_psp = '2023-09-22/14:00:00'
    tend_psp = '2023-09-23/10:00:00'

    tstart_wind = '2023-09-22/14:00:00'
    tend_wind = '2023-09-23/10:00:00'

    tstart_stereo = '2023-09-23/12:00:00'
    tend_stereo = '2023-09-26/12:00:00'

    # the data products of interest
    # 'B': magnetic field
    data_products = np.array(['B'])

    # loading PSP data
    PSP_data_dict = load_data.get_PSP_data(tstart_psp, tend_psp, data_products, cdf_files_dir='fc_psp_data')

    # loading Wind data

    
    # loading Stereo-A data
    StereoA_data_dict = load_data.get_StereoA_data(tstart_stereo, tend_stereo, data_products)
    
    # plotting the different retrieved fields to check
    plot_FN.plot_Bfields_allsat(psp=PSP_data_dict, wind=StereoA_data_dict, stereoA=StereoA_data_dict)

    # calculating the alignments using dtw
    alignment_dict_stereo_stereo = dtw_Bvectors(PSP_data_dict, StereoA_data_dict, downsampling_factors=[100, 1000])

    for key in alignment_dict_stereo_stereo.keys():
        alignment_dict_stereo_stereo[key].plot(type="threeway", xlab='PSP', ylab='Stereo-A')
