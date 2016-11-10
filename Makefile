PIP = .env/bin/pip
PYTHON = .env/bin/python
ENV = virtualenv

.PHONY: install

default: .env install

.env:
	$(ENV) -p python2.7 .env

install: .env
	$(PIP) install -r requirements.txt --upgrade
	$(PYTHON) setup.py install

clean:
	rm -rf dist build srclib_pip.egg-info .env
