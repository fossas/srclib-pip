from __future__ import print_function

import sys
import logging
import pip
import json

from os import path
from glob import glob

logging_config = dict(
  version = 1,
  formatters = {
    "f": {
      "format":
      "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    }
  },
  handlers = {
    "h": {
      "class": "logging.StreamHandler",
      "formatter": "f",
      "level": logging.DEBUG,
      "stream": "ext://sys.stderr"
    }
  },
  root = {
    "handlers": ["h"],
    "level": logging.DEBUG,
  },
)

logging.config.dictConfig(logging_config)


def scan(rootdir):
  req_files = list(set(glob(path.join(rootdir, "**/*requirements*.txt"))) | set(glob(path.join(rootdir, "*requirements*.txt"))))
  source_units = [construct_source_unit(rootdir, req_file) for req_file in req_files]
  print(json.dumps(merge_source_units(source_units)))
  return source_units

def construct_source_unit(rootdir, requirements_path):
  pkg = path.dirname(requirements_path)
  name = path.basename(pkg)
  relpath = path.relpath(pkg, rootdir)
  install_reqs = [(install_req, requirements_path) for install_req in pip.req.parse_requirements(requirements_path, session=pip.download.PipSession())]

  return {
    "Type": "PythonRequirementsPackage",
    "Name": name,
    "Dir": relpath,
    "Dependencies": [construct_dependency(install_req[0], relpath) for install_req in install_reqs],
    "Files": [path.relpath(requirements_path, rootdir)],
    "Data": {
      "text": open(requirements_path).read()
    }
  }

def construct_dependency(install_req, req_path):
  name = install_req.name
  specs = install_req.req.specs
  if install_req.link is not None:
    name = install_req.link.url

  return {
    "Name": name,
    "Specs": specs,
    "Path": req_path
  }

def merge_source_units(source_units):
  def helper(acc_unit, unit):
    if unit:
      acc_unit["Files"] = list(set(acc_unit["Files"]) | set(unit["Files"]))
      acc_unit["Data"] = {}
      acc_unit["Dependencies"].extend(unit["Dependencies"])
    return acc_unit

  new_source_units = []
  lookup = {source_unit["Name"]: [] for source_unit in source_units}
  for source_unit in source_units:
    lookup[source_unit["Name"]].append(source_unit)
  for source_units in lookup.itervalues():
    new_source_units.append(reduce(helper, source_units))

  return new_source_units
