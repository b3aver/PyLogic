
PROJECT = PyLogic


all: gui.py compile
	./gui.py


compile: MainWindow.py AboutBox.py


MainWindow.py: mainwindow.ui
	pyuic4 --pyqt3-wrapper mainwindow.ui > MainWindow.py

AboutBox.py: aboutBox.ui
	pyuic4 --pyqt3-wrapper aboutBox.ui > AboutBox.py


clean:
	-@rm MainWindow.py AboutBox.py
	-@rm parser.out parsetab.py
	-@rm propositional/parser.out propositional/parsetab.py
	-@rm first_order/parser.out first_order/parsetab.py
	-@rm *pyc propositional/*pyc first_order/*pyc
	-@rm -R __pycache__ propositional/__pycache__ first_order/__pycache__


documentation:
	pyreverse . -p${PROJECT} -ojpg
	mv classes_${PROJECT}.jpg doc
	mv packages_${PROJECT}.jpg doc
