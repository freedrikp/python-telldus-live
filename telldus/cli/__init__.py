import argparse

from configuration import JSONTelldusConfiguraton
from session import TelldusSession
from cli.mixins import INSTALLED_MIXINS

def parse_args():
    parser = argparse.ArgumentParser("Telldus REST API CLI")
    parser.add_argument('-f', '--file', type=str, default="telldus.json", help="Configuration file.")
    subparsers = parser.add_subparsers()
    for mixin in INSTALLED_MIXINS:
        mixin(subparsers)
    return parser.parse_args()

def run_cli():
    args = parse_args()
    session = TelldusSession(JSONTelldusConfiguraton(args.file))
    args.func(session, args)
