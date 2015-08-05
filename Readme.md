# Datagrid plugin for Kivy

Kivy: http://kivy.org/#home 
It's a UI framework for python

my work is a plugin that allow to created a grid ( currently kivy not support datagrid yet )

### Using
```python
# create new instance of data grid
self.grid = DataGrid()

# setup grid header
# current grid support this form : 
# {
#  'text': 'xxx',   # title display in header cell
#  'type': 'Lable'  # type can be 'Lable' or 'Button'
# }
# Datagrid will count header elements as collums
self.grid.setupGrid([{'text':"Header 1", 'type':'Lable'}, 
	{'text':"Header 2", 'type':'Lable'}, 
	{'text':"Header 3", 'type':'Lable'}, 
	{'text':"Header 4", 'type':'Lable'}, 
	{'text':"Header 5", 'type':'Lable'}, 
	{'text':"Header 6", 'type':'Lable'}, 
	{'text':"Header 7", 'type':'Lable'}, 
	{'text':"Header 8", 'type':'Lable'}], Window.width, 32)
# add grid to screen or app
self.add_widget(self.grid)

# change cell value ( text ) at row 
# @first param : row index
# @second param : col index
# @last param : value
self.grid.changeCellValueAtRow(3, 0, 'AAAAAAA')
self.grid.changeCellValueAtRow(3, 5, 'AAAAAAA')
self.grid.changeCellValueAtRow(7, 0, 'AAAAAAA')

# test data to add new row
tempData = [{'text':'Item X', 'type':'Lable'}, 
{'text':'Item X', 'type':'Lable'}, 
{'text':'Item X', 'type':'Lable'}, 
{'text':'Item X', 'type':'Lable'}, 
{'text':'Item X', 'type':'Lable'}, 
{'text':'Item X', 'type':'Lable'}, 
{'text':'Item X', 'type':'Lable'}, 
{'text':'Item X', 'type':'Button'}]
# add row normal : push new row at last of datagrid
self.grid.addRow(tempData)
# add row at index
# when add at index = 5 that mean new row is grant index = 5 and old row at index = 5 that change to index = 6 
self.grid.addRow(tempData, type='insert', index=5)
# add row at first of datagrid
self.grid.addRow(tempData, type='first')

# remove row at index
self.grid.removeRowAtIndex(3)
self.grid.removeRowAtIndex(5)
self.grid.removeRowAtIndex(7)

```


