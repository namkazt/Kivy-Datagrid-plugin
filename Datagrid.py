import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListView
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle

# class grid row
class DataGridRow(GridLayout):
	def __init__(self, data, **kwargs):
		super(DataGridRow, self).__init__(**kwargs)
		self.index = kwargs.get('index');
		self.cells = []
		for colIndex in range(0, self.cols):
			cell = None
			if data[colIndex]['type'] == 'Lable':
				cell = Label()
			elif data[colIndex]['type'] == 'Button':
				cell = Button()

			cell.text = data[colIndex]['text']
			self.add_widget(cell)
			self.cells.append(cell)

	def changeCellValueAtIndex(self, index, value):
		self.cells[index].text = value

class DataGridContent(ScrollView):
	def __init__(self, **kwargs):
		super(DataGridContent, self).__init__(**kwargs)
		self.rowStoreWidget = []
		self.rowContainer = BoxLayout(orientation='vertical')
		self.rowContainer.size_hint = (None, None)
		self.rowContainer.width = Window.width
		self.rowContainer.height = 0;
		self.add_widget(self.rowContainer)
		self.do_scroll_x = False
		self.do_scroll_y = True
        
	def addRow(self, widget, index):
		self.rowContainer.add_widget(widget)
		self.rowContainer.height += 32
		print 'insert item at index: ' + str(index)
		self.rowStoreWidget.append(widget)

	def removeRowAtIndex(self, index):
		print 'remove item at index: ' + str(index)
		self.rowContainer.remove_widget(self.rowStoreWidget[index])
		del self.rowStoreWidget[index]
		self.rowContainer.height -= 32

	def changeCellValueAtRow(self, rowIndex, cellIndex, cellValue):
		self.rowStoreWidget[rowIndex].changeCellValueAtIndex(cellIndex, cellValue)

	def insertRowAtIndex(self, row, index):
		self.rowContainer.add_widget(row, index)
		self.rowContainer.height += 32
		print 'insert item at index: ' + str(index)
		self.rowStoreWidget.append(row)


# class data grid contain rows
class DataGrid(BoxLayout):
	def __init__(self, **kwargs):
		# init box layout
		super(DataGrid, self).__init__(**kwargs)
		self.orientation = 'vertical'
		self.currentRowCount = 0;

	# function used to init grid
	def setupGrid(self, headers, width, height):
		self.rowWidth = width
		self.rowHeight = height
		# init header
		self.headerRow = DataGridRow(headers, cols=len(headers), index=None)
		self.headerRow.size_hint = (None, None)
		self.headerRow.width = self.rowWidth
		self.headerRow.height = self.rowHeight
		self.add_widget(self.headerRow)
		# init body
		self.body = DataGridContent(size_hint=(1, 1), scroll_y=0 )
		self.add_widget(self.body)

	# function used to add new rows to grid
	def addRow(self, rowsData, **kwargs):
		if len(rowsData) < self.headerRow.cols:
			print "Rows is not enough data to insert"
			return

		#init new row
		newRow = DataGridRow(rowsData, cols=self.headerRow.cols, index=self.currentRowCount, id='rowID_' + str(self.currentRowCount))
		newRow.size_hint = (None, None)
		newRow.width = self.rowWidth
		newRow.height = self.rowHeight

		# TODO: check to where to insert this data
		addType = kwargs.get('type')
		if addType is not None:
			if addType == 'insert':
				addIndex = kwargs.get('index')
				if addIndex is not None:
					addIndex = self.currentRowCount - addIndex
					self.body.insertRowAtIndex(newRow, addIndex)
					self.currentRowCount += 1
					return
				else:
					print 'wrong or missing index when add row.'
					return
			elif addType == 'first':
				self.body.insertRowAtIndex(newRow, self.currentRowCount + 1)
				self.currentRowCount += 1
				return
		else:
			self.body.addRow(newRow, self.currentRowCount)
			self.currentRowCount += 1
		

	def removeRowAtIndex(self, index):
		self.currentRowCount -= 1
		self.body.removeRowAtIndex(index)

	def changeCellValueAtRow(self, rowIndex, cellIndex, cellValue):
		self.body.changeCellValueAtRow(rowIndex, cellIndex, cellValue)
		



