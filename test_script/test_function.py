# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 18:03:28 2023

@author: HuangAlan
"""
import os
import function_gen_topo

path_cwd = os.path.abspath(os.getcwd())
path_file = os.path.join(path_cwd, 'test_data', 'lefthand_1201.cnt')
path_save = os.path.join(path_cwd, 'test_data', 'plot_result')

# ----- call -----
message = function_gen_topo.gen_bp_avg(path_file, path_save=path_save,
                                       UNIT_V=1e3, LEN_DATA_S=300, LEN_EPOCH_S=10, BASELINE_S=0.5,
                                       BP_BAND={'Delta': (0.5, 4), 'Theta': (4, 8), 'Alpha': (8, 12), 
                                                'Beta': (12, 30), 'Gamma': (30, 45)})