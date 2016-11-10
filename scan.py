#!/usr/bin/python

from os import path
from glob import glob
import pip
import json


def scan(rootdir):
  req_files = list(set(glob(path.join(rootdir, "**/*requirements*.txt"))) | set(glob(path.join(rootdir, "*requirements*.txt"))))
  source_units = [construct_source_unit(rootdir, req_file) for req_file in req_files]
  print json.dumps(source_units)
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
      "text": file(requirements_path).read()
    }
  }

def construct_dependency(install_req):
  name = install_req.name
  specs = str(install_req.req.specifier)

  return {
    "Name": name,
    "Version": specs
  }
