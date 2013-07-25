PROJECT = PyLogic


all: pylogic.py compile
	./pylogic.py

compile:
clean:
	-@rm parser.out parsetab.py
	-@rm pylogic/propositional/parser.out pylogic/propositional/parsetab.py
	-@rm pylocic/first_order/parser.out pylogic/first_order/parsetab.py
	-@rm *pyc pylogic/*pyc pylogic/gui/*pyc pylogic/propositional/*pyc pylogic/first_order/*pyc
	-@rm -R __pycache__ pylogic/__pycache__ pylogic/gui/__pycache__
	-@rm -R pylogic/propositional/__pycache__ pylogic/first_order/__pycache__

documentation:
	pyreverse . -p${PROJECT} -ojpg
	mv classes_${PROJECT}.jpg doc
	mv packages_${PROJECT}.jpg doc

test:
	nosetests3
