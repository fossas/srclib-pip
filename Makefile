ENV = virtualenv

PIP2 = .env2/bin/pip
PYTHON2 = .env2/bin/python

PIP3 = .env3/bin/pip
PYTHON3 = .env3/bin/python

.PHONY: install

default: .env install

.env:
	$(ENV) -p python2.7 .env2
	$(ENV) -p python3.5 .env3

install: .env
	$(PIP2) install -r requirements.txt
	$(PYTHON2) setup.py install
	
	$(PIP3) install -r requirements.txt
	$(PYTHON3) setup.py install

clean:
	rm -rf dist build srclib_pip.egg-info .env .env2 .env3
