'''
@Author: AllanXu
@Date: 2020-04-17 13:47:39
@Description: Pyserial for Hardware devices
'''

import serial.tools.list_ports 

plist = list(serial.tools.list_ports.comports())

if len(plist) <= 0:
    print("没有发现端口!")
else:
    #端口数
    print(len(plist))

    plist_0 = list(plist[1])
    serialName = plist_0[0]
    print(serialName)

    serialFd = serial.Serial(serialName, 9600, timeout=60)
    print(serialFd.name)