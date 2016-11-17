from __future__ import print_function

import logging
from os import path
from glob import glob
import pip
import json

logging.basicConfig()


def scan(rootdir):
  req_files = list(set(glob(path.join(rootdir, "**/*requirements*.txt"))) | set(glob(path.join(rootdir, "*requirements*.txt"))))
  source_units = [construct_source_unit(rootdir, req_file) for req_file in req_files]
  print(json.dumps(source_units))
  return source_units

def construct_source_unit(rootdir, requirements_path):
  pkg = path.dirname(requirements_path)
  name = path.basename(pkg)
  relpath = path.relpath(pkg, rootdir)
  install_reqs = [install_req for install_req in pip.req.parse_requirements(requirements_path, session=pip.download.PipSession())]

  return {
    "Type": "PythonRequirementsPackage",
    "Name": name,
    "Dir": relpath,
    "Dependencies": [construct_dependency(install_req) for install_req in install_reqs],
    "Data": {
      "text": open(requirements_path).read()
    }
  }

def construct_dependency(install_req):
  name = install_req.name
  specs = install_req.req.specs
  if install_req.link is not None:
    name = install_req.link.url

  return {
    "Name": name,
    "Specs": specs
  }
