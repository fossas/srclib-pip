ENV = virtualenv

PIP2 = .env/bin/pip
PYTHON2 = .env/bin/python

.PHONY: install

default: .env install

.env:
	$(ENV) -p python2.7 .env

install: .env
	$(PIP2) install -r requirements.txt
	$(PYTHON2) setup.py install

clean:
	rm -rf dist build srclib_pip.egg-info .env
