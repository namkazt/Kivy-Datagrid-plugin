import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
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
from BorderBehavior import BorderBehavior
from kivy.properties import ObjectProperty

class BorderButton(Button, BorderBehavior):
	def __init__(self):
		super(BorderButton, self).__init__()

class BorderLabel(Label, BorderBehavior):
	def __init__(self):
		super(BorderLabel, self).__init__()

# class grid row
class DataGridRow(GridLayout):
	bgColorProperty = ObjectProperty(Color(1,1,1,0.1))

	def __init__(self, data, **kwargs):
		super(DataGridRow, self).__init__(**kwargs)
		self.index = kwargs.get('index');
		self.cells = []
		self.listWidth = kwargs.get('listWidth');

		for colIndex in range(0, self.cols):
			cell = None
			# label cell
			if data[colIndex]['type'] == 'Label':
				cell = Label()
				cell.valign = 'middle'
				cell.halign = 'center'
			# border lable cell
			elif data[colIndex]['type'] == 'BorderLabel':
				cell = BorderLabel()
				cell.valign = 'middle'
				cell.halign = 'center'
				if data[colIndex].get('borders'):
					cell.borders= data[colIndex]['borders']
				else:
					cell.borders= (.5, 'solid', (1,1,1,0.3))
			# button cell define
			elif data[colIndex]['type'] == 'Button':
				self.bgColorProperty = Color(1,1,1,0)
				cell = Button()
				if data[colIndex].get('callback'):
					callback =  data[colIndex].get('callback')
					param_kwargs = data[colIndex].get('params')
					if not param_kwargs:
						param_kwargs = {}
					cell.bind(on_press=partial(callback, **param_kwargs))
			# border button cell define
			elif data[colIndex]['type'] == 'BorderButton':
				self.bgColorProperty = Color(1,1,1,0)
				cell = BorderButton()
				if data[colIndex].get('borders'):
					cell.borders= data[colIndex]['borders']
				else:
					cell.borders= (.5, 'solid', (1,1,1,0.3))
				if data[colIndex].get('callback'):
					callback =  data[colIndex].get('callback')
					param_kwargs = data[colIndex].get('params')
					if not param_kwargs:
						param_kwargs = {}
					cell.bind(on_press=partial(callback, **param_kwargs))

			cell.size_hint = (None, 1)
			cell.text = data[colIndex]['text']
			cell.width = self.listWidth[colIndex]
			self.add_widget(cell)
			self.cells.append(cell)

		with self.canvas.before:
			self.bgColor = Color(rgba=self.bgColorProperty.rgba)
			self.rect = Rectangle(pos=self.center, size=(self.width/2., self.height/2.))
		self.bind(pos=self.updateRect,size=self.updateRect,bgColorProperty=self.updateRect)

	def changeCellValueAtIndex(self, index, value):
		self.cells[index].text = value

	def updateRect(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size
		self.bgColor.rgba = self.bgColorProperty.rgba

	def changeRowColor(self, changedColor):
		self.bgColorProperty = changedColor

	def cleanCells(self):
		del self.cells[:]

class DataGridContent(ScrollView):
	def __init__(self, **kwargs):
		super(DataGridContent, self).__init__(**kwargs)
		self.rowStoreWidget = []
		self.rowStoreWidgetByID = {}
		self.rowHeight = kwargs.get('row_height')
		self.rowContainer = BoxLayout(orientation='vertical')
		self.rowContainer.size_hint = (1, None)
		#self.rowContainer.width = Window.width
		self.rowContainer.height = 0;
		self.add_widget(self.rowContainer)
		self.do_scroll_x = False
		self.do_scroll_y = True
		
	def addRow(self, widget, index):
		self.rowContainer.add_widget(widget)
		self.rowContainer.height += self.rowHeight
		print 'insert item at index: ' + str(index)
		self.rowStoreWidget.append(widget)
		self.rowStoreWidgetByID[widget.id] = widget

	def removeRowById(self, widget_id):
		if widget_id in self.rowStoreWidgetByID:
			_widget = self.rowStoreWidgetByID[widget_id]
			self.rowContainer.remove_widget(_widget)
			index = self.rowStoreWidget.index(_widget)
			del self.rowStoreWidget[index]
			self.rowContainer.height -= self.rowHeight
			del self.rowStoreWidgetByID[widget_id]

	def removeRowAtIndex(self, index):
		print 'remove item at index: ' + str(index)
		_widget = self.rowStoreWidget[index]
		self.rowContainer.remove_widget(_widget)
		del self.rowStoreWidget[index]
		self.rowContainer.height -= self.rowHeight
		if _widget.id in self.rowStoreWidgetByID:
			del self.rowStoreWidgetByID[_widget.id]

	def changeCellValueAtRow(self, rowIndex, cellIndex, cellValue):
		self.rowStoreWidget[rowIndex].changeCellValueAtIndex(cellIndex, cellValue)

	def insertRowAtIndex(self, row, index):
		self.rowContainer.add_widget(row, index)
		self.rowContainer.height += self.rowHeight
		print 'insert item at index: ' + str(index)
		self.rowStoreWidget.append(row)
		self.rowStoreWidgetByID[row.id] = row


# class data grid contain rows
class DataGrid(BoxLayout):
	def __init__(self, **kwargs):
		# init box layout
		super(DataGrid, self).__init__(**kwargs)
		self.orientation = 'vertical'
		self.currentRowCount = 0;
		self.listWidth = []

	# function used to init grid
	def setupGrid(self, headers, width, height):
		self.rowWidth = width
		self.rowHeight = height
		# init header
		for item in headers:
			self.listWidth.append(item["width"])

		self.headerRow = DataGridRow(headers, cols=len(headers), index=None, listWidth=self.listWidth)
		self.headerRow.size_hint = (1, None)
		self.headerRow.height = self.rowHeight
		self.add_widget(self.headerRow)
		# init body
		self.body = DataGridContent(size_hint=(1, 1), scroll_y=0, row_height=height)
		self.add_widget(self.body)

	# function used to add new rows to grid
	def addRow(self, rowsData, **kwargs):
		if len(rowsData) < self.headerRow.cols:
			print "Rows is not enough data to insert"
			return

		widget_id = kwargs.get('id')
		if not widget_id:
			widget_id = 'rowID_' + str(self.currentRowCount)

		#init new row
		newRow = DataGridRow(rowsData, cols=self.headerRow.cols, index=self.currentRowCount, \
			id=widget_id,cellHeigth=self.rowHeight, size_hint=(1, None), \
			height=self.rowHeight, listWidth=self.listWidth)
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

	def removeRowById(self, widget_id):
		self.body.removeRowById(widget_id)

	def removeAllContent(self):
		self.body.cleanRows()
		self.body.rowContainer.clear_widgets()
		self.body.rowContainer.height = 0
		self.currentRowCount = 0

	def changeRowColor(self, rowIndex, changedColor):
		self.body.rowStoreWidget[rowIndex].changeRowColor(changedColor)

	def changeRowColorByID(self, widget_id, changedColor):
		for row in self.body.rowStoreWidget:
			if row.id == widget_id:
				row.changeRowColor(changedColor)
		



