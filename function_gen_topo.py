# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 14:55:47 2023

@author: HuangAlan
"""
__version__='0.1.0'

# %% inner def: filter 
def hnc_filter(data, Fs):
    from scipy import signal 
    
    cutoff_low=59.5
    cutoff_high=60.5
    passband = [(cutoff_low*2)/Fs,(cutoff_high*2)/Fs]
    b,a = signal.butter(5, passband, 'bandstop',analog=False)
    data_stop = signal.lfilter(b, a, data)
    
    cutoff=0.5
    b,a = signal.butter(3, ((cutoff*2)/Fs), 'high',analog=False)
    data_high = signal.lfilter(b, a, data_stop)
    
    cutoff=60
    b,a = signal.butter(3, ((cutoff*2)/Fs), 'low',analog=False)
    data_low = signal.lfilter(b, a, data_high)
    
    return data_low

# %% inner def: function_BP
def cal_bp(data, band_start, band_end, fs=500):
    import numpy as np
    import numpy.fft as npfft
    
    # ----- initial parameter -----
    if data.ndim == 1:
        data = data.reshape(1, -1)
    [num_ch, num_dp] = data.shape
    num_time = num_dp/fs
    
    # ----- Fourier transform -----
    data_fft = npfft.fft(data, axis=1)
    data_psd = np.square(np.abs(data_fft))
    value_bp = np.sum(
        data_psd[:,int(np.round((band_start*num_time))):int(np.round((band_end*num_time)))], axis=1)
    
    return value_bp

# %% inner def: plot topo
def plot_topo(bp_avg, eeg_fs, path_save):
    import mne
    import numpy as np
    from matplotlib import pyplot as plt
    from mne.channels.layout import _auto_topomap_coords
    
    # ----- model bp -----
    ch_sel = bp_avg.index.to_list()
    band_sel = [i.split('_')[0] for i in bp_avg.columns]
    
    # ----- set mne parameter -----
    mne_ch_sel = [i.title() for i in ch_sel]
    m =  mne.channels.make_standard_montage('standard_1020')
    info = mne.create_info(mne_ch_sel, eeg_fs, ch_types="eeg")
    channel = dict(marker='o', markerfacecolor='k', markeredgecolor='w', 
                   linewidth=0, markersize=8)
    visual = np.any([np.ones([len(ch_sel),1]) == 1], axis=0)
    
    # ----- topo plot -----
    for i_band in range(len(band_sel)):
        tmp = bp_avg[band_sel[i_band]].values
        bp_plot = (tmp-np.mean(tmp))/np.std(tmp)
        
        # ----- create mne data -----
        topodata = mne.EvokedArray(bp_plot.reshape(len(bp_plot),1), info)
        topodata.set_montage(m)
        
        # ----- reset ch location -----
        ch_axes = _auto_topomap_coords(topodata.info, picks=None, 
                                       ignore_overlap=False, to_sphere=True, 
                                       sphere='auto')
        ch_axes = ch_axes-np.mean(ch_axes,0)
        ch_axes[:,1] -= 0.005
        ch_axes[:,0] += 0.001
        ch_axes = np.round(ch_axes, 3)*0.75
        
        # ----- plot -----
        image, _ = mne.viz.plot_topomap(topodata.data[:,0], ch_axes, contours=0, res=256, 
                                        cmap='RdBu_r', mask=visual, mask_params=channel, 
                                        show=False, size=5)
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1)
        plt.colorbar(image, shrink=0.8, pad=0)
        plt.savefig(path_save+f'/topomap_{band_sel[i_band]}.png', transparent=True)

# %% main def
def gen_bp_avg(path_file, UNIT_V=1e3, LEN_DATA_S=300, LEN_EPOCH_S=10, BASELINE_S=0.5,
               BP_BAND={'Delta': (0.5, 4), 'Theta': (4, 8), 'Alpha': (8, 12), 
                        'Beta': (12, 30), 'Gamma': (30, 45)}):
    import os
    import mne
    import numpy as np
    import pandas as pd
    SUPPORT_FS = [1000, 500, 250, 512, 256]
    
    # ----- decode file -----
    try:
        raw_cnt = mne.io.read_raw_cnt(path_file, preload=True, verbose=50,
                                      data_format='int32')
    except:
        message = "error, fail in mne.io.read_raw_cnt, please check file format."
        return message
    
    try:
        eeg_fs = int(raw_cnt.info['sfreq'])
        eeg_ch = raw_cnt.ch_names
        eeg_data = raw_cnt.get_data()
        if np.shape(eeg_data)[1] < 180*eeg_fs:
            message = "error, EEG data must longer than 3 mins"
            return message
        else:
            if eeg_fs in SUPPORT_FS:
                message = "success, the cnt file is decoded."
            else:
                message = "error, the sampling rate is supported {SUPPORT_FS} Hz only. the sampling rate of input file is {eeg_fs} Hz."
    except KeyError: 
        message = "error, the cnt file lost information of ['sfreq']."
        return message
    except AttributeError:
        message = "error, the cnt file lost Attribute [ch_names]."
        return message

    # ----- select 19 ch and change unit to mV -----
    ch_sel = ['FP1','FP2','F7','F3','FZ','F4','F8','T3','C3','CZ','C4','T4',
              'T5','P3','PZ','P4','T6','O1','O2']
    ch_ide_sel = [eeg_ch.index(i_ch) for i_ch in ch_sel]
    if len(ch_ide_sel) < len(ch_sel):
        message = "error, the channel is less than 20, please check cnt file."
        return message
    data_raw = eeg_data[ch_ide_sel, :]*UNIT_V
        
    # ----- baseline 0.5sec -----
    _data_pt = LEN_DATA_S*eeg_fs
    if np.shape(data_raw)[1] < _data_pt:
        message = "error, EEG data must less than input mins, please check."
        return message

    _baseline_pt = int(np.shape(data_raw)[1]%(_data_pt))
    if _baseline_pt > int(BASELINE_S*eeg_fs):
        _baseline_pt = int(BASELINE_S*eeg_fs)
    else:
        message = "warning, the baseline data point is less than {int(BASELINE_S*eeg_fs)}"

    data_bsl = data_raw[:, :_baseline_pt].mean(axis=1).reshape(-1,1)
    data_crct = data_raw[:, _baseline_pt:] - data_bsl
    data_crct = data_crct[:, :LEN_DATA_S*eeg_fs]
    
    # ---- filter -----
    data_filter = hnc_filter(data_crct, eeg_fs)
    
    # ----- cut epoch -----
    _epoch_pt = LEN_EPOCH_S*eeg_fs
    epoch_data = []
    for i_tri in range(int(_data_pt/_epoch_pt)):
        epoch_data.append(data_filter[:, i_tri*_epoch_pt:(i_tri+1)*_epoch_pt])
    epoch_data = np.array(epoch_data)
    
    # ----- get log bp -----
    bp_avg = pd.DataFrame([])
    for i_band in BP_BAND:
        bp_value = []
        for i_data in epoch_data:
            bp_value.append(cal_bp(i_data, BP_BAND[i_band][0], 
                                   BP_BAND[i_band][1], 
                                   fs=eeg_fs))
        _tmp_bp = pd.Series(np.array(np.log(bp_value)).mean(axis=0))
        _tmp_bp.index = ch_sel
        bp_avg[i_band] = _tmp_bp
    
    # ----- generate report elements -----
    path_save = os.path.join("/".join(path_file.split("/")[:-1]), 'topo_plot')
    os.makedirs(path_save, exist_ok=True)
    plot_topo(bp_avg, eeg_fs, path_save)
    message = f'success, the report elements in generated in {path_save}.'

    return message
