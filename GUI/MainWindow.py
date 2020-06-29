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
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import time
import re

TempNum=[]
temp_Showing=[20,20,20,20,20,20,20,20,20,20]
time_Showing=[0,1,2,3,4,5,6,7,8,9]

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
        self.testbutton = Button(self, text='Test button',command=self.test)
        self.testbutton.pack()
        self.createPortsBox()
        self.axshandle=self.createMatplotlib()

    def test(self):
        TempCurve()
        pass

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
    
    def createMatplotlib(self): 
        fig = plt.figure()  
        axs = plt.subplot()
        axs.set(xlabel='time (s)', ylabel='temperature (℃)',title='Real Time Temp. Value')
        axs.set(xlim=[time_Showing[0]-0.2,time_Showing[9]+0.4],ylim=[-180,180])
        axs.plot(time_Showing,temp_Showing)

        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()  

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()    
        canvas.get_tk_widget().pack()
        return axs

    def Get_axshandle(self):  # offer a interface for external part to operate figure 
        return self.axshandle
       



# Mutil-Threads
def loopData():
    global TempNum
    Check_Handle = HW_serial.SerialCheck()
    if Check_Handle.Get_PortNameList() == 'NoPorts':
        print('UartReceiveThread close because no ports')
        return 
    ser= HW_serial.SerialOperation(Check_Handle.Get_PortName(),115200,timeout=0)
    while 1:
        if ser.in_waiting > 0 :
            #read_data=ser.read(ser.in_waiting)
            read_data=ser.readline()
            ser.reset_input_buffer()
            #print(read_data) 
            #print(read_data.decode('utf-8')) 
            TempNum= [float(s) for s in re.findall(r'.\d+.\d+', read_data.decode('utf-8'))] # data structure type from uart is bytes, has to change to be num/str
            print(TempNum)
            app.Datashow(read_data)

def loopTemp():
    global TempNum
    while True:
        time.sleep(0.5)
        
        for i in range(9):
            temp_Showing[i]= temp_Showing[i+1] 
            time_Showing[i]= time_Showing[i+1]
        
        if len(TempNum) > 0: # prevent error coz list to be empty
            temp_Showing[9] = TempNum[0]
            time_Showing[9]+=1
        

def TempCurve():
    axhandle = app.Get_axshandle()
    plt.ion()
    print(temp_Showing)
            
    plt.cla() # reset figure
    
    axhandle.set(xlabel='time (s)', ylabel='temperature (℃)',title='Temp. Value')
    axhandle.set(xlim=[time_Showing[0]-0.2,time_Showing[9]+0.4],ylim=[-180,180])
    axhandle.plot(time_Showing,temp_Showing)
        
         


if __name__=='__main__':
    
    app = Main_Windows()
    app.Datashow('AllanXu Uart Tool\n')
    app.master.title('Serial by Python')
    

    thread_UartReceive = threading.Thread(target=loopData, name='DataThread')
    thread_UartReceive.daemon=True
    thread_UartReceive.start()

    thread_TempUpdate = threading.Thread(target=loopTemp, name='TempThread')
    #thread_TempUpdate.daemon=True
    thread_TempUpdate.start()


    app.mainloop() # window loop , must called in the end




