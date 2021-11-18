"""
Python 3.7 wird benötigt um die MatLabEngine installieren zu können
und eine aktuelle Version von MatLab muss auf dem Rechner installiert sein.
(https://de.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
dann im terminal:
cd matlabroot/extern/engines/python
python setup.py install
My Path: /usr/local/MATLAB/R2021a/extern/engines/python
next
"""

import matlab.engine # funktioniert nur mit python 3.7
import numpy as np
import scipy.io
import os
import h5py
#d

spike_list = np.zeros(0)
amp = np.zeros(0)
rec_dur = 0
SaRa = 0

def import_mat(path):
    global spike_list
    global amp
    global rec_dur
    global SaRa
    try:
        mat_data = scipy.io.loadmat(path)

    except:
        mat_data = h5py.File(path, 'r')
    try:
        spike_list = np.transpose(mat_data["SPIKEZ"]["TS"][0, 0])
        spike_list = np.where(np.invert(np.isnan(spike_list)), spike_list, 0)
        amp = np.zeros([spike_list.shape[1], spike_list.shape[0]])
        rec_dur = float(mat_data["SPIKEZ"][0, 0]["PREF"][0, 0]["rec_dur"][0])
        SaRa = mat_data["SPIKEZ"][0, 0]["PREF"][0, 0]["SaRa"][0][0]
        flag_mat_v1 = True
        print("Mat Datei erfolgreich importiert")
    except:
        try:
            spike_list = np.transpose(mat_data["temp"]["SPIKEZ"][0, 0]["TS"][0, 0])
            amp = mat_data["temp"]["SPIKEZ"][0, 0]["AMP"][0, 0]
            rec_dur = mat_data["temp"]["SPIKEZ"][0, 0]["PREF"][0,0]["rec_dur"][0, 0][0][0]
            SaRa = mat_data["temp"]["SPIKEZ"][0, 0]["PREF"][0, 0]["SaRa"][0, 0][0][0]
            flat_mat_v2 = True
            print("Mat Datei erfolgreich importiert")
        except:
            print("Mat Datei konnte nicht importiert werden")
    # return spike_list, amp, rec_dur, SaRa


def matlab_calc_all_feature(drcell_path, spike_list, amp, rec_dur, SaRa):

    for i in matlab_feautre_list:
        feature_value = matlab_all_feature(drcell_path=drcell_path, TS=spike_list, AMP=amp, rec_dur=rec_dur, SaRa=SaRa,
                                           Selection=i, time_win=rec_dur, FR_min=0)
        feature_mean = feature_value[0]
        feature_values = feature_value[1]
        feature_std = feature_value[2]
        feature_allEl = feature_value[3]


def matlab_all_feature(drcell_path, TS, AMP, rec_dur, SaRa, Selection, time_win, FR_min, N=0, binSize=0):
    TS = np.transpose(TS)
    TS = matlab.double(TS.tolist())
    AMP = matlab.double(AMP.tolist())
    """path = os.getcwd()
    print(path)
    path = os.path.dirname(os.path.dirname(path))
    print(path)
    path = path + "/DrCell"""
    path = drcell_path + "/shared/Engines/Python"
    eng = matlab.engine.start_matlab()  # MatLab Umgebung aufrufen
    eng.cd(path)  # nach Spike-Contrast navigieren
    # eng.get_path(path_manuell, nargout=0)
    # eng.cd(path)  # nach Spike-Contrast navigieren
    values = eng.adapter_python(drcell_path, TS, AMP, float(rec_dur), float(SaRa), Selection, float(time_win), float(FR_min), float(0), float(0))
    eng.quit()
    return values
    # eng.adapter(TS, AMP, rec_dur, SaRa, Selection, time_win, FR_min, N, binSize)

matlab_feautre_list = ['Spikerate',
'Number of spikes',
'Amplitude',
'ActiveElectrodes',
'BR_baker100',
'BD_baker100',
'SIB_baker100',
'IBI_baker100',
'BR_baker200',
'BD_baker200',
'SIB_baker200',
'IBI_baker200',
'BR_selinger',
'BD_selinger',
'SIB_selinger',
'IBI_selinger',
'NBR_chiappalone',
'NBD_chiappalone',
'SINB_chiappalone',
'INBI_chiappalone',
'NBR_jimbo',
'NBD_jimbo'
'SINB_jimbo',
'INBI_jimbo',
'NBR_MC',
'NBD_MC',
'SINB_MC',
'INBI_MC',
'Sync_CC_selinger',
'Sync_STTC',
'Sync_MI1',
'Sync_MI2',
'Sync_PS',
'Sync_PS_M',
'Sync_Contrast',
'Sync_Contrast_fixed',
'Sync_ISIDistance',
'Sync_SpikeDistance',
'Sync_SpikeSynchronization',
'Sync_ASpikeSynchronization',
'Sync_AISIDistance',
'Sync_ASpikeDistance',
'Sync_RISpikeDistance',
'Sync_RIASpikeDistance',
'Sync_EarthMoversDistance',
'Connectivity_TSPE',
'Connectivity_TSPE_70percent',
'Connectivity_TSPE_withSurrogateThreshold',
'Entropy_bin100',
'Entropy_capurro']



path = "/media/broxy/Seagate Expansion Drive/BackUp/HDD/FauBox/Uni/Master/PyCharm/MatLab_adapter/000_TS.mat"
drcell_path = "/mnt/38DA-A148/FauBox/Uni/Master/MatLab/DrCell"

# print(files)
import_mat(path)

values = matlab_all_feature(drcell_path, spike_list, amp, rec_dur, SaRa, Selection='Connectivity_TSPE', time_win=rec_dur, FR_min=0)
auto = matlab_calc_all_feature(drcell_path, spike_list, amp, rec_dur, SaRa)
print(auto)
print(values)