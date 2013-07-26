# PyLogic

PyLogic is a tool for theorem proving implemented in Python 3.


## Dependences
- [Python 3](http://www.python.org/download/)
- [pip](https://pypi.python.org/pypi/pip)
- [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/installation.html)
- [ply](http://www.dabeaz.com/ply/) (automatically installed with pip)


## Quickstart

Ensure that dependences are installed before.

```bash
git clone git@github.com:b3aver/PyLogic.git
cd PyLogic
make
```


## Propositional Formulas

The grammar for specify a propositional formula is
```
formula : LETTER
        | NOT formula
        | ( formula CONNECTIVE formula )
```
where `LETTER` is an uppercase letter of the English alphabet,
`NOT` is the minus sign `-`,
and `CONNECTIVE` is one of the following symbols

- `|` or
- `&` and
- `->` implication
- `<-` converse implication
- `<->` biconditional


## Testing

The package includes several tests written with
[unittest](http://docs.python.org/3.3/library/unittest.html).
These tests can be executed with `make test` also if
[Travis](https://travis-ci.org/) says that the current state is
[![Build Status](https://travis-ci.org/b3aver/PyLogic.png)](https://travis-ci.org/b3aver/PyLogic)


# References

- Melvin Fitting. *First-Order Logic and Automated Theorem Proving*.
