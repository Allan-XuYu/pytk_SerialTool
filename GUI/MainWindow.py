'''
@Author: AllanXu
@Date: 2020-04-12 21:30:50
@Description: MainWindows
'''

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
import HW_serial
import threading
import time

class Main_Windows(Frame):
    def __init__(self,master=None): 
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()    
        self.ScT = scrolledtext.ScrolledText(self, width=30, height=10) 
        self.ScT.pack()

    def createWidgets(self):
        self.helloLabel = Label(self, text='AllanXu Serial Tool')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit',command=self.quit)
        self.quitButton.pack()
        self.createPortsBox()

    def createPortsBox(self):
        PortBox = ttk.Combobox(self)
        PortBox.pack()
        # add contents
        CheckHandle = HW_serial.SerialCheck()
        PortBox['value'] = CheckHandle.Get_PortNameList() 
        PortBox.current(0) # default display
    
    def Datashow(self,DisplayString):
        self.ScT.insert(END,DisplayString)
        self.ScT.see(END)  # To see the lastest

# Mutil-Threads
def loopData():
    Check_Handle = HW_serial.SerialCheck()

    ser= HW_serial.SerialOperation(Check_Handle.Get_PortName(),115200,timeout=0)
    while 1:
        if ser.in_waiting > 0 :
            read_data=ser.read(ser.in_waiting)
            ser.reset_input_buffer()
            print(read_data) 
            app.Datashow(read_data)


if __name__=='__main__':
    
    app = Main_Windows()
    app.Datashow('AllanXu Uart Tool\n')
    app.master.title('Serial by Python')

    thread_UartReceive = threading.Thread(target=loopData, name='DataThread')
    thread_UartReceive.start()
 
    app.mainloop() # window loop , must called in the end




