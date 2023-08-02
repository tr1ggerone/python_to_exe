## python_to_exe
- 將 python script 生成exe檔，以下討論兩種不同的生成結果
- 使用到的 python 檔中使用的 package 請見檔案中的`requirements_v010.txt`

## 生成流程
- 前置作業: 
	- 生成的python檔，需要加入 `if __name__=='__main__':` 才可以執行，其中參數的傳入需要使用sys.argv(請見**exe_for_cmd.py**)
		- sys.argv is a Python code that accesses the command-line arguments passed to a script
		- 當您從命令列執行 Python 腳本時，可以在腳本名稱後面提供額外的參數。這些參數會以空格分隔，並存儲在 sys.argv 的列表中。其中，sys.argv[0] 會保存腳本本身的名稱，而後續元素 sys.argv[1]、sys.argv[2]，以此類推，則存儲了從命令列傳遞的其他參數。
	- 也可利用 Tkinter 做成介面的樣式在生成(請見**exe_for_tkinter.py**)

- Auto Py to Exe 參數說明
	- Script Location: 選擇要生成的python檔 (如: exe_for_cmd.py 或是 exe_for_tkinter.py)
    - Onefile: onedir 與 onefile 的差異是在打包成 exe 時，其結果為一個資料夾或是一個執行檔。onedir 的檔案大小相對較大，但是在建置環境的速度較快且會將程序引用的文件放到一個文件夾下，不需額外定義夾帶檔案的路徑參數。
    - Addition Files 則是添加生成 exe 所需的附屬文件
		- 若在執行exe時發現缺少了某個套件，需選擇 Add Folder 將其加入。由於在打包的過程，mne 套件無法順利被加入，因此需手動將 mne 的資料夾添加進去
		- 若程式有讀取某些特定檔案，需選擇 Add Files 將其加入(如.pkl, .csv ...)，並更改python中的檔案路徑。詳細說明請見 **Reference的第三點**，修改路徑的def則如下所示:
		```python
		def resource_path(file_path):
			import os
			import sys
			try:
    				base_path = sys._MEIPASS
				print(base_path)
			except Exception:
				base_path = os.path.abspath(".")

			return os.path.join(base_path, file_path)
		```
	- Settings: Output Directory則是設定 exe 檔生成的位置
	- 以上參數都設定好便可以按下 **CONVERT .PY TO .EXE** 進行轉換

## Reference: 
- [How to convert .py to .exe? Step by step guide.](https://proxlight.medium.com/how-to-convert-py-to-exe-step-by-step-guide-82e9e9a8984a)
- [Auto Py to Exe Github](https://github.com/brentvollebregt/auto-py-to-exe)
- [夾帶檔案的exe生成方式 - onefile](https://zhuanlan.zhihu.com/p/130328237)

## 備註
- test_data中的資料為壓縮檔，記得解壓縮後再使用
- 以下為 exe_for_tkinter.exe 的開啟方式:
  ```
  1. 開啟cmd
  2. cd 至 exe 的位址資料夾
  3. exe_for_tkinter.exe
  ```
- 以下為 exe_for_cmd.exe 的開啟方式:
  ```
  1. 開啟cmd
  2. cd 至 exe 的位址資料夾
  3. exe_for_cmd.exe 測試資料完整路徑("C:/Users/XXXX/Desktop/my_github/python_to_exe/test_data/lefthand_1201.cnt")
  ```
