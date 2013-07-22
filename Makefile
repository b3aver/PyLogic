PROJECT = PyLogic


all: pylogic.py compile
	./pylogic.py

compile: pylogic/gui/MainWindow.py pylogic/gui/AboutBox.py

clean:
	-@rm pylogic/gui/MainWindow.py pylogic/gui/AboutBox.py
	-@rm parser.out parsetab.py
	-@rm pylogic/propositional/parser.out pylogic/propositional/parsetab.py
	-@rm pylocic/first_order/parser.out pylogic/first_order/parsetab.py
	-@rm *pyc pylogic/propositional/*pyc pylogic/first_order/*pyc
	-@rm -R __pycache__ pylogic/__pycache__ pylogic/gui/__pycache__
	-@rm -R pylogic/propositional/__pycache__ pylogic/first_order/__pycache__

documentation:
	pyreverse . -p${PROJECT} -ojpg
	mv classes_${PROJECT}.jpg doc
	mv packages_${PROJECT}.jpg doc

test:
	nosetests3

pylogic/gui/MainWindow.py: pylogic/gui/mainwindow.ui
	pyuic4 --pyqt3-wrapper pylogic/gui/mainwindow.ui > pylogic/gui/MainWindow.py

pylogic/gui/AboutBox.py: pylogic/gui/aboutBox.ui
	pyuic4 --pyqt3-wrapper pylogic/gui/aboutBox.ui > pylogic/gui/AboutBox.py
