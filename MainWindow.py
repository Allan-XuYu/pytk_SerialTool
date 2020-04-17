'''
@Author: AllanXu
@Date: 2020-04-12 21:30:50
@Description: MainWindows
'''
from tkinter import *

class Main_Windows(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello,World')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit',command=self.quit)
        self.quitButton.pack()

app = Main_Windows()
app.master.title('Hello World')
app.mainloop()