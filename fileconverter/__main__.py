#coding: utf-8
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import HORIZONTAL
from tkinter import ttk
from tkinter import filedialog
import threading
import traceback
from enum import Enum
from PIL import Image
import configparser
import os
import Define as d

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # window
        self.geometry("600x300")
        self.title("file converter")
        
        extensionTuple = self.getExtensionTuple()
        
        # canvas, scrollWindow, scrollBar
        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.LEFT, fill="both", expand=True)
        
        # mainFrame: insertTableName, insertRecordLength, exportButton, executeButton
        self.labelFrame = tk.Frame(master=self.frame, width=100)
        self.labelFrame.pack(side=tk.TOP, fill="x")
        self.inputFilePathLabel = tk.Label(master=self.labelFrame, text="file", width=24)
        self.inputFilePathLabel.pack(side=tk.LEFT, padx=10, pady=5)
        self.inputFormatLabel = tk.Label(master=self.labelFrame, text="format", width=20)
        self.inputFormatLabel.pack(side=tk.LEFT, padx=10, pady=5)
        self.inputSizesLabel = tk.Label(master=self.labelFrame, text="sizes", width=20)
        self.inputSizesLabel.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.mainFrame = tk.Frame(master=self.frame, width=100)
        self.mainFrame.pack(side=tk.TOP, fill="x")
        self.filepath = tk.StringVar()
        self.inputFilePathEntry = tk.Entry(master=self.mainFrame, textvariable=self.filepath, width=20)
        self.inputFilePathEntry.pack(side=tk.LEFT, padx=5, pady=5)
        self.referButton = ttk.Button(master=self.mainFrame, text=u'reffer', command=self.clickRefferButton)
        self.referButton.pack(side=tk.LEFT, padx=0, pady=5)
        self.inputFormatNameCombobox = ttk.Combobox(self.mainFrame, textvariable=tk.StringVar(), values=extensionTuple, style="office.TCombobox", width="20")
        self.inputFormatNameCombobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.inputWidthEntry = tk.Entry(master=self.mainFrame, width=7)
        self.inputWidthEntry.pack(side=tk.LEFT, padx=5, pady=5)
        self.inputsizesLabel = tk.Label(master=self.mainFrame, text="x", width=1)
        self.inputsizesLabel.pack(side=tk.LEFT, padx=0, pady=5)
        self.inputHeightEntry = tk.Entry(master=self.mainFrame, width=7)
        self.inputHeightEntry.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.executeButton = tk.Button(
            master=self.mainFrame,
            text="Execute",
            command=lambda:self.startThread(self.excuteFileConvert)
        )
        self.executeButton.pack(side=tk.LEFT, padx=15, pady=5)
        
        self.pb = ttk.Progressbar(
            self.mainFrame,
            orient=HORIZONTAL,
            maximum=10,
            value=0,
            length=200,
            mode="indeterminate"
        )

    def getExtensionTuple(self):
        if not os.path.exists(d.settingDefine.FILE_PATH.value):
            raise FileNotFoundError(d.settingDefine.FILE_PATH.value + " is not exist")
        config = configparser.ConfigParser()
        config.read(d.settingDefine.FILE_PATH.value)
        return tuple(json.loads(config[d.settingDefine.SETTING.value][d.settingDefine.EXTENSION_LIST.value]))
    
    def getFormat(self, extensionName):
        if not os.path.exists(d.settingDefine.FILE_PATH.value):
            raise FileNotFoundError(d.settingDefine.FILE_PATH.value + " is not exist")
        config = configparser.ConfigParser()
        config.read(d.settingDefine.FILE_PATH.value)
        type = config[extensionName][d.settingDefine.TYPE.value]
        extension = config[extensionName][d.settingDefine.EXTENSION.value]
        return [(type, extension)]
    
    def clickRefferButton(self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        self.filepath.set(filepath)
        
    def showAlertMessageBox(self, title, message):
        messagebox.showerror(title, message)

    def startThread(self, targetFunc):
        t = threading.Thread(target=targetFunc) 
        t.start() 
        
    # excute
    def excuteFileConvert(self):
        self.pb.pack(side=tk.LEFT)
        self.pb.start()
        try:
            self.fileConvert()
        except Exception as e:
            self.showAlertMessageBox(e.__class__.__name__, traceback.format_exc())
            
        self.pb.stop()
        self.pb.pack_forget()
        
    def fileConvert(self):
        inputFilePath = self.inputFilePathEntry.get()
        formatName = self.inputFormatNameCombobox.get() # file extension
        width = int(self.inputWidthEntry.get()) # [(width, height)])
        height = int(self.inputHeightEntry.get())
        sizes = [(width, height)]
        formatList = self.getFormat(formatName) # length = 1
        outputFilepath = filedialog.asksaveasfilename(filetypes=formatList, defaultextension="*" + formatList[0][1])
        img = Image.open(inputFilePath)
        img.save(outputFilepath, format=formatList[0][0], sizes=sizes)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()