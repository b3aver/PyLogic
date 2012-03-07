



all: gui.py compile
	./gui.py



compile: MainWindow.py AboutBox.py

MainWindow.py: mainwindow.ui
	pyuic4 mainwindow.ui > MainWindow.py


AboutBox.py: aboutBox.ui
	pyuic4 aboutBox.ui > AboutBox.py