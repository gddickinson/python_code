import os
import sys
import win32com.client


def run_macro(pathName,macroName):
    print('macro-running')
    print(pathName)

    #this part runs the macro from excel
    if os.path.exists(pathName):
        xl=win32com.client.Dispatch("Excel.Application")
        #xl.Visible = 1
        xl.Workbooks.Open(Filename=pathName, ReadOnly=1)
        xl.Application.Run(macroName)
        xl.Save()
        xl.Application.Quit() # Comment this out if your excel script closes
        del xl

    print('File refreshed!')

pathName = r"C:\Google Drive\SiCr_Digitization\scripts\test2.xlsm"
macroName = "Sheet1.CommandButton1_Click"

run_macro(pathName,macroName)