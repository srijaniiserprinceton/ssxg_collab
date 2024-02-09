import numpy as np
import matplotlib.pyplot as plt
plt.ion()

def plot_Bfields_allsat(**B_data_allsat):
    '''
    Function to plot the magnetic fields corresponding to each satellite.

    Parameters:
    -----------
    B_data_allsat : List of dictionaries to be unpacked before plotting.
                    A list of BRTN dictionaries from all the different satellites used.
    '''

    # the number of satellites
    Nsat = len(B_data_allsat.keys())

    fig, ax = plt.subplots(Nsat, 1, figsize=(9.5, 8))

    print(B_data_allsat)

    # looping over subplots
    for i, key in enumerate(B_data_allsat.keys()):
        B_sat = B_data_allsat[key]['B']
        t_sat = B_data_allsat[key]['time_B']
        ax[i].plot(t_sat, B_sat[0], label='BR')
        ax[i].plot(t_sat, B_sat[1], label='BT')
        ax[i].plot(t_sat, B_sat[2], label='BN')
        ax[i].plot(t_sat, np.linalg.norm(B_sat, axis=0), 'k', label='B')
        ax[i].legend(loc="upper right")

    plt.subplots_adjust(wspace=0.1, hspace=0.1, left=0.1, right=0.98, top=0.98, bottom=0.1)