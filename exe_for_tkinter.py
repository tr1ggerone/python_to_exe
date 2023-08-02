# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 11:35:14 2023

@author: HuangAlan
"""
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import warnings
warnings.filterwarnings('ignore')
import function_gen_topo as gp

# %% inner def
class PrintLogger(object):  
    def __init__(self, textbox):
        self.textbox = textbox 
    def write(self, text):
        self.textbox.configure(state="normal")  
        self.textbox.insert("end", text) 
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
    def flush(self):
        pass
    
def gen_topo():
    path_file = filedialog.askopenfilename()
    _arg1 = int(cb_ratio.get())
    _arg2 = int(cb_time.get())*60
    _arg3 = int(cb_epoch.get())
    _arg4 = float(cb_base.get())
    message = gp.gen_bp_avg(path_file, UNIT_V=_arg1, LEN_DATA_S=_arg2, LEN_EPOCH_S=_arg3, BASELINE_S=_arg4,
                            BP_BAND={'Delta': (0.5, 4), 'Theta': (4, 8), 'Alpha': (8, 12), 
                                     'Beta': (12, 30), 'Gamma': (30, 45)})
    print(message)
    
# %% initial GUI
if __name__ == '__main__':
    window = tk.Tk()
    window.lift()
    window.title('EEG Topo Software V1.0.0')
    window.geometry('800x200')
    
    # %% place the item
    # ----- initial parameter -----
    LB_W = 16
    CB_W = 8
    FONT = ('Arial', 10)
    initial_x, initial_y = 30, 30
    move_x, move_y = 120, 30
    
    # ----- function -----
    lb_ratio = ttk.Label(window, text='amplifying ratio:', width=LB_W, anchor='e')
    cb_ratio = ttk.Combobox(window, values=[1000], font=FONT, width=CB_W)
    cb_ratio.current(0)
    lb_time = ttk.Label(window, text='data length (min):', width=LB_W, anchor='e')
    cb_time = ttk.Combobox(window, values=[3, 5, 7], font=FONT, width=CB_W)
    cb_time.current(1)
    lb_epoch = ttk.Label(window, text='epoch length (sec):', width=LB_W, anchor='e')
    cb_epoch = ttk.Combobox(window, values=[3, 6, 10, 15], font=FONT, width=CB_W)
    cb_epoch.current(2)
    lb_base = ttk.Label(window, text='baseline len (sec):', width=LB_W, anchor='e')
    cb_base = ttk.Combobox(window, values=[0.5, 1], font=FONT, width=CB_W)
    cb_base.current(0)
    btn = tk.Button(window, text='select cnt file and start plot', command=gen_topo, 
                    width=27)
    log_widget = ScrolledText(window, font=('consolas', 9, 'normal'))
    
    # -----place ---- 
    lb_ratio.place(x=initial_x, y=initial_y)
    cb_ratio.place(x=initial_x+move_x, y=initial_y)
    lb_time.place(x=initial_x, y=initial_y+move_y)
    cb_time.place(x=initial_x+move_x, y=initial_y+move_y)
    lb_epoch.place(x=initial_x, y=initial_y+2*move_y)
    cb_epoch.place(x=initial_x+move_x, y=initial_y+2*move_y)
    lb_base.place(x=initial_x, y=initial_y+3*move_y)
    cb_base.place(x=initial_x+move_x, y=initial_y+3*move_y)
    btn.place(x=initial_x, y=initial_y+4*move_y)
    log_widget.place(x=initial_x+1.8*move_x, y=initial_y, height=150, width=500)
    
    # %% initial log
    logger = PrintLogger(log_widget)
    sys.stdout = logger
    sys.stderr = logger
    window.mainloop()
