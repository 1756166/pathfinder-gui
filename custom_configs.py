import sys, PyQt5, json, pathfinder_gen
from PyQt5.QtWidgets import (QWidget, QApplication, QComboBox, QLineEdit, QGroupBox, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtCore import pyqtSlot

class MainWin(QWidget):
	waypoints = {}
	def __init__(self):
		super().__init__()
		self.waypoints = self.load_json()
		self.main()

	def main(self):
		self.setWindowTitle('Pathfinder Generation Hub')
		self.setGeometry(100, 100, 400, 400)

		self.new_path_name = QLineEdit(self)
		self.alliance_color = QComboBox(self)
		self.alliance_color.addItems(['Red', 'Blue'])
		self.new_path_submit = QPushButton('Add new path', self)
		self.new_path_submit.clicked.connect(lambda: self.create_new_gui(self.new_path_name.text(), self.alliance_color.currentText()))
		self.new_path = [self.new_path_name, self.alliance_color, self.new_path_submit]

		self.grid = QGridLayout()
		self.grid.addWidget(self.widget_group(self.new_path, 'Add new path configuration'), 0, 0)

		self.setLayout(self.grid)
		self.show()

	def load_json(self):
		with open('waypoints.json', 'r') as f:
			waypoints = json.load(f)
		return waypoints


	def widget_group(self, widgets, title):
		widget_group = QGroupBox(title)
		vbox = QVBoxLayout()

		for widget in widgets:
			vbox.addWidget(widget)

		widget_group.setLayout(vbox)
		
		return widget_group

	def create_new_gui(self, title, alliance_color):
		pathfinder_gen.simulate(alliance_color, title, self.waypoints)

app = QApplication(sys.argv)
win = MainWin()
sys.exit(app.exec_())