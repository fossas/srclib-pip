
import argparse
import os

from scan import scan


def main():
  parser = argparse.ArgumentParser(description="")
  subparsers = parser.add_subparsers(help="", dest="subcmd")

  scanparser = subparsers.add_parser("scan", help="")
  scanparser.add_argument('--repo', default="")
  scanparser.add_argument('--subdir', default=".")
  depresolveparser = subparsers.add_parser("depresolve", help="")
  graphparser = subparsers.add_parser("graph", help="")
  graphparser.add_argument('--verbose', help='verbose', action='store_true', default=True)
  graphparser.add_argument('--debug', help='debug', action='store_true', default=False)
  graphparser.add_argument('--quiet', help='quiet', action='store_true', default=False)
  graphparser.add_argument('--unit-file', help="debugging purposes", default=None)

  args = parser.parse_args()
  if args.subcmd == "scan":
    scan(os.getcwd())


if __name__ == '__main__':
  main()
