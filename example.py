#!/usr/bin/kivy

from os.path import dirname, join
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'system')
Config.set('input', 'mouse', 'mouse, disable_multitouch')


###############################################################################
# Screen file
###############################################################################

from kivy.core.window import Window
from Datagrid import DataGrid
from kivy.graphics import Color

class DataGridScreen(Screen):
	def __init__(self):
		super(DataGridScreen, self).__init__()
		self.grid = DataGrid()
		self.grid.setupGrid([{'text':"Header 1", 'type':'BorderLabel', 'width': 100}, 
			{'text':"Header 2", 'type':'BorderLabel', 'width': 100},
			{'text':"Header 3", 'type':'BorderLabel', 'width': 100}, 
			{'text':"Header 4", 'type':'BorderLabel', 'width': 100}, 
			{'text':"Header 5", 'type':'Label', 'width': 100}, 
			{'text':"Header 6", 'type':'Label', 'width': 100}, 
			{'text':"Header 7", 'type':'Label', 'width': 100}, 
			{'text':"Header 8", 'type':'Label', 'width': 100}], Window.width, 46)
		self.add_widget(self.grid)

		# add test data
		for index in range(0,20):
			tempData = [{'text':'Item ' + str(index), 'type':'Label'}, 
			{'text':'Item Item Item Item Item Item  ' + str(index), 'type':'Label'}, 
			{'text':'Item ' + str(index), 'type':'BorderLabel'}, 
			{'text':'Item ' + str(index), 'type':'BorderLabel'}, 
			{'text':'Item ' + str(index), 'type':'BorderLabel'}, 
			{'text':'Item ' + str(index), 'type':'Label'}, 
			{'text':'Item ' + str(index), 'type':'Label'}, 
			{'text':'Item ' + str(index), 'type':'BorderButton'}]

			self.grid.addRow(tempData)

		self.grid.changeRowColor(10, Color(1.,0,0,1))
		self.grid.changeRowColor(16, Color(1.,0,0,1))
		self.grid.changeRowColor(12, Color(0.91764705882352941176470588235294, 0.01960784313725490196078431372549, 0.02352941176470588235294117647059, 1))
		#--- test change value of cell
		self.grid.changeCellValueAtRow(3, 0, 'AAAAAAA')
		self.grid.changeCellValueAtRow(3, 5, 'AAAAAAA')
		self.grid.changeCellValueAtRow(7, 0, 'AAAAAAA')

		#--- test insert row at index
		tempData = [{'text':'Item X', 'type':'Label'}, 
			{'text':'Item X', 'type':'Label'}, 
			{'text':'Item X', 'type':'Label'}, 
			{'text':'Item X', 'type':'Label'}, 
			{'text':'Item X', 'type':'Label'}, 
			{'text':'Item X', 'type':'Label'}, 
			{'text':'Item X', 'type':'Label'}, 
			{'text':'Item X', 'type':'Button'}]
		self.grid.addRow(tempData, type='insert', index=0)

		tempData = [{'text':'Item Y', 'type':'Label'}, 
			{'text':'Item Y', 'type':'Label'}, 
			{'text':'Item Y', 'type':'Label'}, 
			{'text':'Item Y', 'type':'Label'}, 
			{'text':'Item Y', 'type':'Label'}, 
			{'text':'Item Y', 'type':'Label'}, 
			{'text':'Item Y', 'type':'Label'}, 
			{'text':'Item Y', 'type':'Button'}]
		self.grid.addRow(tempData, type='insert', index=30)

		tempData = [{'text':'Item Z', 'type':'Label'}, 
			{'text':'Item Z', 'type':'Label'}, 
			{'text':'Item Z', 'type':'Label'}, 
			{'text':'Item Z', 'type':'Label'}, 
			{'text':'Item Z', 'type':'Label'}, 
			{'text':'Item Z', 'type':'Label'}, 
			{'text':'Item Z', 'type':'Label'}, 
			{'text':'Item Z', 'type':'Button'}]
		self.grid.addRow(tempData, type='first')
		#---------------------------------
		self.grid.removeRowAtIndex(3)
		self.grid.removeRowAtIndex(5)
		self.grid.removeRowAtIndex(7)

###############################################################################
# Main file
###############################################################################

class Example(App):
	def __init__(self):
		super(Example, self).__init__()

	def build(self):
		self.title = 'Example'
		self.pos = (0, 0)
		self.currentDir = dirname(__file__)
		self.sm = ScreenManager()
		self.screens = {}

		test = DataGridScreen()
		self.sm.switch_to(test)
		
		return self.sm

if __name__ == '__main__':
	Example().run()
	
