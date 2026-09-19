import argparse

from ..configuration import JSONTelldusConfiguraton
from ..session import TelldusLiveSession, TelldusLocalSession
from .mixins import INSTALLED_MIXINS

def parse_args():
    parser = argparse.ArgumentParser("Telldus REST API CLI")
    parser.add_argument('-f', '--file', type=str, default="telldus.json", help="Configuration file.")
    parser.add_argument('-l', '--local', action='store_true', help='Use local API.')
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    for mixin in INSTALLED_MIXINS:
        mixin(subparsers)
    return parser.parse_args()

def run_cli():
    args = parse_args()
    session_cls = TelldusLocalSession if args.local else TelldusLiveSession
    session = session_cls(JSONTelldusConfiguraton(args.file))
    args.func(session, args)
