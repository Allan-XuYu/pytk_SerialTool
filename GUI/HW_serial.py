'''
@Author: AllanXu
@Date: 2020-04-17 13:47:39
@Description: Pyserial for Hardware devices

'''

import serial
import serial.tools.list_ports

class SerialCheck:
    def __init__(self):
        self.ports = serial.tools.list_ports.comports() # pyserial tools module
        self.portsNum = len(self.ports)

    def Get_PortNum(self):
        if self.ports == [] :  # No ports were detected
            return 'NoPorts'
        return (self.portsNum)

    def Get_PortName(self,index=1): # index for the selection among mutil-ports 
        if index > self.portsNum:
            return 'over error'
        port_info = list(self.ports[index-1]) # list first element start at 0
        return (port_info[0]) # [name,type,ID]
 
    def Get_PortNameList(self):
        if self.ports == [] :  # No ports were detected
            return 'NoPorts'
        portNameList = []
        n = 1
        while n <= self.portsNum:
            portNameList.append(self.Get_PortName(n))
            n=n+1
        return portNameList
    
class SerialOperation(serial.Serial):
        pass


if __name__=='__main__':
    Check_Handle = SerialCheck()
    print(Check_Handle.Get_PortNum())
    print(Check_Handle.Get_PortName())
    print(Check_Handle.Get_PortNameList())
    ser= SerialOperation(Check_Handle.Get_PortName(),115200,timeout=0)

    while 1:
        if ser.in_waiting > 0 :
            read_data=ser.read(ser.in_waiting)
            ser.reset_input_buffer()
            print(read_data)   
