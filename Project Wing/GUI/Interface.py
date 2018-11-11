'''      
Authors:    Kloni Maluleke (Msc), kloniphani@gmail.com
Date:       January 23, 2018
Copyrights:  2017 ISAT, Department of Computer Science
            University of the Western Cape, Bellville, ZA
'''

from tkinter import *
from threading import Thread
from time import sleep

class Interface(Frame):
	"""description of class"""

	def __init__(self, Master = None, Title = None):
		if Master is not None:
			super().__init__(Master)
		else:
			self.Root = Tk()
			super().__init__(self.Root)

		if Title is not None:
			self.master.title(Title)

		self.OutputConsoleWidget()

		self.pack()
		self.MainLoop()

	def MainLoop(self):
		self.Root.mainloop()

	def OutputConsoleWidget(self, Height = 400, Width = 800):
		self.Height = Height; self.Width = Width
		self.master.geometry('{}x{}'.format(self.Width, self.Height))

		self.DATAQUEUE = [] #Infomartion waiting to be printed on the interface

		self.Text = Text(self.master)
		self.Scrollbar = Scrollbar(self.master)

		self.Text.focus_set()
		self.Text.pack(side = LEFT, fill = 'both', expand = True)
		self.Scrollbar.pack(side = RIGHT, fill = Y)

		self.Text.config(yscrollcommand  = self.Text.yview)
		self.Scrollbar.config(command = self.Scrollbar.set)

		T = Thread(target = self.AutoRefresh, args=())
		T.start()

	def UpdateTextView(self):
		for data in self.DATAQUEUE:
			self.Text.insert(END, data)
		self.DATAQUEUE = []

	def Insert(self, Message):
		if 'DATAQUEUE' in globals():
			self.DATAQUEUE.append(Message)
			return True
		return False

	def Show(self, Message):
		self.Text.insert(END, data)

	def AutoRefresh(self):
		while True:
			self.UpdateTextView()
			sleep(0.5)
