# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 11:27:24 2023

@author: HuangAlan
"""

# %% package for exe
if __name__=='__main__':
    import sys
    from time import time
    import function_gen_topo

    T = time()
    path_file = sys.argv[1]
    _arg1 = sys.argv[2] if len(sys.argv) >= 3 else 1e3
    _arg2 = sys.argv[3] if len(sys.argv) >= 4 else 300
    _arg3 = sys.argv[4] if len(sys.argv) >= 5 else 10
    _arg4 = sys.argv[5] if len(sys.argv) >= 6 else 0.5

    message = function_gen_topo.gen_bp_avg(path_file,
                                           UNIT_V=_arg1, LEN_DATA_S=_arg2, 
                                           LEN_EPOCH_S=_arg3, BASELINE_S=_arg4)
    print(message)
    print(f'consumed time: {time()-T :.2f}')
