



all: gui.py compile
	./gui.py


compile: MainWindow.py AboutBox.py


MainWindow.py: mainwindow.ui
	pyuic4 mainwindow.ui > MainWindow.py


AboutBox.py: aboutBox.ui
	pyuic4 aboutBox.ui > AboutBox.py


clean:
	-@rm *pyc MainWindow.py AboutBox.py parser.out parsetab.py
	-@rm propositional/*pyc
# -mv *pyc trash
# -mv MainWindow.py trash
# -mv AboutBox.py trash
# -mv parser.out trash
# -mv parsetab.py trash